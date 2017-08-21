from setuptools import setup
#
setup(
  name = 'vralib',
  packages = ['vralib'],
  version = '0.1',
  description = 'This is a helper library used to manage vRealize Automation via python.',
  author = 'Russell Pope',
  author_email = 'vralib@kovarus.com',
  url = 'https://github.com/kovarus/vrealize-pysdk',
  keywords = ['vralib'],
  install_requires = ['requests', 'prettytable'],
  classifiers = [],
)
