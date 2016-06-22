var ExtractTextPlugin = require('extract-text-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var webpack = require('webpack');
var path = require('path');


module.exports = {
  entry: './src/app.js',
    output: {
    path: path.resolve(__dirname + '/build'),
    filename: 'bundle.js'
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'index.tpl.html',
      showErrors: true
    }),
    new ExtractTextPlugin('main.css'),
    new webpack.optimize.UglifyJsPlugin({
      minimize: false,
      compress: {
        warnings: false
      }
    })
  ],
  module: {
    loaders: [
      {
        exclude: /node_modules/,
        loader: 'babel'
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          'style',
          'css!sass'
        )
      },
      {
        test: /\.(png|jpg|gif|ttf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
        exclude: /node_modules/,
        loader: 'file-loader'
      },
      {
        test: /\.html$/,
        exclude: /index\.tpl\.html$/,
        loader: 'html'
      }
    ]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  devServer: {
    historyApiFallback: true,
    contentBase: './'
  }
};
