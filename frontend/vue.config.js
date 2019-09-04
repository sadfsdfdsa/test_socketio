const WebpackShellPlugin = require('webpack-shell-plugin');

module.exports = {
    assetsDir: '',
    productionSourceMap: false,
    devServer: {
        proxy: {
            '^/api/*': {
                // proxies request for api to localhost:80
                target: "http://localhost:5000/"
            },
        }
    },
    configureWebpack: {
        plugins: [
            new WebpackShellPlugin({
                onBuildStart: ['echo Copy'],
                //onBuildEnd: ['cp ../static/index.html ../templates/index.html']
            })
        ],
    },
};