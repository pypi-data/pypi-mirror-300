from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-16") as f:
    required_packages = f.read().splitlines()


setup(
name='bb_pbf_html_writer',
version='0.1.1',
author='John Nastala',
author_email='your.email@example.com',
description='Writes BB Mega PBF HTML file and adds links to the HTML file.',
packages=find_packages(),
install_requires=required_packages, 
# long_description=open("README.md").read()
# long_description_content_type='text/plain',
# url='https://github.com/yourusername/my_package',
)
