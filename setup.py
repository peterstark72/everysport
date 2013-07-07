from distutils.core import setup
setup(name='everysport',
      version='1.0.2',
      packages=['everysport'],
      description='A Python wrapper for the Everysport API',
      author='Peter Stark',
      author_email='peterstark72@gmail.com',
      url='https://github.com/peterstark72/everysport',
      scripts=['esport.py'],
      classifiers=[
      	  'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: Free for non-commercial use',
          'Natural Language :: English',
          'Natural Language :: Swedish',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities'
          ],
      )