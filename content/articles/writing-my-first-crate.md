Title: Writing my first Rust crate: jsonwebtoken
Date: 2015-11-04
Short_summary: I talk about the experience of writing a library in Rust to handle JWTs 
Category: Dev
Authors: Vincent

*Reading time: ~10 minutes.*

After [looking into Rust for webservices]({filename}/articles/rust-for-web-services.md), I concluded that, while it was not mature enough yet in my opinion, the language itself is quite nice and I would be interested in writing more of it. So here it is, my first crate (the name for packages in Rust): [jsonwebtoken](https://crates.io/crates/jsonwebtoken) (code on [github](https://github.com/keats/rust-jwt)).
<!-- PELICAN_END_SUMMARY -->


## What are JWTs
First of all a very quick introduction on JSON Web Token (JWT). If you already know about them you can skip this.

JWTs are a way to transmit data using JSON — hence the name — and are mostly used for APIs and token based authentication. You can read the standard [there](http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html).

Rather than having a session in a database, you would store some non-sensitive data in your token that allow you to identify the user.

Here's what a JWT looks like (with the fields shortened for example's sake):

```js
// header.payload.signature
eyJhbGciOiJIUzI1Ni.eyJzdWIiOiIxMjM0NTY3ODkwIn0.Rq8IxqeX7eA6GgYxlcHdP
```

From the code above, you can see that a JWT has 3 parts, separated by a `.`.
All of those parts are base64 encoded, which means is trivial to decode (remember the non-sensitive data point above?).


The first is the header, that typically contains the following:
```js
{
  "alg": "HS256", // which algorithm was used to sign
  "typ": "JWT"  // actually optional
}
```

The second is the claims object, which contains an arbitrary JSON object. There are 
some reserved claim name such as `exp` for an expiration timestamp but none of them are
mandatory. Typically in an app, you would store the user id along as some token metadata such as exp mentioned above for example.

The last part is the signature which is obtained the following way in pseudo-code:

```
  payload = base64(header) + "." + base64(claims)
  // "secret" is your secret private key
  signature = Hmac(payload, "secret", Sha256) 
```

As you can see it's quite a convenient way to transfer some data and the signature ensures that the payload was not tampered with (there are some issues though, such as [this vulnerability](https://auth0.com/blog/2015/03/31/critical-vulnerabilities-in-json-web-token-libraries/)).


## Enter jsonwebtoken
I was implementing JWT in a Go project using the [jwt-go](https://github.com/dgrijalva/jwt-go) library when I realised a JWT library was something simple enough that I could try in Rust.

We can see there are already [crates](https://crates.io/search?q=jwt) for that available but [one](https://github.com/GildedHonour/frank_jwt) only allows string types and the other put too much important on the registered claims to my liking.

I didn't implement the standard to the letter as I wanted to keep it simple for now and not support some part of it (having `none` a valid value for the alg header makes no sense to me therefore is not supported).


Compared to the Go library (which is quite good!), using Rust allows leveraging generics to have type-safe claims.
For example, the claims in jwt-go are stored in a `map[string]interface{}` which is the only way to do so and therefore need type assertion when decoding claims to access its true type. The next version (v3 at the time of writing) seem to allow passing a struct though.

Here's how jsonwebtoken is used in practice, taken from the example in the crate:

```rust
extern crate jsonwebtoken as jwt;
extern crate rustc_serialize;

use jwt::{
    Algorithm,
    encode,
    decode
};

// Deriving RustcEncodable and RustcDecodable make Claims satisfy the jwt::Part trait
#[derive(Debug, RustcEncodable, RustcDecodable)]
struct Claims {
    sub: String,
    company: String
}

fn main() {
    let my_claims = Claims {
        sub: "b@b.com".to_owned(),
        company: "ACME".to_owned()
    };
    let key = "secret";

    let token = match encode::<Claims>(my_claims, key.to_owned(), Algorithm::HS256) {
        Ok(t) => t,
        Err(_) => panic!()
    };
    // or let token = try!(encode::<Claims>(my_claims, key.to_owned(), Algorithm::HS256));

    // And then decode it back into a Claims object
    let claims = match decode::<Claims>(token.to_owned(), key.to_owned(), Algorithm::HS256) {
        Ok(c) => c,
        Err(err) => match err {
            Error::InvalidToken => panic!(), // Example on how to handle a specific error
            _ => panic!()
        }
    };
    // or let claims = try!(decode::<Claims>(token.to_owned(), key.to_owned(), Algorithm::HS256));
}
```

On the other hand, decoding the token gives you an instance of the `Claims` struct declared in the function and thanks to the `Result` type, we are certain that if we are in the `Ok()` branch, the variable contains valid data.

How cool is that? And we can use any struct we want as long as the struct we use satisfy the [`Part` trait](https://github.com/Keats/rust-jwt/blob/6ae77c0b068328c47febe4169d6d28c0c66ba101/src/lib.rs#L29-L47), which is done automatically by deriving `RustcEncodable` and `RustcDecodable`.
I'm guessing other languages with generics implement similar things for their JWT libraries but it feels cleaner to me compared to the current version of the Go one.


## Thoughts
Here are some thoughts on the process of creating that crate.


### Cargo
Cargo is really cool. It probably is the smoothest package manager of all the programming languages that I've tried.
From installing crates to publishing the package on [crates.io](https://crates.io/), everything works.

I think the main thing missing for me is built-in vendoring, to not be dependent on a third party (crates.io).


### Error handling
One of the most annoying thing for me in Go is all those `if err != nil`. After trying Rust, I wish there was an equivalent of the `try!` macro so I could get rid of all that code cluttering my functions.

The `Result` type makes error checking mandatory to handle them, like in the example above. Pattern matching also has to be exhaustive, meaning that every possible value of the type I am matching has to be handled, from numbers to enum members and errors.


### Testing and benchmark support
Having tests built-in the language and the package manager is very nice, ensuring there is no barrier to tests.

It is missing an easy setup and teardown method though but I think I have seen macros for that and, hopefully, someone will make a tool similar to the amazing [goconvey](https://github.com/smartystreets/goconvey).


### .to_owned()
If you look at that the code, it is littered with to_owned() calls which converts a string literal (`&str`) into a `String`.

I wish there was a quickway to create a `String` (maybe there is but I haven't found it yet other than writing a macro) such as typing a string into backtick for example:

```
let secret = `secret`;
```
Probably a silly idea but it would make things like tests less noisy.


### Community
The IRC channels (`#rust` and `#rust-beginners` on `irc.mozilla.org`) and the [rust subreddit](https://www.reddit.com/r/rust) were very helpful.


## Conclusion
That was quite a pleasant experience!

While I'm still very much a complete newbie in Rust, I'm looking forward to making another library in Rust.
It will probably some kind of port of [migrate](https://github.com/mattes/migrate), ie a tool to handle SQL migrations.
If you have any comments or find a bug, feel free to open an issue or submit a pull request to [the repo](https://github.com/keats/rust-jwt).

Lastly, thanks to the [pyjwt library](https://github.com/jpadilla/pyjwt) for the API inspiration!
