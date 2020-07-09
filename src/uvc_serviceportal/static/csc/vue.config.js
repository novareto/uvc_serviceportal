// vue.config.js
module.exports = {
    filenameHashing: false,
    runtimeCompiler: true,
    outputDir: '../vuedist'
}

chainWebpack: config => {
  config.optimization.delete('splitChunks')
}
