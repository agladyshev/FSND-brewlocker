var gulp = require('gulp'),
    watch = require('gulp-watch'),
    responsive = require('gulp-responsive');


var config = {
      '*': [{
        width: 600,
        rename: { suffix: '-600' },
      }, {
        width: 300,
        rename: { suffix: '-300' },
      }, {
        width: 1200,
        rename: { suffix: '-1200' },
      }]
    };


var global = {
      errorOnEnlargement: false,
      quality: 80,
      progressive: true,
      compressionLevel: 6,
      withMetadata: false,
    };


gulp.task('images', function () {
  return gulp.src('uploads/images/*')
    .pipe(responsive(config, global))
    .pipe(gulp.dest('uploads/images/responsive'));
});


gulp.task('stream', function () {
    return watch('uploads/images/*', { ignoreInitial: true })
        .pipe(responsive(config, global))
        .pipe(gulp.dest('uploads/images/responsive'));
    });


gulp.task('build', ['images']);
gulp.task('default', ['stream']);
