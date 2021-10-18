#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
]

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40',
]

examples_require = [
]

setup_requires = [
    'pytest-runner>=5.2',
]

processing_dependencies = [
    'celery>=5.0.5'
]

searchengine_dependencies = [
    'elasticsearch==7.13.4',  # compatible with opensearch (https://opensearch.org/docs/clients/index/)
    'elasticsearch-dsl==7.4.0'
]

invenio_dependencies = [
    'invenio-db>=1.0.9',
    'invenio-files-rest>=1.2.0',
    'invenio-records>=1.4.0',
    'invenio-records-files>=1.2.1',
    'invenio-indexer>=1.2.1',
    'invenio-cache>=1.1.0',
    'invenio-rdm-records>=0.32.5',
    'invenio-records-resources>=0.16.14',
    'invenio-drafts-resources>=0.13.6',
    'invenio-search>=1.4.2',
    'invenio-celery==1.2.2'  # fixed to avoid problems
]

database_dependencies = [
    'SQLAlchemy>=1.3.11',
    'psycopg2-binary>=2.8',
    'Flask-SQLAlchemy>=2.4',
    'sqlalchemy-json>=0.4.0',
    'marshmallow-sqlalchemy==0.25.0',
    'cacheout>=0.13.1'
]

general_dependencies = [
    'Click>=7.0',
    'Flask>=1.1.4',
    'six>=1.16.0',
    'base32-lib>=1.0.2',
    'bdc-auth-client @ git+https://github.com/brazil-data-cube/bdc-auth-client@v0.2.3',
]

install_requires = [*general_dependencies, *invenio_dependencies, *searchengine_dependencies,
                    *processing_dependencies, *database_dependencies]

extras_require = {
    'docs': docs_require,
    'examples': examples_require,
    'tests': tests_require,
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

packages = find_packages()

g = {}
with open(os.path.join('storm_ws', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='storm-ws',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    keywords=['Time series', 'Earth Observations'],
    license='MIT',
    author='Brazil Data Cube Team',
    author_email='brazildatacube@inpe.br',
    url='https://github.com/brazil-data-cube/storm-ws',
    project_urls={
        'Repository': 'https://github.com/brazil-data-cube/storm-ws',
        'Issues': 'https://github.com/brazil-data-cube/storm-ws/issues',
        'Documentation': 'https://storm-ws.readthedocs.io/en/latest/'
    },
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'storm-ws = storm_ws.cli:cli'
        ],
        'invenio_jsonschemas.schemas': [
            'node_record = storm_ws.models.graph.jsonschemas'
        ],
        'invenio_search.mappings': [
            'node_records = storm_ws.models.graph.mappings'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
