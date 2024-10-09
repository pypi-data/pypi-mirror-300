from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='datai',
    version='1.5.2',
    description='A library for data visualization and cleaning',
    long_description=README,
    long_description_content_type='text/markdown',
    author='M Ans',
    author_email='m.ans.cs@outlook.com',
    url='https://github.com/yourusername/datai',  # Replace with your actual URL
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'setuptools',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
