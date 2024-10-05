from setuptools import setup, find_packages
setup(
name='the_madras_techie_demo',
version='1.0.2',
packages=find_packages(),
install_requires=[
# Add dependencies here.
# e.g. 'numpy>=1.11.1'
],
entry_points={
"console_scripts": [
"tmt-hello = the_madras_techie_demo: hello",
"tmt-weight = the_madras_techie_demo: weight",
"tmt-height = the_madras_techie_demo: height",
],
},
)