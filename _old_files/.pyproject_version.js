const toml = require("@iarna/toml");

module.exports.readVersion = function (contents) {
  return toml.parse(contents).tool.poetry.version;
};

module.exports.writeVersion = function (contents, version) {
  const poetry_pattern = /\s*\[tool.poetry\]/i;
  const section_pattern = /\s*\[[0-9a-z.]+\]/i;
  const version_pattern = /\s*version\s*=\s*"[0-9a-z.-]*"/i;
  var updated_version = false;
  found_poetry = false;
  var pyproject = contents.split("\n");
  for (var i = 0; i < pyproject.length; i++) {
    if (found_poetry === false) {
      if (pyproject[i].search(poetry_pattern) != -1) {
        var found_poetry = true;
        continue;
      }
    } else if (pyproject[i].search(section_pattern) != -1) {
      throw "No version found in [tool.poetry] section.";
    } else {
      if (pyproject[i].search(version_pattern) != -1) {
        pyproject[i] = pyproject[i].replace(
          /"[0-9a-z.-]*"/i,
          '"' + version + '"'
        );
        var updated_version = true;
        break;
      }
    }
  }
  if (updated_version === false) {
    if (found_poetry === false) {
      throw "No [tool.poetry] section found.";
    } else {
      throw "No 'version' found in [tool.poetry] section.";
    }
  }
  return pyproject.join("\n");
};
