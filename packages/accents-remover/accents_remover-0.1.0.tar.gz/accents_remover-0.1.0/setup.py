from setuptools import setup

with open('README.md', 'r') as file:
    readme = file.read()
 
setup(
    name='accents_remover',
    version='0.1.0',
    license='MIT License',
    author='Lincoln Oliver',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='lincolnolive@gmail.com',
    keywords='remove accents',
    description='A function to remove string accents withouth changing other characters',
    packages=['src'],
    install_requires=[],
    url='https://github.com/lincolnolivr/accents_remover-pylib.git'
)