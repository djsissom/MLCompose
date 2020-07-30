#!/usr/bin/env python

import setuptools

setuptools.setup(
	name='mlcompose',
	version='0.1.0',
	author='Daniel Sissom',
	author_email='daniel@arclet.org',
	description='Compose music with machine learning.',
	packages=['mlcompose'],
	entry_points={
		'console_scripts': [
			'mlcompose = mlcompose.mlcompose:main'
		]
	},
)
