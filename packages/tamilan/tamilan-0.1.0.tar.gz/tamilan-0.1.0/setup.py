from setuptools import setup, find_packages

setup(
    name='tamilan',  # Your package name
    version='0.1.0',
    packages=find_packages(),  # This will find your package automatically
    py_modules=['twosum'],  # This will include your twosum.py file
    install_requires=[
        # Add any dependencies your module needs
    ],
    author='Sivasaran',
    author_email='sivasaran354@gmail.com',
    description='This module is for TwoSum operations and subsequence checks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sivasarans/2sum',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)
