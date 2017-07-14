from setuptools import setup


setup(name='DukeBlinky',
        version='0.0.1',
        description='Tool for accessing Duke ldap and grouper',
        url='https://github.com/Duke-GCB/DukeBlinky',
        keywords='duke ldap grouper internet2',
        license='MIT',
        packages=['blinky'],
        install_requires=[
          'python-ldap==2.4.41',
          'requests==2.18.1',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
    )

