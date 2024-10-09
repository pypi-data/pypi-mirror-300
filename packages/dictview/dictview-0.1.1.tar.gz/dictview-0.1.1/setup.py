from setuptools import setup, find_packages

setup(
    name='dictview',  # Replace with your package name
    version='0.1.1',
    author='Quentin Auster',
    author_email='qauster1@gmail.com',
    description='A package for viewing and navigating heavily nested dictionaries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/qaust/dictview/tree/main',  # Your package's GitHub repository
    packages=find_packages(where='src'),  # Tell setuptools to look in 'src'
    package_dir={'': 'src'},  # Point to the 'src' directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)