var path          = require("path")
var BundleTracker = require("webpack-bundle-tracker")
var config        = require("./webpack.config.js")

config.output.path = path.resolve("./frontend/dist/")

config.plugins = [
    new BundleTracker({filename: "./webpack-stats-prod.json"}),
]

module.exports = config
