import os
from setuptools import setup, find_packages


version = "0.1"

install_requires = [
    'chameleon',
    'horseman',
    'roughrider.routing',
    'wrapt',
    'fanstatic',
    'cromlech.session',
    'cromlech.sessions.file',
]

test_requires = [
    'WebTest',
]


setup(
    name='uvc_serviceportal',
    version=version,
    author='Novareto GmbH',
    author_email='contact@example.com',
    url='http://www.example.com',
    download_url='',
    description='Horseman example WebSite',
    long_description=(open("README.txt").read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python:: 3 :: Only',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    entry_points={
        'fanstatic.libraries': [
            'uvc_servicportal = uvc_serviceportal.resources:library',
        ],
    }
)
