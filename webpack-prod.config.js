var config        = require("./webpack.config.js");
var BundleTracker = require("webpack-bundle-tracker");

config.output.path = require("path").resolve("./frontend/dist");
config.plugins = [
    new BundleTracker({filename: "./webpack-stats-prod.json"})
]
module.exports = config;
