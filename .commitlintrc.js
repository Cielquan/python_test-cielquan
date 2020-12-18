// https://github.com/conventional-changelog/commitlint/blob/master/docs/reference-rules.md
module.exports = {
	parserPreset: 'conventional-changelog-conventionalcommits',
	rules: {
		'type-enum': [
			2,
			'always',
			[
				'feat',
				'fix',
				'chore',
				'docs',
				'style',
				'refactor',
				'perf',
				'test',
				'build',
				'ci',
				'revert',
			],
		],
		'header-max-length': [2, 'always', 72],
		'body-max-line-length': [2, 'always', 100],
		'footer-max-line-length': [2, 'always', 100],
		'body-full-stop': [2, 'always', '.'],
	},
};
