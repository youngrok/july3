from setuptools import setup, find_packages

setup(name='july3',
      description='Deployment automation tool',
      author='Youngrok Pak',
      author_email='pak.youngrok@gmail.com',
      keywords= 'make build deploy fabric devops',
      url='https://github.com/youngrok/july3',
      version='0.0.3',
      packages=find_packages(),
      scripts=['bin/july3'],
      package_data={'july3': ['files/*'],},
      classifiers = [
                     'Development Status :: 3 - Alpha',
                     'Topic :: System :: Installation/Setup',
                     'License :: OSI Approved :: BSD License']
      )
