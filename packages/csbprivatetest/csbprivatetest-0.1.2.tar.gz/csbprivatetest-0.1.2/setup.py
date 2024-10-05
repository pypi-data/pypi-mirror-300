from setuptools import setup, find_packages

setup(
    name='csbprivatetest',  # Your package name
    version='0.1.2',    # Version of the package
    description='CSB Toolkit for Georeferencing and Uncertainty Calculations',
    author='Vishwa Barathy',
    author_email='vishwa.barathy@cidco.ca',
    url='https://github.com/vishwabarathy-cidco/csbprivate',
    license='MIT',  # License type (if different, specify accordingly)

    # Define where the packages are located
    package_dir={'': 'src'},  # Root directory of the packages
    packages=find_packages(where='src'),  # Automatically find packages in 'src'

    # Include additional files like README.md, LICENSE, etc.
    include_package_data=True,
    long_description=open('README.md').read(),  # Ensures README.md is included
    long_description_content_type='text/markdown',
    
    # Specify classifiers if needed
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the required Python version
)
