module.exports = function (grunt) {
    var path = require("path");

    // Load NPM tasks
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks("grunt-bower-install-simple");

    // Init GRUNT configuraton
    grunt.initConfig({
        'bower-install-simple': {
            options: {
                color:       true,
                production:  false,
                directory:   "theme/vendors"
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
};
