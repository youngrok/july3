from setuptools import setup
setup(name='july3',
      description='Deployment automation tool',
      author='Youngrok Pak',
      author_email='pak.youngrok@gmail.com',
      keywords= 'fabric pycrypto ecdsa',
      url='https://github.com/youngrok/july3',
      version='0.0.1',
      packages=['july3',
                ],
      package_data={'july3': ['files/*'],},
      classifiers = [
                     'Development Status :: 3 - Alpha',
                     'Topic :: System :: Installation/Setup',
                     'License :: OSI Approved :: BSD License']
      )