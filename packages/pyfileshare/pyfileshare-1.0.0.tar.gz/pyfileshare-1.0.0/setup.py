from setuptools import setup, find_packages

setup(
	name='pyfileshare',
	version='1.0.0',
	packages=find_packages(),
	install_requires=[
		"cloudscraper",
		"bs4"
	],
	author='RedPiar',
	author_email='Regeonwix@gmail.com',
	license='MIT',
	description='PyFileShare is a Python library designed for seamless interaction with the file-sharing service.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/RedPiarOfficial/FileShare/',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.8',
	keywords=[
		"file sharing",
		"file upload",
		"file download",
		"cloudscraper",
		"BeautifulSoup"
	],
)
