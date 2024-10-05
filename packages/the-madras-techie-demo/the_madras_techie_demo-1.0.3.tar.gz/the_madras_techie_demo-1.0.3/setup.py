from setuptools import setup, find_packages
setup(
name='the_madras_techie_demo',
version='1.0.3',
packages=find_packages(),
install_requires=[
# Add dependencies here.
# e.g. 'numpy>=1.11.1'
],
entry_points={
"console_scripts": [
"the_madras_techie_demo-hello = the_madras_techie_demo: hello",
"the_madras_techie_demo-weight = the_madras_techie_demo: weight",
"the_madras_techie_demo-height = the_madras_techie_demo: height",
],
},
)