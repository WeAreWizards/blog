Title: Migrating to gulp 4 by example
Date: 2015-03-13
Short_summary: showing how to migrate to gulp 4 by example
Category: Dev
Authors: Vincent

*Reading time: ~20 minutes.*

Last year I wrote a blog post on my personal website (you can see it here [Gulp by example ](http://vincent.is/introducing-people-to-gulp/)) showing what [gulp](http://gulpjs.com/) was and making a demo project using it.
Since then, the team behind it did a lot of work on v4 of gulp which, while not released as of the writing of the post, is stable enough to be used.  

Rather than going through a list of new features, let's update my [angular boilerplate](https://github.com/Keats/ng-boilerplate) to use gulp4.

You can have a look at the [Goal section of the README](https://github.com/Keats/ng-boilerplate#goal) to know what this boilerplate does but for those not wanting to open the link: Typescript, Sass, automatic DI, template preloading, testing with Karma and Protractor, live reload with browser-sync.
> Note: I'm not using this boilerplate personally anymore since I don't really do vanilla angular anymore.

Here's the [starting commit](https://github.com/Keats/ng-boilerplate/tree/87e75551651e94dfc1aa6135e1ea7cb5bd61cf0f).

## Updating dependencies
Nothing fancy here, just updating our npm and bower dependencies, including pointing to the gulp4 branch on github. To use npm install from a github repo, you can use:
```
$ npm install --save-dev gulpjs/gulp.git#4.0
```
The boilerplate demo tests are going to fail at that point because of changes in the api of gulp and probably some in other libraries we just updated as well.  

You can see the commit [here](https://github.com/Keats/ng-boilerplate/commit/49a339cc5cbde8f5374b8f4c915a548dc2916cc4).

## Migrating the gulpfile
### Calling gulp
The first thing we need to do is ensure that we are using the right version of gulp.  You might have another version installed globally or nothing installed globally like me.  
The easiest way (at least to me) to deal with that issue is the [npm scripts](https://docs.npmjs.com/misc/scripts) part of the package.json.

```js
// package.json
"scripts": {
  "gulp": "./node_modules/gulp/bin/gulp.js"
},

// in your terminal, instead of using gulp, use npm run gulp
npm run gulp
```

The downside is that you will get npm errors instead of the regular ones but that's only an issue when building your gulpfile.
Let's not forget to update the travis.yml to use that npm script too.  

You can see the commit [here](https://github.com/Keats/ng-boilerplate/commit/ef30315f43580e8b3c1ba85d4536c7fe0d69365d).

### Fixing the errors we're getting
If you run the gulpfile locally or look at the [travis build](https://travis-ci.org/Keats/ng-boilerplate/builds/54252789), you will notice we get the following error:
```bash
assert.js:87
  throw new assert.AssertionError({
        ^
AssertionError: Task function must be specified
    at Gulp.set (/home/vincent/Code/ng-boilerplate/node_modules/gulp/node_modules/undertaker/lib/set.js:14:3)
    at Gulp.task (/home/vincent/Code/ng-boilerplate/node_modules/gulp/node_modules/undertaker/lib/task.js:14:8)
....
```
This comes from the fact that gulp.task changed and the 3 parameters signature was removed.
In short, tasks that look like the one below will need to be changed to remove the `[]` parameter:
```js
gulp.task('default', ['build'], function () {
  return runSequence(['watch', 'karma-watch']);
});
```
To give a quick background to people not familiar with gulp, the list parameter is a list of tasks that need to be run before running that task.
In this case it will call the build task before running watch and karma-watch in order (runSequence is another thing that can be changed but we will get back to that later).
To solve that very common issue of task dependencies, two methods were added:

- `gulp.series`: will run the tasks in order
- `gulp.parallel`: will run the tasks in parallel

Let's fix our error by replacing those dependent tasks, for example for the default task:

```js
gulp.task(
  'default',
  gulp.series('build', gulp.parallel('browser-sync', 'watch', 'karma-watch'))
);
```

In that case we first want to run build, and then browser-sync, watch and karma-watch in parallel. 
If you look at the commit below, you will be able to spot an easy mistake: browser-sync is in the `gulp.series` despite being blocking. In short, don't put blocking tasks in a series.  

Now trying to run the build task, I get another error:

```js
[15:09:07] TypeError: undefined is not a function
    at /home/vincent/Code/ng-boilerplate/node_modules/run-sequence/index.js:18:22
    at Array.forEach (native)
    at verifyTaskSets (/home/vincent/Code/ng-boilerplate/node_modules/run-sequence/index.js:12:11)
```

Since gulp 4 has a method to run things sequentially, let's use it.

```js
// before
gulp.task('build', function(){
  return runSequence(
    'clean',
    ['sass', 'copy-assets', 'ts-compile', 'templates', 'copy-vendor'],
    'index'
  );
)};

// after
gulp.task(
  'build',
  gulp.series(
    'clean',
    gulp.parallel('sass', 'copy-assets', 'ts-compile', 'templates', 'copy-vendor'),
    'index'
  )
);
```

> Note: I had to modify some tasks like the browser-sync since its API changed.
I also had to make a [patch](https://github.com/dlmanning/gulp-sass/pull/207) to gulp-sass to update the node-sass version.  

You can see the commit [here](https://github.com/Keats/ng-boilerplate/commit/91a05401c6ea532467bc00b5a6e54fd95b6b0eaf).  

Looking at the [build](https://travis-ci.org/Keats/ng-boilerplate/builds/54274589), it still fails because of a missing selenium jar which means a protractor error.
My elegant solution was the [following](https://github.com/Keats/ng-boilerplate/commit/d999db2442ac72fc440e8ff9cccd8348c533c72d), as in removing protractor from travis because I'm not using it right now anyway.

### Small cleanup
The following is not strictly related to gulp4 but contains some of the things I like to do to have a clean gulpfile.
The config part at the top of the gulpfile (where I am defining all the paths to inject) is quite ugly but I am not going to touch it here, only change the gulp related things.

First thing, [gulp-load-plugins](https://www.npmjs.com/package/gulp-load-plugins) makes things quite simple but the prefix I had chosen, 'plugins', is quite verbose and takes up space. Recently I've started using `$` which works quite well.
Something that took me way too long to realise is that it auto-camelCases packages names with dash so my following line was useless:

```js
plugins.ngAnnotate = require('gulp-ng-annotate');
```

Another thing to examine is whether some of the gulp plugins you're using actually bring any values compared to using the actual npm module directly.
In my boilerplate, gulp-karma is not doing anything special and was only necessary while the karma team was fixing some of the issues the plugin was solving.

While going through the file, I also realised I didn't test the watch process at all and that it didn't work (surprising eh).  

The fix was easy and I included it in the [clean up commit](https://github.com/Keats/ng-boilerplate/commit/bee9fba6e9ee2602e96c8d735d409b31a267d655).

Lastly, I have seen quite a few people dividing their tasks in individual files but that seems like an excessive measure to me.
Maybe it makes more sense if you have very long files but all of mine are between 50 and 200 lines (this one is actually my longest) so I never felt the need.


## Wrap up
Some functions from gulp 3 such a `gulp.start` and `gulp.run` were deprecated and are not covered in this article since I never used them in any of my gulpfiles.  

There is also a bunch of new functions that I haven't used yet. To have a complete overview of what's new, you can check the [gulp 4 changelog](https://github.com/gulpjs/gulp/blob/4.0/CHANGELOG.md).
Gulp 4 is still in alpha so I'll update this article if any breaking change happens.  

A question often asked is why use gulp when you have things like [webpack](http://webpack.github.io/) around but that's out of scope for this article but will probably be part of another one.

