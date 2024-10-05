from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()


setup(
name='the_madras_techie_demo',
version='1.0.8',
packages=find_packages(),
install_requires=[
# Add dependencies here.
# e.g. 'numpy>=1.11.1'
],
entry_points={
"console_scripts": [
"the_madras_techie_demo = the_madras_techie_demo:hello",
"tmt-hello = the_madras_techie_demo:hello",
"tmt-height = the_madras_techie_demo:height",
"tmt-weight = the_madras_techie_demo:weight",
"tmt-location = the_madras_techie_demo:location",
"tmt-job = the_madras_techie_demo:job",
"tmt-sports = the_madras_techie_demo:sports"
],},
long_description=description,
long_description_content_type="text/markdown",
)