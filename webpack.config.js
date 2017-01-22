//require our dependencies
var path = require("path")
var webpack = require("webpack")
var BundleTracker = require("webpack-bundle-tracker")

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    entry: "./namubufferiapp/assets/js/index", 
    devtool: "inline-source-map",

    output: {
        path: path.resolve("./namubufferiapp/static/bundles/"),
        publicPath: "/static/bundles/",
        filename: "[name]-[hash].js", 
        sourceMapFilename: "[name].map.js",
    },

    plugins: [
        new BundleTracker({filename: "./webpack-stats.json"}), 
        //makes jQuery available in every module
        new webpack.ProvidePlugin({ 
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery' 
        })
    ],

    resolve: {
        modulesDirectories: ["node_modules"],
        extensions: ["", ".js", ".jsx"] 
    },

	module: {
		loaders: [
			{ test: /\.(woff|woff2)$/,  loader: "url-loader?limit=10000&mimetype=application/font-woff" },
			{ test: /\.ttf$/,    loader: "file-loader" },
			{ test: /\.eot$/,    loader: "file-loader" },
			{ test: /\.svg$/,    loader: "file-loader" },
            { test: /\.css$/,    loader: "style-loader!css-loader" }
		]
	},

};
