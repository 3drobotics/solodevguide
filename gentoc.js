#!/usr/bin/env node

var fs = require('fs');

var file = fs.readFileSync(__dirname + '/README.md', 'utf-8')
	.replace(/\s+<!--TOC-->[\s\S]*<!--\/TOC-->\s+/, '\n\n')
	.split('\n');

var toc = []
file.filter(function (l) {
	if (l.match(/^\s*##(?!#)/)) {
		var title = l.replace(/^\s*##\s*/, '').replace(/^\s*|\s*$/g, '');
		toc.push([title, title.toLowerCase().replace(/[^a-z0-9_]+/g, '-').replace(/^-+|-+$/g, '')])
	}
});

var toclist = '<!--TOC-->\nTable of Contents:\n\n' + toc.map(function (line) {
	return '1. [' + line[0] + '](#' + line[1] + ')'
}).join('\n') + '\n\n<!--/TOC-->\n'

file.splice(2, 0, toclist)

fs.writeFileSync('README.md', file.join('\n'));
console.error('done')
