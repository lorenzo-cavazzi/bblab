from setuptools import setup, find_packages

setup(
	name="bblab",
	version="0.1",
	url="https://github.com/lorenzo-cavazzi/bblab",
	license="MIT",
	author="Lorenzo Cavazzi",
	author_email="lorenzo.cavazzi.tech@gmail.com",
	description="Library implementing useful image processing algorithms for the bblab",
	packages=find_packages(exclude=["tests"]),
	long_description=open("README.md").read(),
	zip_safe=False,
	python_requires=">=3.4",
	install_requires=[
		"numpy",
		"opencv-python"
	]
)