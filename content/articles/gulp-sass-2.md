Title: gulp-sass v2 released
Date: 2015-05-07
Short_summary: Showing what's new in gulp-sass v2
Category: Dev
Authors: Vincent

*Reading time: ~15 minutes.*


[gulp-sass](https://github.com/dlmanning/gulp-sass) v2 was released today!  
In itself, this is not a big change as this is simply a wrapper for node-sass which uses libsass so, while this version is a complete rewrite this is not the important news. The important news is that it ships with [node-sass](https://github.com/sass/node-sass) v3 which is using [libsass](http://libsass.org/) 3.2.2.
<!-- PELICAN_END_SUMMARY -->

We will see in a short moment why it is exciting but first a small explanation on what is sass and libsass.  

**TL;DR**:
```bash
$ rm -rf node_modules/gulp-sass/
$ npm install gulp-sass --save-dev
// enjoy nearly full sass compatibility
```

## Sass
Nowadays, most front-end developers and designers use CSS preprocessors to immensely simplify their work.  
A CSS preprocessor brings variables, nesting, mixins, functions and other things to CSS.  Let's see a short example of why we would use one, in this case using variables for colours:

```css
.header {
  background: #484c55;
}

.header .title {
  background: #5a5d66; /* 10% lighter than #484c55 */
}

.header .title .logo {
  background: #484c55;
}
```

And in Sass:
```sass
// functions.scss
/// Slightly lighten a color
@function tint($color, $percentage) {
  @return mix(white, $color, $percentage);
}

// colors.scss
@import "functions";

$header-background: #484c55;
$header-title-background: tint($header-background, 10%);

// header.scss
@import "colors";

.header {
  background: $header-background;

  .title {
    background: $header-title-background;

    .logo {
      background: $header-background;
    }
  }
}
```

> The above ignores best practices about naming/nesting/specificity of selectors for the sake of example.

While the Sass version is longer, it makes your CSS more readable, easy to organise and consistent. This is only a tiny part of what CSS preprocessors but it hopefully gives you an idea on why they are extremely useful.  

[Sass](http://sass-lang.com/) is one of them. There is also [less](http://lesscss.org/), [stylus](http://learnboost.github.io/stylus/) and a few others but I personally use Sass so I will be talking about that.  

Sass is written in Ruby, which means that Ruby is now needed to build your frontend. Ruby is also not the fastest programming language around and the compilation was taking more than 10 seconds for some large projects, which is not really sustainable when working.  

## Here comes a new challenger
[Aaron Leung](https://github.com/akhleung) started porting the Sass compiler to C/C++.  
Lots of people (including me) started playing with it and were impressed by the compilation time an order of magnitude faster than sass but quickly realized that lots of features were not implemented yet, for example [this article](http://benfrain.com/libsass-lightning-fast-sass-compiler-ready-prime-time/). While it was usable for some projects, it could not be a drop-in replacement for most people as you would have to use workarounds for some features and not use some others at all or were using frameworks like Bourbon or earlier versions of Foundation.

[Hugo Giraudel](https://twitter.com/HugoGiraudel) started a website called [Sass Compatibility](http://sass-compatibility.github.io/) to keep track of those incompatibilities.  
As mentioned in the introduction, gulp-sass is now using libsass 3.2.2 while it was using 2.0 before and the results of that website look pretty damn good !  
Most features are supported except for selector manipulation and string functions, both of which I didn't even know existed in the first place.  

## gulp-sass
As mentioned in the introduction, gulp-sass has been rewritten and it means that your existing tasks won't work.  
Here's how to update your gulpfile (from the README):

```javascript
// gulp-sass 1.3.3 task
gulp.task('sass', function () {
    gulp.src('./scss/*.scss')
        .pipe(sass({errLogToConsole: true}))
        .pipe(gulp.dest('./css'));
});

// gulp-sass 2.0 task
gulp.task('sass', function () {
    gulp.src('./scss/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(plugins.autoprefixer())
        .pipe(gulp.dest('./css'));
});

// gulp-sass 2.0 synchronous compilation task
gulp.task('sass', function () {
    gulp.src('./scss/*.scss')
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(plugins.autoprefixer())
        .pipe(gulp.dest('./css'));
});
```

Any options passed to gulp-sass will be passed down to node-sass, there is no gulp-sass specific options.  

As a general advice, I would recommend using [gulp-autoprefixer](https://github.com/sindresorhus/gulp-autoprefixer) along as it simplifies your Sass even more since you don't have to worry about browsers prefixes and flexbox syntaxes.  

There are already issues open on gulp-sass but if you encounter problems (except installations errors, those are most likely node-sass), please open an issue on [https://github.com/dlmanning/gulp-sass/issues](https://github.com/dlmanning/gulp-sass/issues) so we can have a look !  
There was over 45k downloads of gulp-sass on npm last week so spread the word about that new version and it might be a good time to try replacing your Ruby Sass!  

As an aside, if you are writing Sass I heavily recommend reading those [guidelines](http://sass-guidelin.es/) as they are really good and well detailed.  
The only thing missing for me now in the Sass ecosystem is a Ruby-free linter (sounds like a fun Rust learning project).  
