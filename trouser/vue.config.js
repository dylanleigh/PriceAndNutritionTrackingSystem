const path = require("path");

//vue.config.js
module.exports = {
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = "Trouser - What goes over Pants";
                return args;
            })
    },
    // Configure how the public path when building for production
    // Normally you can run this application using npm's built in server (npm serve), but if you instead use
    // npm run build -- --mode staging
    // Then the .env.staging file for environment variables will be loaded
    publicPath: process.env.VUE_APP_STATIC_URL,
    // The output will go to the django app folder always
    outputDir: path.resolve(__dirname, "..","pants","frontend","static", "frontend"),
    indexPath: path.resolve(__dirname, "..","pants","frontend","templates", "frontend", "index.html"),
}