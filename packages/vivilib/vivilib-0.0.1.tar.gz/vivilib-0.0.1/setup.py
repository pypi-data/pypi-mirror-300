from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'vivilib test release'
LONG_DESCRIPTION = 'place to store random utility functions'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="vivilib", 
        version=VERSION,
        author="Vivian Wang",
        author_email="lilcatriag@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'vivilib'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)