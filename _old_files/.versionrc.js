const tracker = {
  filename: "pyproject.toml",
  updater: require("./.pyproject_version.js"),
};

module.exports = {
  bumpFiles: [tracker],
  packageFiles: [tracker],
  header: "# Change Log\n\n",
  types: [
    { type: "feat", section: "Features" },
    { type: "fix", section: "Bug Fixes" },
    { type: "docs", section: "Documentation" },
    { type: "chore", hidden: true },
    { type: "style", hidden: true },
    { type: "refactor", hidden: true },
    { type: "perf", hidden: true },
    { type: "test", hidden: true },
    { type: "build", hidden: true },
    { type: "ci", hidden: true },
    { type: "revert", hidden: true },
  ],
  releaseCommitMessageFormat: "chore(release): {{currentTag}} [skip ci]",
};
