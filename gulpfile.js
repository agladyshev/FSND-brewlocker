var gulp = require('gulp'),
    watch = require('gulp-watch'),
    responsive = require('gulp-responsive');

gulp.task('images', function () {
  return gulp.src('uploads/images/*.{jpg, png, webp, gif}')
    .pipe(responsive({
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
    }, {
      // Global configuration for all images
      // The output quality for JPEG, WebP and TIFF output formats
      errorOnEnlargement: false,
      quality: 70,
      // Use progressive (interlace) scan for JPEG and PNG output
      progressive: true,
      // Zlib compression level of PNG output format
      compressionLevel: 6,
      // Strip all metadata
      withMetadata: false

    }))
    .pipe(gulp.dest('uploads/images/responsive'));
});


// gulp.task('default', gulp.series('images', function () {
//     // Endless stream mode 
//     return watch(['uploads', '/uploads/**/*'], { ignoreInitial: false })
//         .pipe(gulp.dest('images'));
// }));

gulp.task('default', ['images'])