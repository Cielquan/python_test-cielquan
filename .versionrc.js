const tracker = {
  filename: 'pyproject.toml',
  updater: require('./updater.js')
}

module.exports = {
  bumpFiles: [tracker],
  packageFiles: [tracker]
}
