Title: Flow and TypeScript part 2: TypeScript
Date: 2015-11-20
Short_summary: Static typing helps keeping codebases (and developers) sane. We have a look on adding types to JavaScript
Category: Dev
Authors: Vincent, Tom


Continuing from the [first part that introduced Flow](https://blog.wearewizards.io/flow-and-typescript-part-1-flow), we are now going to have a look at [TypeScript](http://www.typescriptlang.org/).

TypeScript is a superset of JavaScript that compiles to several targets, including ES5 and ES6. The current latest version of TypeScript (1.6 at the time of writing) now supports JSX, which was the main blocker for most people using React.

One of the great advantages of TypeScript is  [DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped). This repo contains definition for over a thousand JavaScript packages but more on that later.

Here is the [repo](https://github.com/Keats/flow-typescript/tree/master/typescript). Note that I have used TypeScript for a project before.


## Converting a project to Typescript
Moving a project to TypeScript is not as straightforward as it was for Flow.

There are a couple of steps and gotchas which I will explain on the way.

### Build tools
Obviously you are going to need to change your build tools to use TypeScript rather than what you were using before.
In my case, I was using Webpack so I only had to replace `eslint` with `tslint` and add [ts-loader](https://github.com/TypeStrong/ts-loader) to the mix.

As mentioned in the introduction, TypeScript can target ES5 or ES6. The advantage of targeting ES6 is that you can still use Babel to compile and benefit from hot module reload. For more information on how to do that, please read [ES6 modules with TypeScript and webpack](www.jbrantly.com/es6-modules-with-typescript-and-webpack/) and have a look at the [webpack config](https://github.com/Keats/flow-typescript/blob/master/typescript/webpack.config.js) for a practical example.


## Actual conversion
TypeScript use a config file named `tsconfig.json`. Here's the one currently used by the example:

```ts
{
  "compilerOptions": {
    "target": "es6",
    "jsx": "react",
    "noImplicitAny": true,
    "sourceMap": true
  },
  "exclude": ["node_modules", "gulpfile.js", "webpack.config.js", "server.js"]
}
```
When you are starting the conversion, you want to remove the `"noImplicitAny": true,` line since it would error if you have any missing type annotations.

You then need to rename all your `.js` files to `.ts` and `.tsx`. The `.txs` extension is needed if the file contains JSX.

## Some gotchas and examples
While TypeScript intends to support most of ES6 and ES7 features, you will need to change some bits of your code. Here are the main ones I stumbled into.

### Object destructuring assignment
It doesn't work in TypeScript ([playground](http://www.typescriptlang.org/Playground#src=var%20printer%20%3D%20function%28obj%3A%20Object%29%20{%0A%09console.log%28obj%29%3B%0A}%0A%0Aconst%20hey%20%3D%20{1%3A%20null%2C%202%3A%20null}%3B%0A%0Aprinter%28{%0A%09lol%3A%20null%2C%0A%09...hey%0A}%29%3B)).
Let's look at the `combineReducers` from redux for example:

```js
const reducer = combineReducers({
  router: routerStateReducer,
  ...reducers,
});
// will need to be changed to
const reducer = combineReducers({
  router: routerStateReducer,
  lists: reducers.lists,
  cards: reducers.cards
});
```

### Importing default
Importing the default from a ES6 module is different from the Babel one. For example in the case of React:

```ts
// will not work in typescript
import React from "react";
// will work in typescript
import * as React from "react";
```

### Adding 3rd party definitions
Adding type definitions for your own app is great but if you are using 3rd party libraries without definitions for them It's a bit like giving a mail to a random mail carrier and hoping it was the right one.

Thankfully we have [DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped) to save us. While this doesn't have definitions for every single library you might use, it contains a fair bit.
There is a tool called [tsd](http://definitelytyped.org/tsd/) to manage definitions but frankly, I don't use so many libraries that it's worth the hassle over manually copying files.


### React PropTypes
Now that you have realy typing, you can delete all of those and add interfaces for your components props and state:

```ts
interface IAddFormProps {
  placeholder: string;
  callback: (value: string) => void;
}

export class AddForm extends React.Component<IAddFormProps, {}>{...}
```
Those props will be checked at compile time rather than runtime and will actually prevent the compilation if some are missing.


## Thoughts
This is working really well!

I remember trying TypeScript with [ImmutableJS](http://facebook.github.io/immutable-js/) records months ago and giving up. With a more recent version of TypeScript, we now have both records working (they are used in the example repo if you are curious) and JSX.

Moving to TypeScript is definitely more involved than to Flow where you can easily do file by file. On the other hand, the TypeScript community is much bigger and definitions are widely available and you can integrate the tools directly in your pipeline, as opposed to running Flow outside of it. It also doesn't do much inference compared to Flow.

In terms of IDE support for TypeScript is probably better than Flow (with https://code.visualstudio.com/ for example) but in my PyCharm, both are good.

I think TypeScript is the best bet right now despite believing that the Flow approach is the best one. What is lacking for Flow to catchup is community and tooling.

