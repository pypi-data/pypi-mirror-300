from setuptools import setup, find_packages

setup(
    name='randomcos',
    version='0.1.1',
    author='Klev',
    author_email='klevbs6@gmail.com',
    description='A pseudo-random number generator based on the cosine of the current time',
    packages=find_packages(),
    py_modules=['randomcos'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)