var WebpackStripLoader = require("strip-loader");
var devConfig = require("./webpack.config.js");

// Remove console.log request from production code
var stripLoader = {
    test: ["/\.js$/", "/\.es6$/"],
    exclude: "/node_modules/",
    loader: WebpackStripLoader.loader("console.log")
};
devConfig.module.loaders.push(stripLoader);

// We don't want to inline source maps in production
devConfig.devtool = "source-map";

module.exports = devConfig;
