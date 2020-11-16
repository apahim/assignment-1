from setuptools import setup


setup(name='cloudy',
      packages=['cloudy'],
      version=open('VERSION').read().strip(),
      author='Amador Pahim',
      author_email="amador@pahim.org",
      description='Web Application created for the Cloud Architecture assignment',
      python_requires='>=3.6',
      license="GPLv2+",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Framework :: Flask',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: '
          'GNU General Public License v2 or later (GPLv2+)',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      install_requires=[
          'Flask',
          'Flask-SQLAlchemy',
          'psycopg2-binary',
          'gunicorn',
          'boto3'
      ],
      )
