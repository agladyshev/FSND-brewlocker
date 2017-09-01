var gulp = require('gulp'),
    watch = require('gulp-watch'),
    del = require('del'),
    responsive = require('gulp-responsive'),
    runSequence = require('run-sequence');


var config = {
      // Resize all images to 100 pixels wide and add suffix -thumbnail
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
    }


var global = {
      // Global configuration for all images
      // The output quality for JPEG, WebP and TIFF output formats
      errorOnEnlargement: false,
      quality: 70,
      // Use progressive (interlace) scan for JPEG and PNG output
      progressive: true,
      // Zlib compression level of PNG output format
      compressionLevel: 6,
      // Strip all metadata
      withMetadata: false,
    }


gulp.task('images', function () {
  return gulp.src('uploads/images/*')
    .pipe(responsive(config, global))
    .pipe(gulp.dest('uploads/images/responsive'));
});


// gulp.task('clean:uploads', function () {
//   return del([
//     'uploads/images/img_temp/*',
//   ]);
// });


gulp.task('stream', function () {
    // Endless stream mode 
    return watch('uploads/images/*', { ignoreInitial: true })
        .pipe(responsive(config, global))
        .pipe(gulp.dest('uploads/images/responsive'));
    });


gulp.task('build', ['images'])

gulp.task('default', ['stream'])