Title: Experience report: Rocket lander in Elm
Date: 2015-02-15
Short_summary: We build a small game in the programming language Elm.
Category: Dev
Authors: Tom

*Reading time: ~10 minutes.*

Writing anything substantial in JavaScript is hard because JavaScript
lacks many of the tools programmers expect these days, like a coherent
and strong type system.
<!-- PELICAN_END_SUMMARY -->

For that reason we are investigating various new compile-to-JavaScript
languages. In this post we're looking at
[Elm](http://elm-lang.org/). To get a better feel for the language I
implemented a small game:

[Play the demo (desktop only, sorry!)](/rocket-lander-in-elm-extra/ship.html)

First though, why is JavaScript hard? Consider the following cases:

```js
> "hi" * 0
NaN
> "2" * 0
0
> "2" + 0
"20"
> null - undefined
NaN
```

[The famous Wat video](https://www.destroyallsoftware.com/talks/wat)
has more examples after the brief part about Ruby.

People noticed this of course, and to fix these issues they started
developing new languages that transpile to JavaScript. Some well-known
ones are [CoffeeScript](http://coffeescript.org/),
[TypeScript](http://www.typescriptlang.org/) and
[Dart](https://www.dartlang.org/).

I have spent a reasonable amount of time with all of the above,
writing actual production code. I consider all of them an improvement
over the very low bar that is JavaScript, but none of them get me
excited.

Picking e.g. TypeScript: It is high-ceremony to define interfaces, and
the type-safety only helps if a sufficiently large amount of code is
type-annotated. It's like a phase change: Below a certain threshold
one might as well just omit all annotations because they help so
little. Luckily a large body of type annotations has been
[developed already](https://github.com/borisyankov/DefinitelyTyped/).

The following snippet is a simplified version of a production
bug we had because of an intermediate function with an `any` type
argument:

```js
function mul(a: number, b: number) {
  return a * b;
}

function anymul(a: any, b: any) {
  return mul(a, b);
}

// The following doesn't compile and that's great.
console.log(mul([], 0)); // Breaks!

// This does compile though:
console.log(anymul([], 0));
```

In the last few years the space of compile-to-JavaScript got more
crowded, and a lot of the new entrants are either based on more
principled languages like Haskell, or compile well-typed languages
directly. To name a few: [PureScript](http://www.purescript.org/),
[js_of_ocaml](http://ocsigen.org/js_of_ocaml/),
[ghcjs](http://ghcjs.org/), [Elm](http://elm-lang.org/),
[Fay](https://github.com/faylang/fay/wiki),
[clojurescript](https://github.com/clojure/clojurescript),
[scala.js](http://www.scala-js.org/).


## Enter Elm

Elm is a statically typed, functional language with immutable data
structures and first-class support for [functional reactive
programming](http://en.wikipedia.org/wiki/Functional_reactive_programming).

Elm also comes with a standard library that contains lots of useful
tools such as an implementation of the
[virtual-DOM](https://github.com/Matt-Esch/virtual-dom),
famous for making [React](http://facebook.github.io/react/) so
speedy.

Like in Haskell type annotations can be given inline, or in a line
above a function, and types always start with upper case:

```elm
1 : Int
True : Bool
["ab", "cde"] : List String

mul : Int -> Int -> Int
mul a b = a * b
```

Elm starts execution at the `main` entry point:

```
import Text

main = Text.plainText "Hello from Elm."
```

To see more code check out our rocket lander game
[on GitHub](https://github.com/WeAreWizards/elm-rocket-lander/blob/master/Ship.elm)

To get going I recommend installing Elm via Haskell's
[Cabal-Install](https://www.haskell.org/cabal/) which is
available on most distributions:

```
cabal update
cabal install elm-make elm-package elm-compiler
```

This is not a tutorial so I refer to Elm's
[own documentation](http://elm-lang.org/Learn.elm) to learn more.


# FRP

Elm's functional reactive programming (FRP) connects inputs
("signals") to code that depends on these signals, forming a directed
graph in the process.

Anything that generates DOM events can be a signal in Elm. E.g. the
mouse moving or a key press. Elm also has a signal that generates a
steady tick, e.g. at 30 frames-per-second, which is useful for
programming games. **Edit:** As Jason Merrill points out
[in the comments](https://blog.wearewizards.io/experience-report-rocket-lander-in-elm#comment-1863077473)
there is `fpsWhen` which allows switchting of the `fps` updates. Thanks Jason!

Every signal in Elm propagates to all code that depends on it. The
flow is usually something like (Input -> Update application state ->
Redraw application).

Elm requires setting up the entire signal graph *before* the
application starts. That makes it easier to reason about inputs
flowing through the code, but it also comes with some downsides:

E.g. for the
[rocket lander demo](/rocket-lander-in-elm-extra/ship.html) I need a
30 frames-per-second signal to animate the game. I have to set that up
at game start and can't switch it off. I.e. the help-screen at the
beginning is re-rendering 30 times a second, even though nothing
changes.

For a silly little Game that's probably fine. Consider though: An app
that deals with user input will see a few events a second with long
pauses of nothing happening. If you wanted to add an animation that
fades out at 30 frames per second then the app would need to run at 30
FPS the whole time. In these cases it's best to use JavaScript
directly via Elm's ([ports](http://elm-lang.org/learn/Ports.elm)).

See
[this video from Strange Loop 2014](https://www.youtube.com/watch?v=Agu6jipKfYw)
for why the FRP graph is fixed.

# Maturity

Elm is new, and it shows. There are very few libraries. There are also
bugs: Despite the promise of producing error-free JavaScript I managed
to create a few compiling-but-broken programs. E.g. the following
compiles,

```Elm
 ship = shipUpdate
           game.gravity
           (if game.ship.fuel > 0 then arrows.y == 1 else False)
           (if game.ship.fuel > 0 then arrows.x else 0)
           ship
```

but throws a `"ship is undefined"` error in JavaScript. I used `ship`
instead of `game.ship` in the last line by accident.

Interacting with the outside world through WebSockets and HTTP works
but is not well thought out. E.g. there is no error handling for
WebSockets. Elm's main author, Evan Czaplicki, has some good ideas for
improving this with a
[promise-API](https://github.com/elm-lang/core/blob/promises/src/Promise.elm)
so I don't think this will be a problem for much longer.

# Would use again

Despite sounding critical my experience was very smooth. Elm requires
code to be explicit about state, and cheating is *very hard*. After a
few hours of getting used to that I reaped the benefits in form of a
game that worked immediately.

I believe that Elm will be usable for non-game programming at some
point, but it's still missing a few bits like the promise API I
mentioned above.

Just as I finished writing this Evan released an
[excellent tutorial on how to architect apps in Elm](https://github.com/evancz/elm-architecture-tutorial#the-elm-architecture)
