from setuptools import setup
setup(
  name = 'RailIN',
  packages = ['RailIN'], # this must be the same as the name above
  version = '0.2',
  description = 'Unofficial API for Indian Railways.',
  license='MIT',
  author = 'Ashish Shukla',
  author_email = 'ash2shukla@gmail.com',
  url = 'https://github.com/ash2shukla/RailIN', # use the URL to the github repo
  download_url = 'https://github.com/ash2shukla/RailIN/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['Railways', 'API', 'IR','unofficial'], # arbitrary keywords
  classifiers = [],
  install_requires=[
          'bs4',
          'requests==2.18.1',
          'user_agent==0.1.8',
          'pillow==4.2.1',
          'pytesseract==0.1.7'
          ]
)
