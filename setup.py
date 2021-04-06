import pathlib
from setuptools import find_packages, setup

# The text of the README file
# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='zip2np', 
    packages=find_packages(include=['zip2np'], 
                           exclude=['tests']),
    version='0.1.1',
    url='https://github.com/borjaeg/zip2np',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    description='Library for decompressing Zip files and put into Numpy Arrays',
    author='Borjakas',
    author_email="hello@borjakas.com",
    license='MIT',
    long_description=README,
    include_package_data=True,
    long_description_content_type="text/markdown",
    install_requires=[
          'numpy',
          'glob3',
          'tqdm',
          'opencv-python'
      ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"]
)