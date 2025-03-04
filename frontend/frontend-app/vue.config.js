const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? '/curtain-samples/'  // 替换成您的 GitHub 仓库名
    : '/',
  outputDir: 'docs',  // GitHub Pages 可以使用 /docs 目录
  configureWebpack: {
    entry: './src/main.mjs'
  }
})
