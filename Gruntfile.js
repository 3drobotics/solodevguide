module.exports = function (grunt) {
  var path = require("path");

  // Load NPM tasks
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks("grunt-bower-install-simple");
  grunt.loadNpmTasks('grunt-link-checker');
  grunt.loadNpmTasks('grunt-gitbook');
  grunt.loadNpmTasks('grunt-http-server');

  // Init GRUNT configuraton
  grunt.initConfig({
    'bower-install-simple': {
      options: {
        color:       true,
        production:  false,
        directory:   "theme/vendors"
      }
    },
    'http-server': {
      'check': {
        root: 'book/_book',
        port: '4000',
        runInBackground: true,
      },
      'dev': {
        root: 'book/_book',
        port: '4000',
      },
    },
    linkChecker: {
      gitbook: {
        site: 'localhost',
        options: {
          maxConcurrency: 20,
          initialPort: 4000,
          supportedMimeTypes: [/html/i],
        }
      }
    },
    less: {
      development: {
        options: {
          compress: true,
          yuicompress: true,
          optimization: 2
        },
        files: {
          "theme/assets/style.css": "theme/stylesheets/website.less",
          "theme/assets/print.css": "theme/stylesheets/ebook.less"
        }
      }
    },
    copy: {
      vendors: {
        files: [
          {
            expand: true,
            cwd: 'theme/vendors/fontawesome/fonts/',
            src: ['**'],
            dest: 'theme/assets/fonts/fontawesome/',
            filter: 'isFile'
          }
        ]
      }
    }
  });

  grunt.registerTask("bower-install", [ "bower-install-simple" ]);

  // Build
  grunt.registerTask('build', [
    'bower-install',
    'less'
  ]);

  grunt.registerTask('default', [
    'build'
  ]);

  grunt.registerTask('gitbook', 'Runs gitbook.', function (mode) {
    var done = this.async();
    var spawn = require('child_process').spawn;
    var p = spawn('gitbook', ['build', 'book'], {
      cwd: __dirname
    });
    p.stdout.pipe(process.stdout);
    p.stderr.pipe(process.stderr);
    p.on('exit', function (code) {
      if (!code) {
        done();
      } else {
        throw new Error('Non-zero exit code from gitbook: ' + String(code));
      }
    });
  });

  // Create Default Task
  grunt.registerTask('check', [
    'gitbook',
    'http-server:check',
    'linkChecker',
  ]);

  // Create Default Task
  grunt.registerTask('dev', [
    'gitbook',
    'http-server:dev',
  ]);
};
