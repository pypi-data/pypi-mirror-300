from setuptools import setup


setup(
    name='cli2',
    version='3.0.0rc4',
    setup_requires='setupmeta',
    install_requires=[
        'docstring_parser',
        'pyyaml',
        'pygments',
    ],
    extras_require=dict(
        test=[
            'freezegun',
            'pytest',
            'pytest-cov',
        ],
    ),
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/cli2',
    include_package_data=True,
    license='MIT',
    keywords='cli',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cli2 = cli2.cli:main.entry_point',
        ],
    },
)
