const {join} = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'production',
    entry: {
        index: join(__dirname, 'src/index.js'),
        // billing: join(__dirname, 'src/billing.js')
    },
    optimization: {
        minimize: true
      },
    output: {
        path: join(__dirname, 'build'),
        filename: '[name].bundle.js'
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: './public/index.html',
            chunks: ['index'],
        }),
        // new HtmlWebpackPlugin({
        //     filename: 'billing.html',
        //     template: './public/billing.html',
        //     chunks: ['billing'],
        // })
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                include: join(__dirname, 'src'),
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            babelrc: false,
                            presets: [
                                '@babel/env',
                                '@babel/react'
                            ]
                        }
                    }
                ]
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    }
};
