from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name="elyzer",
    entry_points={
        'console_scripts': [
            'elyzer=elyzer.__main__:main'
        ]
    },
    packages=['elyzer'],
    version="1.1.0",
    description="Step-by-Step Debug Elasticsearch Analyzers",
    long_description=read_md('README.md'),
    license="Apache",
    author="Doug Turnbull",
    author_email="dturnbull@o19s.com",
    url='https://github.com/o19s/elyzer',
    install_requires=['elasticsearch>=5.0.0,<6.0.0'],
    keywords=["elasticsearch", "database"],
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities'
    ]
)
