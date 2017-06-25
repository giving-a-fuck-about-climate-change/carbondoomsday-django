var path = require("path")
var webpack = require("webpack")
var BundleTracker = require("webpack-bundle-tracker")

module.exports = {
  context: __dirname,

  entry: "./frontend/js/index",

  output: {
      path: path.resolve("./frontend/bundles/"),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: "./webpack-stats.json"}),
  ],

  module: {
    loaders: [
      { test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        query:
        {
          presets: ["es2015", "react"]
        }
      },
    ],
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".jsx"]
  },
}
