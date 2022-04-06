import setuptools


with open("README.md", "r") as fin:
    long_description = fin.read()

setuptools.setup(
    name='clip-util',
    version='0.0.3',
    author='Kyle L. Davis',
    author_email='AceofSpades5757.github@gmail.com',
    url='https://github.com/AceofSpades5757/clip-util',
    description='Utilities for use with Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    python_requires='>=3.6',
    packages=setuptools.find_packages('src'),
    package_dir={
        '': 'src',
        'clipboard': 'src/clipboard',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
