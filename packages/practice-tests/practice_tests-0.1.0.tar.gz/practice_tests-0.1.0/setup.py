from setuptools import setup, find_packages

setup(
    name='practice_tests',
    version='0.1.0',
    packages=find_packages(),
    description='A simple SDK to manage names',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rajasekhar Baludu',
    author_email='rajasekharbaludu10105@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
