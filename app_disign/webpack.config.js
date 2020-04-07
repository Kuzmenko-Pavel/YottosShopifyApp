const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development', //'production',
    entry: {
        index: './src/index.js',
        index2: './src/index.js',
        index3: './src/index.js',
        unsub: './src/index.js'
    },
    optimization: {
        minimize: true,
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/](react|react-dom|axios|react-transition-group)[\\/]/,
                    name: 'react',
                    chunks: 'all'
                },
                shopify: {
                    test: /[\\/]node_modules[\\/]@shopify[\\/](app-bridge|polaris|polaris-icons)[\\/]/,
                    name: 'polaris',
                    chunks: 'all'
                }
            }
        }
    },
    output: {
        path: path.resolve(__dirname, 'build'),
        filename: '[name].app.js'
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: './public/index.html',
            chunks: [
                'index',
                'react',
                'polaris'
            ]
        }),
        new HtmlWebpackPlugin({
            filename: 'index2.html',
            template: './public/index2.html',
            chunks: [
                'index',
                'react',
                'polaris'
            ]
        }),
        new HtmlWebpackPlugin({
            filename: 'index3.html',
            template: './public/index3.html',
            chunks: [
                'index',
                'react',
                'polaris'
            ]
        }),
        new HtmlWebpackPlugin({
            filename: 'unsub.html',
            template: './public/unsub.html',
            chunks: [
                'index',
                'react',
                'polaris'
            ]
        })
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                include: path.resolve(__dirname, 'src'),
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
    },
    devServer: {
        https: true,
        compress: true,
        disableHostCheck: true,
        host: '0.0.0.0',
        port: 8000
    }
};
