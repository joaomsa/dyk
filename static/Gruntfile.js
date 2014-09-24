module.exports = function(grunt) {
    "use strict";

    grunt.initConfig({
        paths: {
            "less": "style/less",
            "css": "style/css"
        },

        less: {
            development: {
                files: {
                    "<%= paths.css %>/style.css": "<%= paths.less %>/style.less"
                }
            }
        },

        watch: {
            style: {
                files: [
                    "<%= paths.less %>/*.less"
                ],
                tasks: ["less"]
            }
        }
    });

    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.registerTask("default", ["watch"]);
}
