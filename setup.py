from setuptools import setup, find_packages

setup(
    name = "sss",
    version = "1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Django>=1.2', 'distribute>=0.6'],
    author='Bruno Bord',
    author_email='bruno@jehaisleprintemps.net',
    description='Simple Scrum System is a basic Django-based Scrum-like project manager. It takes advantage of the automagic admin contrib site.',
    license='WTFPL',
    keywords='django scrum',
    url='https://bitbucket.org/brunobord/sss/',
    setup_requires=['setuptools_hg'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Framework :: Django',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
    ],
    long_description = open('README', 'r').read(),
    download_url = 'http://pypi.python.org/pypi/sss',
)
