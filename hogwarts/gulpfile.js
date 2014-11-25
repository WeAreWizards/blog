var gulp = require('gulp');
var sass = require('gulp-sass');
var prefix = require('gulp-autoprefixer');

var sassFiles = ['./scss/*.scss'];

gulp.task('sass', function() {
    gulp.src(sassFiles)
        .pipe(sass({outputStyle: 'compressed', errLogToConsole: true}))
        .pipe(prefix())  // defauls to > 1%, last 2 versions, Firefox ESR, Opera 12.1
        .pipe(gulp.dest('./static/css'));
});

gulp.task('watch', ['sass'], function () {
    gulp.watch(sassFiles, ['sass']);
});
