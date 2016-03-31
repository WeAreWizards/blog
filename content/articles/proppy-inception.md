Title: How Proppy is made and its inception
Date: 2016-03-31
Short_summary: Looking at history and stack behind proppy.io
Category: Dev, Product
Authors: Vincent


*Reading time: ~5min*

We released [Proppy](https://proppy.io/) in beta last week.
Since this blog has a mostly technical following, I thought it would be interested in details about the stack and the data model.
<!-- PELICAN_END_SUMMARY -->

As mentioned in the last article, Proppy is originally a CLI tool written in Python available at [https://github.com/WeAreWizards/proppy](https://github.com/WeAreWizards/proppy). It generates PDFs from a TOML configuration file and warns when it thinks it found an error such as a missing field or a 100% discount.

While this works great for small projects, the output doesn't look super professional and is certainly not pretty. CLI is also definitely not usable by non-tech people. Hence the decision to start a web tool to provide similar features to everyone.

Let's have a look at the stack used and how it was chosen.

## Backend
The backend started in Go and while the dev environment was very pleasant (thanks to [GoConvey](http://goconvey.co/)), the language itself was quite verbose for a CRUD app using SQL, even with [sqlx](https://github.com/jmoiron/sqlx). So many `if err != nil...`

We then decided to move to Flask and, while we lose the type safety, it is much faster to develop in. SQLAlchemy is also a very nice ORM that makes most of our (simple) interactions with Postgres a breeze.

As you can see, the backend is pretty normal: nothing special about it and it works. It's probably webscale too.

## Frontend
The frontend has ironically seen more changes than the backend, despite the backend having changed languages halfway through.

The first version of the frontend only contained the editor to familiarise myself with the mess that is `contenteditable` and try to figure out a good data model and interactions for the features we wanted such as sections import, comments and sections re-ordering.

After a few iterations, here's a quick description of the model we ended up choosing.  

> A proposal is composed of `blocks` which can be of different types such as `section`, `paragraph`, `image`, etc.. 

> A section is a specific kind of block as blocks can be nested under it and it is possible to import them from other proposals to keeps things DRY.

The block system makes things like comments very easy but things like `CTRL+a` doesn't work as people might think.

From the start, Proppy was a ES6 React app using Webpack, Babel and Sass. I would have used TypeScript right away but JSX support was not present at the time. After a while, we realised that lots of time was wasted on typos, incorrect imports or general refactoring and we decided that adding some types would help. 


We used TypeScript for a client before with good success and Flow was getting more popular at the same time. We tried both on a pet project as well as on our codebase and wrote about it ([https://blog.wearewizards.io/flow-and-typescript-part-1-flow](https://blog.wearewizards.io/flow-and-typescript-part-1-flow) and [https://blog.wearewizards.io/flow-and-typescript-part-2-typescript](https://blog.wearewizards.io/flow-and-typescript-part-2-typescript)). Ultimately we chose TypeScript as the community was bigger, tooling was better and it revealed a few bugs in our codebase right from the start.


When it came to choosing a state management library, the Great Flux War was raging on at and left me in much confusion: Vanilla fhttp://mobxjs.github.io/mobx/lux, alt, Reflux and new Flux implementations pretty much everyday. Eventually I've heard of this one implementation that was inspired from Elm called Redux and went along with it which has been a pretty good choice so far!
If I had to start another project now, I would have a close look at [MobX](http://mobxjs.github.io/mobx/) first instead.

## Deployment
As for all our projects, we use [Nix](https://nixos.org/nix/) and [NixOps](https://nixos.org/nixops/) for dependencies and deployment. 

Npm is still used for JavaScript dependencies as it doesn't work very well with Nix but the packages are cached by Nix.

## Conclusion
Overall, the frontend bit still seems unsatisfactory due to having to cobble so many packages to get a half-decent language. 

Hopefully WebAssembly will be ready and usable  as a replacement for JavaScript — DOM support and everything — soon since I don't expect JavaScript to get any groundbreaking changes supported by the majority of browsers anytime soon.
