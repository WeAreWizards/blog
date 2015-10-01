Title: Trying Rust for web services
Date: 2015-10-01
Short_summary: I made a very basic Rust backend, here's what I think about it
Category: Dev
Authors: Vincent

*Reading time: ~15 minutes.*


Developing web apps in dynamic languages is a breeze when using frameworks like [Django](https://www.djangoproject.com/) for Python.
The downsides are that software written in dynamic languages is harder, at least in my opinion, to maintain, to refactor and you also need to write tests to cover potential errors that would simply not be possible with a compiler.
<!-- PELICAN_END_SUMMARY -->


While I would use Flask or Django for a small project, I would definitely prefer having help from a compiler for a long-lived product. The fact that compiled languages are generally faster than dynamic ones is a nice bonus too.

The two choices in my mind right now for a compiled language are Go and Rust. Some (ie Tom) would say Haskell, others would say Scala but in the end it's down to preferences.

I previously used Go for a few projects and I quite liked it despite some annoying quirks such as package management (might be solved by [gb](https://getgb.io/) now) and seeing `interface {}` in some libraries to get around the weak type system. On the other hand, I have been following [Rust](https://www.rust-lang.org/) development for quite a while but didn't play with it more than a couple of toy programs. I was keen to see if it could work as the backend for a web app, which in short means a HTTP server receiving and sending JSON while talking to a Postgres database. There are obviously an awful lot of other things but let's keep it simple for now.


## The demo
You can see the project at [https://github.com/Keats/webrust](https://github.com/Keats/webrust).
This is a simple webapp with one endpoint that responds to either a GET or a POST. The GET handler will return all the passwords in the table and the POST will insert a record into the table and return a 201 status code.

For the HTTP framework, I have used [Iron](http://ironframework.io/) which was simple to use, granted I only created 2 routes and had no middlewares but there are other alternative such as [rustful](https://github.com/Ogeon/rustful) and [nickle.rs](http://nickel.rs/).

For the postgres side, there is a crate (the term for a package in Rust) called [postgres](https://github.com/sfackler/rust-postgres). I'm also using a pool manager called [r2d2](https://github.com/sfackler/r2d2) because I didn't know about [Arc](https://doc.rust-lang.org/std/sync/struct.Arc.html) and couldn't pass the connection itself as it wasn't thread safe.

The Makefile for Postgres was taken from another Iron + Postgres project I have found on Github: [rustwebapp](https://github.com/superlogical/rustwebapp).


Keep in mind I'm a newbie in Rust so there are probably lots of things I'm doing wrong in there, feel free to point them out!
> **Note:** the server is currently quite slow, only handling around 6.5k req/s for the GET handler, removing the database part makes it shoot up to 70k req/s so something must be going wrong somewhere around postgres


## What I liked
[Cargo](https://crates.io/), Rust package manager, works pretty damn well and its configuration file `Cargo.toml` is easy to write and understand. It is also used to build and run your package.

The language itself is very nice and easy to get started, granted this demo is very simple and doesn't have a single lifetime. Every single time the compiler didn't complain, whatever I wanted to do was working and whenever it complained, the message was clear enough for me to realize what was happening.  
This is not going to be exhaustive by any means but here are the things I liked and disliked the most.


### Result and Option types
Every Go developers has been caught forgetting the `if err != nil` when calling a function, every Python developers has seen exceptions that they didn't realise could happen. Rust (and some functional languages it's borrowing the concept from) bake those in the language, using the [Result](https://doc.rust-lang.org/std/result/) type.
In practice, this means that by returning this type, the caller **has** to handle the possible errors. It wouldn't even compile if you didn't as we will see later, unless you use `.unwrap()` which is a way to get panics if there is an error.

The Option types is the same as the Maybe in FP, it represents the possibility of a value which Javascript would benefit greatly from for example (`undefined is not a function` anyone?).


### Pattern matching
The easiest way to handle the above types is called *pattern matching* and is awesome in Rust.
As an example from the demo, here's how to handle the Result from `list_passwords` that fetches all the passwords from the table in our handler:

```rust
match dal::list_passwords(conn) {
    Ok(passwords) => {
        let response_payload = try_or_500!(serde_json::to_string(&passwords));
        Ok(Response::with((status::Ok, response_payload)))
    },
    Err(e) => {
        Ok(Response::with((status::InternalServerError)))
    }
}
```
> **Note:** Rust automatically returns the last value, in that case the Ok() ones. Iron handler return type is a Result so I should probably return an Err but it currently works well enough™

As mentioned earlier, Rust forces us to handle the result properly: removing the Err branch errors with the following message `error: non-exhaustive patterns: Err(_) not covered [E0004]`.

Pattern matching is obviously not limited to Result and Option and can be used anywhere you would want a if/else or a switch.

### Macros
Macros are a way to abstract some code but, instead of a function call, the macro is expanded where it's called at compilation time. In practice it means you can simplify code without the overhead of calling a function. The most used macro is probably [try!](https://doc.rust-lang.org/std/macro.try!.html) which returns the error if there is one or gives the result value otherwise. Here's an example from the demo: while trying things out I ended up with the following two lines in each http handler to get a connection to postgres.

```rust
let pool = req.get::<PRead<db::PostgresDB>>().unwrap();
let conn = pool.get().unwrap();
```
As you can see, I use `unwrap` which means it can panic in case of errors. I wrote the following macro to clean it up:

```rust
// db.rs
// Gets a connection from the pool from the given request or returns a 500
macro_rules! get_pg_connection {
    ($req:expr) => (match $req.get::<persistent::Read<db::PostgresDB>>() {
        Ok(pool) => match pool.get() {
            Ok(conn) => conn,
            Err(_) => {
                println!("Couldn't get a connection to pg!");
                return Ok(Response::with((status::InternalServerError)));
            }
        },
        Err(_) => {
            println!("Couldn't get the pg pool from the request!");
            return Ok(Response::with((status::InternalServerError)));
        }
    })
}

// main.rs
// we can use the macro that way in a handler, notice the ! to indicate it's a macro
let conn = get_pg_connection!(req);
```
The last line in the snippet will get a connection or will return a 500 if anything fails in the middle. 

You can even have macros checking [SQL syntax](https://github.com/sfackler/rust-postgres-macros) or [HTML one](https://github.com/lfairy/maud) at compile time! Neat!


## What I didn't like
I think it can be summed up in one word: documentation.

Most of the crates I have looked at (except the postgres one) have next to no real documentation, only a maze of links to click in the generated rustdoc that pulls the in-code documentation into a nice looking website. This is useful if I want to know more details about a type or a trait but doesn't help me understanding how am I supposed to use it. Having to go through the tests or the code directly to see what I am supposed to do for every crate instead of having a "How to use" documentation is annoying. 

The provided documentation can also be outdated as it is currently not integrated with Cargo. There is an [open issue](https://github.com/rust-lang/crates.io/issues/91) for that though.

## Rust for a backend yet?
I don't think I would use Rust if I had to choose a backend language right now. The toy project was intentionally small but there are lots of other things needed for a backend not shown here:

- *sending emails*: I found [rust-smtp](https://github.com/amousset/rust-smtp) but haven't tried it
- *templates*: needed for example for emails, there is [handlebars](https://github.com/sunng87/handlebars-rust) and if I have time I would like to port a subset of [Jinja2](http://jinja.pocoo.org/docs/dev/). There is also some compile-time HTML templating using macros such as [maud](https://github.com/lfairy/maud)
- *serialization e.g. between services* : there is [rust-protobuf](https://github.com/stepancheg/rust-protobuf)
- *database migrations*: we could probably use [Alembic](http://alembic.readthedocs.org/en/latest/), a python library
- *logging*
- *error reporting*
- and probably a bunch of other things that I can't think of right now

There are also a few open questions where I haven't spent the time to look for the answer:

- *testing*: are there hooks available somewhere to truncate the database between tests?
- *mocking*: often you want to mock things in test, how would that work in Rust?

I think that, with a bit more time, the ecosystem will be good enough to make Rust a good first choice but it is not there right now. If I had to start a project now, I would lean towards Go but who knows for the one after!

As mentioned before, I'm a Rust beginner so do not hesitate to correct me and I would definitely appreciate PRs on the demo to see how it could improve.
