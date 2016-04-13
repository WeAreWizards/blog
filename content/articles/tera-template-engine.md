Title: Introducing Tera, a template engine in Rust
Date: 2016-04-14
Short_summary: Talking about a template engine in Rust called Tera, inspired by Jinja2 and Django
Category: Dev
Authors: Vincent


*Reading time: ~15 minutes.*

Back in October 2015, I tried [Rust for web services](https://blog.wearewizards.io/trying-rust-for-web-services) and found the ecosystem lacking at the time. I've been working on porting some of the tools we use in [Proppy](https://proppy.io/) to Rust: [jwt](https://crates.io/crates/jsonwebtoken), [bcrypt](https://crates.io/crates/bcrypt) (granted that Argon2 seems superior) and a [migration tool](https://crates.io/crates/dbmigrate). While I mostly do SPAs these days and don't write many templates in the backend, I still need one for some occasions. Being a Python, I like [Jinja2](http://jinja.pocoo.org/docs/dev/) and [Django templates](https://docs.djangoproject.com/en/1.9/topics/templates/#the-django-template-language). Here's how I attempted to port them to Rust and the result is [Tera](https://github.com/Keats/tera/).
<!-- PELICAN_END_SUMMARY --> 

## Goals and philosophy
As mentioned before, the inspiration comes from both Jinja2 and django templates. As you might know, those two have similar syntax but different philosophies: Django templates are for presentation only and don't have a lot of logic allowed while Jinja2 is way more powerful.
I side with Django on this one as complex logic is better put in code than in a template but Django goes a bit too far by even not supporting something like `{{ count + 1 }}`.

So here are some of the things I want:

- math operations in templates
- no macros or other complex logic in the template
- beautiful html output out of the box (ie no need for the `{{-` tags)
- simple inheritance
- simple to use filters
- able to register new tags easily like the `{% url ... %}` in Django

While new tags are definitely logic added in the template, that logic would have to be written in Rust and not in a template. That limits reusability but is simpler to understand in the end.

Filters should be kept simple and be limited in scope: variable in, modifier function with optional argument and return a string. The easiest to think of would be uppercase, lowercase, capitalize and more importantly time formatting. Here are some examples of how it should look:
```
{{ name | uppercase }}
{{ birthday | time:"YYYY-MM-dd" }}
```
Users should be able to add their own filters as well.

In terms of error handling, we cannot do anything if a template cannot be parsed so panicking when encountering an error is fine and compilation should be done at compile time to ensure everything works perfectly (more on that on the README.md).
On the API side, using Tera should be trivial:

- give a glob that will select all the templates
- add tag/filter to Tera
- parse all templates
- create a context easily (not as simple as a dict obviously though)
- call a render method that returns a `Result`

Template compilation should only happen once by using something like [lazy_static](https://crates.io/crates/lazy_static).

Let's see how it's built now!

## How it's made
I actually thought of making a template engine after watching the "Lexical Scanning in Go" video by Rob Pike ([youtube link](https://www.youtube.com/watch?v=HxaD_trXwRE)). 

### Lexer/Parser
This talk explains how the lexing in the [template package in the Go standard library](https://golang.org/pkg/text/template/) is implemented. I thought it was pretty cool and implemented something similar last summer.
For those that don't want to watch the video, here's a quick summary.

The lexer can be in a few states: inside a block, text, space, number, identifier, string for Tera currently and there are actions that represents what we do and result in a new state. In short, that means we have a state function that takes the lexer as an argument and returns a state function. While this is easy to do in Go, you cannot do reference the type while declaring it but it's ok to do so for a struct.
```rust
// working
struct StateFn(Option<fn(&mut Lexer) -> StateFn>);
// not working
type StateFn = fn(&mut Lexer) -> Option<StateFn>;
```
Thanks for the help on IRC for that one.
The lexer just runs the state function until we reach EOF which in our case is represented by returning `None` as a state function. Here's the whole run method of the lexer:

```rust
pub fn run(&mut self) {
    loop {
        let StateFn(state_fn) = self.state;
        if state_fn.is_none() {
            break;
        }
        self.state = state_fn.unwrap()(self);
    }
}
```
The actions read the next character and know what to do for each kind of character, eg. finding a number in a variable block will return the `lex_number` state function. The lexer ouput is a vector of tokens that ends with either a EOF or and error.

You can read the whole lexer [on github](https://github.com/Keats/tera/blob/fddb8a0b82cba7374bd0552fed1cf831b8943395/src/lexer.rs), it is actually quite simple and readable.


The parser is quite simple as well. Since we are either in text, in a variable block or in a tag block, we just handle those cases in a loop and use EOF to break. Each "state" knows how to parse itself so the main logic is actually only:

```rust
pub fn parse(&mut self) {
    loop {
        match self.peek().kind {
            TokenType::TagStart => self.parse_tag_block(),
            TokenType::VariableStart => self.parse_variable_block(),
            TokenType::Text => self.parse_text(),
            TokenType::Eof => break,
            _ => unreachable!()
        };
    }
}
```

The trickiest bit was handling precedence in blocks so that something like `{{1 / 2 + 3 * 2 + 42}}` would parse as expected. This is done by assigning precedence values to each kind of token and looking forward to see if something with higer precedence is coming. I would be surprised if there was not a bug in there.

The output of the parser is a classic AST.

### Context
Context is the part where ease of use compared to dynamic languages really show. In python I can just pass a dict `{"user": user, "count": 1}` to Jinja2 or Django and be done with it. In Rust, it can't be that easy unfortunately.
Here's the same context as above for Tera:

```rust
let mut context = Context::new();
context.add("user", &user);
context.add("count", &1);
```
To make that possible, Tera uses [serde](https://github.com/serde-rs/serde) which means that in the example above, the `user` variable would have to implement the `Serialize` trait. This makes Tera annoying to use on non-nightly Rust as compiler plugins are not stable yet but Serde is the future for serialization in Rust so might as well embrace it.

### Rendering
In the rendering phase, we take the AST from the parser and traverse it, replacing variables with values from the context and handling the various tag blocks. It is also home to some terrible terrible code, namely the [`eval_condition`](https://github.com/Keats/tera/blob/fddb8a0b82cba7374bd0552fed1cf831b8943395/src/render.rs#L126-L241) method that checks `if` and `elif` conditions. It has a cyclomatic complexity of 27 apparently.
It also contains the classic test fixing snippet that will be removed after I handle calculations properly:

```rust
// TODO: fix properly
// TODO: add tests for float maths arithmetics
if result.fract() < 0.01 {
    result = result.round();
}
```

## Feedback on the dev aspect
The more Rust I do, the more I like it. There are times where you might look at the screen blankly for a few minutes and then decide to have a walk instead but it happens less and less. IRC and the [Rust subreddit](https://www.reddit.com/r/rust) are very good source for help if you are stuck and they have interesting conversations.

With no hesitation, [Clippy](https://github.com/Manishearth/rust-clippy) is the MVP of the development tools I'm using at the moment across all languages (Rust, Python and TypeScript mostly). It is a linter that catches lots of errors or bad code and shows you how to fix or how to do what you wanted to do but in a clearer way. The team is adding lints continuously so I usually just `cargo update` my projects every week or so just so I can run the latest `clippy` on it.

## What's next
The main things Tera are missing right now are filters and a way to add custom tag blocks. If anyone thinks that it is 2016 and therefore should use a parser combinator, feel free to submit a PR! I also welcome any feedback on Tera design as it doesn't have to be a clone of Jinja2 or Django.

Since I am quite busy with our first product [Proppy](https://proppy.io/), I won't have a huge amount of time so any help is welcome.

To finish on a "Rust for web" note, the last main thing I would miss to try it for real is a validation crate that would work [like this gist](https://gist.github.com/Keats/32d26f699dcc13ebd41b). We use [marshmallow](https://marshmallow.readthedocs.org/en/latest/) in proppy and it makes working with API a breeze.
