Title: A tour of modern frontend with React and Flux
Date: 2015-08-25
Short_summary: React and Flux have swept the front-end development world in the last year or so. Let's look at them.
Category: Dev
Authors: Vincent


*Reading time: ~10 minutes.*

In this article we are going to have a look at my preferred set of tools for writing React/Flux web apps.
If you don't know React or Flux, you can finds their documentation at their respective websites: [React](http://facebook.github.io/react/), [Flux](https://facebook.github.io/flux/).
<!-- PELICAN_END_SUMMARY -->


## Tools of the trade
The React community is embracing ES6 — and sometimes ES7 — through [Babel](http://babeljs.io/). For those not doing any frontend, ES6 is the new [Javascript standard](http://www.ecma-international.org/publications/standards/Ecma-262.htm) and ES7 is the one that should become the standard next year. Most browsers only support up to ES5 though so we need to compile our "future" code to something current browsers can understand, which is Babel's job.
I personally like Typescript but recently decided to go with Babel for a few reasons:

- A constant changes in libraries and their sheer number were making it very hard to keep up-to-date definitions
- Typescript is still lacking support for some things, making some libraries like [ImmutableJS](http://facebook.github.io/immutable-js/) and its records very hard to use in a type-safe way
- Getting tired of casting things to <any> because of the compiler not picking up the correct things

I do very much like types though and since they are not in the horizon of ES standards, so I will have a look at [Flow](http://flowtype.org/) when it fully [supports ES6](https://github.com/facebook/flow/issues/560). Flow differs from typescript by only being annotations that you can strip down and inferring as much as possible from the context instead of being a language like Typescript.


### devDependencies
If you look at most React/Flux boilerplates, you will notice they often use different tools than you might be used with Angular for example.


Firstly, as mentioned in the previous section, Babel is omnipresent along with its linter of choice, [eslint](http://eslint.org/).


A good number of projects eschew tasks runners such as [gulp](http://gulpjs.com/) in favour of a tool called [Webpack](http://webpack.github.io/) and npm tasks. Webpack is a module bundler like [Browserify](http://browserify.org/) but while Browserify takes the Unix philosophy of having small modules working together, Webpack comes with a lot more out of the box. Both works great though, so choose the one you like the most.


One feature that made Webpack stand out early on with React was hot reloading using [react-hot-loader](https://github.com/gaearon/react-hot-loader) but is now available as [LiveReactload](https://github.com/milankinen/livereactload) for browserify.

Testing wise, I have seen lots of repos using [jsdom](https://github.com/tmpvar/jsdom) which seems backwards to me as we can run tests in actual browsers using [Karma](http://karma-runner.github.io/0.13/index.html) for example.


### Dependencies
In terms of actual dependencies, we obviously need React. Since 0.14, you will also need the [react-dom](https://www.npmjs.com/package/react-dom) package to actually render.

In terms of Flux implementation, my favourite is [Redux](http://rackt.github.io/redux/) which actually deviates of the Flux reference, leaning towards a FRP (look [here](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754) for a nice introduction on Functional Reactive Programming) approach like [Elm](http://elm-lang.org/) and having pure functions.

The documentation of Redux being first-class, I will not write about it and invite you to read it, even if you aren't planning to use it.
Bindings for React can be found under the [react-redux](https://www.npmjs.com/package/react-redux) package.

A very nice thing about having pure reducers in Redux (the equivalent of stores in Flux) is that you can easily build time-travelling tools, replay actions and testing become trivial. Look at [redux-devtools](https://github.com/gaearon/redux-devtools) for the official one.

Lastly there is another optional dependency I like: [ImmutableJS](http://facebook.github.io/immutable-js/). Reducers in Redux are pure but using ImmutableJS gives us a faster `shouldComponentUpdate` (more [info](https://facebook.github.io/react/docs/advanced-performance.html#immutable-js-to-the-rescue)) as we can compare our props by reference rather than inspecting their values deeply.


## A boilerplate
Looking at that list may appear daunting at first and plenty of boilerplates exist but they didn't fit my own needs as I was first writing it in Typescript.

Switching to Babel was pretty trivial as it only involved changing loaders in webpack and the linter.

You can find the boilerplate on [github](https://github.com/Keats/react-redux-boilerplate) and you can have a look at [this example](https://github.com/Keats/react-example) for a toy project made with that boilerplate.


## Conclusion
Combining live reload of components and reducers with the simplicity and easy testing of React and Redux makes for a very good developer experience. 
Some may wonder why not use Elm, ClojureScript or PureScript when looking at what we end up (and we would get types in some of them too!). This is a good point and we are going to look into Elm more seriously in the coming weeks so expect a post about our experience soon.
