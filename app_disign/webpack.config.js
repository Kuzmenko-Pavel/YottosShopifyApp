const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
    mode: 'production', //'development',
    entry: {
        index: './src/index.js',
        // index2: './src/index.js',
        // index3: './src/index.js',
        unsub: './src/unsub.js',
        fb_integration: './src/fb_integration.js'
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserJSPlugin({}),
            new OptimizeCSSAssetsPlugin({})
        ],
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/](react|react-dom|axios|react-transition-group|react-youtube|react-cookies)[\\/]/,
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
        new MiniCssExtractPlugin(),
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
            filename: 'fb_integration.html',
            template: './public/fb_integration.html',
            chunks: [
                'fb_integration',
                'react',
                'polaris'
            ]
        }),
        // new HtmlWebpackPlugin({
        //     filename: 'index2.html',
        //     template: './public/index2.html',
        //     chunks: [
        //         'index',
        //         'react',
        //         'polaris'
        //     ]
        // }),
        // new HtmlWebpackPlugin({
        //     filename: 'index3.html',
        //     template: './public/index3.html',
        //     chunks: [
        //         'index',
        //         'react',
        //         'polaris'
        //     ]
        // }),
        new HtmlWebpackPlugin({
            filename: 'unsub.html',
            template: './public/unsub.html',
            chunks: [
                'unsub',
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
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            }
        ]
    },
    devServer: {
        https: true,
        compress: true,
        disableHostCheck: true,
        host: 'localhost',
        port: 8000
    }
};
