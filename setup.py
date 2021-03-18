from setuptools import setup
setup(
  name = 'RailIN',
  packages = ['RailIN'],
  version = '0.2',
  description = 'Unofficial API for Indian Railways.',
  license='MIT',
  author = 'Ashish Shukla',
  author_email = 'ash2shukla@gmail.com',
  url = 'https://github.com/ash2shukla/RailIN',
  download_url = 'https://github.com/ash2shukla/RailIN/archive/0.1.tar.gz',
  keywords = ['Railways', 'API', 'IR','unofficial'],
  classifiers = [],
  install_requires=[
          'bs4',
          'requests==2.20.0',
          'user_agent==0.1.8',
          'pillow==8.1.1',
          'pytesseract==0.1.7'
          ]
)
