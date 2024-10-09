from setuptools import setup, find_packages

setup(
    name='gajaraj',
    version='1.00',
    author='Akshat Shukla',
    author_email='Akshatshukla317@gmail.com',
    description='A Pandas alternative library in Python. Gajaraj aims to provide similar functionalities as Pandas, enabling users to perform data manipulation and analysis seamlessly.',
    packages=find_packages(),
    install_requires=[
        'pandas',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)