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
                directory:   "localtheme/vendors"
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
                    "localtheme/assets/style.css": "localtheme/stylesheets/website.less",
                    "localtheme/assets/print.css": "localtheme/stylesheets/ebook.less"
                }
            }
        },
        copy: {
            vendors: {
                files: [
                    {
                        expand: true,
                        cwd: 'localtheme/vendors/fontawesome/fonts/',
                        src: ['**'],
                        dest: 'localtheme/assets/fonts/fontawesome/',
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
