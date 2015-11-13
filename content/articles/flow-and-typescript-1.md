Title: Flow and TypeScript part 1: Flow
Date: 2015-11-13
Short_summary: Static typing helps keeping codebases (and developers) sane. We have a look on adding types to JavaScript
Category: Dev
Authors: Vincent, Tom


*Reading time: ~10 minutes.*

As front-end applications grow in complexity, more and more developers are looking for ways to make development and maintenance more scalable.
For some people it means foregoing JavaScript itself and using languages such as [Clojurescript](https://github.com/clojure/clojurescript), [Elm](http://elm-lang.org/) or [Purescript](http://www.purescript.org/) while others want to keep using JavaScript, especially now that ES6 makes writing it tolerable.

A simple way to make a codebase easier to maintain and to grow is to have types and that is exactly what [Flow](https://babeljs.io/) and [TypeScript](http://www.typescriptlang.org/) offer, albeit in different ways.
<!-- PELICAN_END_SUMMARY -->

TypeScript is a ES6 transpiler like [Babel](https://babeljs.io/) with types while Flow only does the annotation and static type checking. If you want to use ES6 with Flow, you will need to use Babel as well.

For this series of articles, I am going to convert my [react-example](https://github.com/Keats/react-example) which is a very basic react/redux/react-router Kanban board app to both Flow and TypeScript. Both TypeScript and Flow versions are in the same [repo](https://github.com/Keats/flow-typescript) but only the Flow one is working at the time of writing.

In this part 1, we will look at Flow.

## Installation and usage

It's important to say that Flow doesn't currently work on Windows. You can have a look at [issue #6](https://github.com/facebook/flow/issues/6) on their tracker if you are using Windows. Running it in a [docker image](https://hub.docker.com/r/motiz88/flow/) might work for you though.

For the sake of simplicity I will install the Flow binary with [flow-bin](https://www.npmjs.com/package/flow-bin).instead of using e.g. a gulp plugin (mainly since I couldn't find one).

One nice feature in Flow is that the type checking is opt-in: only the files with the `/* @flow */` comment at the top of a file will be checked. This makes transitioning to Flow extremely easy: you can go one file at a time. Flow also has a `suggest` feature that finds a number of type annotations automatically. `suggest` prints a diff of the type annotations:

```diff
$ flow suggest src/app/store.js
--- old
+++ new
@@ -16,7 +16,7 @@
   router: routerStateReducer,
   ...reducers,
 });
-const middlewares = [thunk];
+const middlewares: Array<{thunk: () => any,}> = [thunk];
```

## An example

Let's start with the [`routes.js`](https://github.com/Keats/flow-typescript/blob/master/flow/src/app/routes.js) files and we get the following error:

```
  5: import { Route, IndexRoute } from "react-router";
                                       ^^^^^^^^^^^^^^ react-router. Required module not found

```
As you can see, Flow doesn't complain about the React import as it comes bundled with an interface file for it.

An interface file is how Flow knows what to expect from an external import, such as react-router.

To fix our error, we need to add an interface file for react-router. The interface file will be empty for now and we tell flow to use the `typings` directory for libraries:

```js
// typings/react-router.js
declare module "react-router" {

}
```

Running Flow again gives us another error:
```
  5: import { Route, IndexRoute } from "react-router";
              ^^^^^ "Route" export of "react-router". Property not found in
  5: import { Route, IndexRoute } from "react-router";
                                       ^^^^^^^^^^^^^^ exports of "react-router"
```

In the `routes.js` file we are importing `Route` from `react-router` but our interface file is completely empty.  We have two possibilities here, either we define `Route` to be `any` (if we are prototyping) or we annotate it properly.

```js
declare module "react-router" {
  declare var Route: any;
}
// or
type RouteProps = {
  component: ReactClass<any, any, any>
};

type LinkProps = {
  to: string
};

declare module "react-router" {
  declare var Route: ReactClass<void, RouteProps, void>;
  declare var IndexRoute: ReactClass<void, RouteProps, void>;
  declare var Link: ReactClass<void, LinkProps, void>;
}
```

Do remember that we just started using Flow so those declarations might be incorrect.

Adding flow to the rest of the files is easy as well, with the occasional 3rd party library interface to write.

Flow has a number of useful features but let's have a look at two in more details:

### Import checking

Importing an unknown property will result in a error, as shown in the following error:

```
src/app/components/DashboardRoute.js:9
  9: import { getAllLists2 } from "../reducers/lists";
              ^^^^^^^^^^^^ "getAllLists2" export of "../reducers/lists". Property not found in
  9: import { getAllLists2 } from "../reducers/lists";
                                  ^^^^^^^^^^^^^^^^^^^ exports of "../reducers/lists"
```

This is preferable over the default Javascript behaviour of assigning `undefined` to variables that aren't found in the imported library.

### Union types

Flow doesn't currently have enums (sum types) but allows some approximation with [disjoint union types](http://flowtype.org/blog/2015/07/03/Disjoint-Unions.html):

```js
type TodoAction = Add | Remove
type Add = { type: 'Add', entry: string }
type Remove = { type: 'Remove', id: number }
```

With this setup flow will complain if 1) the type doesn't match any of the defined types or 2) the structure doesn't match. E.g.

```js
let add: TodoAction = {type: 'Ad', entry: 'get milk'}
```

fails with:

```
 17: let add: TodoAction = {type: 'Ad', entry: 'get milk'}
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ object literal. This type is incompatible with
 17: let add: TodoAction = {type: 'Ad', entry: 'get milk'}
              ^^^^^^^^^^ union type
```

and

```js
let add: TodoAction = {type: 'Add'}
```

will fail with a similar error because the `entry` field is missing:

```
 20: let add: TodoAction = {type: 'Add'}
                           ^^^^^^^^^^^^^ object literal. This type is incompatible with
 20: let add: TodoAction = {type: 'Add'}
              ^^^^^^^^^^ union type
```

Unfortunately this is no true sum type. E.g. the following example will work just fine even though `"omgbug"` is not valid for the `type` field:

```js
function reduce(state: any = {}, action: Action) {
  switch (action.type) {
    case "omgbug":
      return "bug";
  }
}
```

## The state of Flow

Flow type inference is really good and the opt-in aspect makes it really easy to add it to a codebase.

However, there are several points that makes it less nice to use:

- Flow seems to have little traction and a tiny community
    - The evidence is lots of reasonably obvious bugs without activity for months.
    - Some fairly obvious features are missing, e.g. integer keys as in `{1: 2}` are not supported despite showing up in tests a lot ([open issue](https://github.com/facebook/flow/issues/380)).
- No equivalent to [DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped) for Flow which means you would have to write the interface file of every third party library you are using if you want types all the way.
- Non-existent support in tools such as Webpack.
- Low priority project for Facebook from an outsider point of view: ImmutableJS (another Facebook project) for example does not have an official Flow interface file.
- The documentation is somewhat incomplete
- Flow runs a server in the background which needs to be restarted manually, e.g. when adding a new interface file. Forgetting this will lead to some head-scratching error messages.
- Flow is not super compatible with Babel and es6-lint. E.g. `function returns_func(): function` works in Flow but not in Babel because `function` is not a valid annotation in Babel (syntax error).

Now that Flow supports ES6, it's mostly lacking in tooling and documentation.

Writing interface files myself is OK (well maybe not all of [Lodash](https://lodash.com/docs) in one go) but it would be nice to have a good reference on how to write proper interface files, and to have Facebook provide interface files for their own projects.
The only official files we found are part of flow itself: [https://github.com/facebook/flow/blob/master/lib/react.js](https://github.com/facebook/flow/blob/ed8f3d136d3432651fd39544d7ca40244a7423c2/lib/react.js) and hasn't been updated yet to 0.14.


While this conclusion sounds overly critical, we really like the idea behind Flow and hope that its community gets larger. We are on the fence for using Flow in the product we are working on.


We are going to work on the TypeScript article soon and the article should be available in a couple of weeks. In the meantime, if you are using Flow (or used it and gave up), we want your opinions!
