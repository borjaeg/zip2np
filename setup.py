from setuptools import find_packages, setup

setup(
    name='pyeden',
    packages=find_packages(include=['pyeden'], exclude=['tests']),
    version='0.1.0',
    url='https://github.com/',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    description='Library for downloading EDEN datasets',
    author='SFT Group',
    license='MIT',
    long_description=open('README.md').read() + "\n\n" + open("CHANGELOG.txt").read(),
    install_requires=[
          'requests',
          'numpy',
          'glob3',
          'tqdm',
          'opencv-python'
      ]
)