const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './react-frontend-dev/app.js',
    output: {
        path       : __dirname + '/react-frontend-public/static/build/',
        filename   : 'main.js',
        publicPath : 'static/build/'
    },
    module: {
        loaders: [
            { test: /\.css$/, loader: 'style-loader!css-loader!autoprefixer-loader' },
            { test: /\.scss$/, loader: 'style-loader!css-loader!autoprefixer-loader!sass-loader' },
            { test: /\.gif$/, loader: 'url-loader?limit=10000&mimetype=image/gif' },
            { test: /\.jpg$/, loader: 'url-loader?limit=10000&mimetype=image/jpg' },
            { test: /\.png$/, loader: 'url-loader?limit=10000&mimetype=image/png' },
            { test: /\.svg/, loader: 'url-loader?limit=26000&mimetype=image/svg+xml' },
            { test: /\.(woff|woff2|ttf|eot)/, loader: 'url-loader?limit=1' },

            { test: /\.jsx$/, loader: 'react-hot!babel', exclude: [/node_modules/, /react-frontend-public/] },
            { test: /\.js$/, loader: 'babel', exclude: [/node_modules/, /react-frontend-public/] },

            { test: /\.json$/, loader: 'json-loader'}
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: '../../index.html',
            template: 'react-frontend-dev/index.html'
        })
    ],
    eslint: {
        configFile: '.eslintrc'
    }
};
