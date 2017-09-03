var gulp = require('gulp'),
    watch = require('gulp-watch'),
    responsive = require('gulp-responsive');


var config = {
      '*': [{
        width: 600,
        rename: { suffix: '-m' },
      }, {
        width: 300,
        rename: { suffix: '-s' },
      }, {
        width: 1200,
        rename: { suffix: '-2x' },
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
