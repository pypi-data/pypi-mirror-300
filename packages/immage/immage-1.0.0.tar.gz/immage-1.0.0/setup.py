from setuptools import setup, find_packages

setup(
    name='immage',
    version='1.0.0',
    description='A versatile image processing library with method chaining and procedural texture generation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tom Wawer',
    author_email='sq5rix@gmail.com',
    url='https://github.com/sq5rix/immage',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'numpy',
        'noise'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
