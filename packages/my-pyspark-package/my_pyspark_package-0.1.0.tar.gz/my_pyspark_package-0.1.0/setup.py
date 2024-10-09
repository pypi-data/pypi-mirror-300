from setuptools import setup, find_packages

setup(
    name='my_pyspark_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0',
    ],
    description='A package to count nulls and -1s in PySpark DataFrames.',
    author='Your Name',
    author_email='prodipesh12@gmail.com',
    url='https://github.com/yourusername/my_pyspark_package',
)
