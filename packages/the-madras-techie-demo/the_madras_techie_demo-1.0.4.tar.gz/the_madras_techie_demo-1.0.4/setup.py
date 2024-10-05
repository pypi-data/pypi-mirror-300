from setuptools import setup, find_packages
setup(
name='the_madras_techie_demo',
version='1.0.4',
packages=find_packages(),
install_requires=[
# Add dependencies here.
# e.g. 'numpy>=1.11.1'
],
entry_points={
"console_scripts": [
"the_madras_techie_demo = the_madras_techie_demo: hello"
],},)