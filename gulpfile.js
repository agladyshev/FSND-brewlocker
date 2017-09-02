var gulp = require('gulp'),
    watch = require('gulp-watch'),
    responsive = require('gulp-responsive'),
    exec = require('gulp-exec');


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


// '. env/bin/activate && python manage.py runserver'


gulp.task('build', ['images']);
gulp.task('default', ['stream']);


// gulp.task('reset', function() {
//   var options = {
//     continueOnError: false, // default = false, true means don't emit error event 
//     pipeStdout: false, // default = false, true means stdout is written to file.contents 
//     customTemplatingThing: 'test' // content passed to gutil.template() 
//   };
//   var reportOptions = {
//     err: true, // default = true, false means don't write err 
//     stderr: true, // default = true, false means don't write stderr 
//     stdout: true // default = true, false means don't write stdout 
//   }
//   return gulp.src('**/*')
//     .pipe(exec('source env/bin/activate && python manage.py runserver', options))
//     .pipe(exec.reporter(reportOptions));
// });