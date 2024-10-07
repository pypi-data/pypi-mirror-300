from setuptools import setup, find_packages

setup(
    name='openface-test',
    version='0.1.3',
    description='A comprehensive toolkit for facial feature extraction.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jiewen Hu',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'torch',
        'opencv-python',
        'numpy',
        'Pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
