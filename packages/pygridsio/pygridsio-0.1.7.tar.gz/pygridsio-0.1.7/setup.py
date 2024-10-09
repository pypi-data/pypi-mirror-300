from setuptools import setup, find_packages

setup(
    name='pygridsio',  # Your module name
    version='0.1.7',  # Version number
    author='Hen Brett',  # Your name
    author_email='hen.brett@tno.nl',  # Your email
    description='This is a utility package to read in .zmap and .asc grids to numpy or xarrays',  # Short description
    long_description=open('README.md').read(),  # Read the long description from README
    long_description_content_type='text/markdown',  # Format of the long description
    url='https://ci.tno.nl/gitlab/AGS/pygridsio.git',  # URL to your project
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[  # Classifiers for package index
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust according to your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[  # Dependencies
        "numpy",
        "pandas",
        "pykrige",
        "xarray"
    ],
)