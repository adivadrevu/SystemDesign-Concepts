from setuptools import setup, find_packages

setup(
	name="flaskner",
	version="0.0.1",
	description="A simple NER API",
	packages=find_packages(exclude=("test", "tests")),
	python_requires=">=3.9",
	install_requires=[
		"Flask>=2.3",
		"spacy>=3.6",
	],
)
