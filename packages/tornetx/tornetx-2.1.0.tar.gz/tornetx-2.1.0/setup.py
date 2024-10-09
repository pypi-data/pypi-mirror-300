from setuptools import setup, find_packages

setup(
    name='tornetx',
    version='2.1.0',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'requests',
        'stem',
    ],
    entry_points={
        'console_scripts': [
            'tornet=tornet.tornet:main',
        ],
    },
    author="ByteBreach",
    author_email="mrfidal@proton.me",
    maintainer="Macxzew",
    maintainer_email="macxzew@proton.me",
    description="TorNet - Automate IP address changes using Tor (Adapted by Macxzew)",
    license="MIT",

    # URL du projet (home-page)
    url="https://github.com/Macxzew/tornet",  # URL principale pour la version adaptée

    project_urls={
        'Original Repo': 'https://github.com/ByteBreach/tornet',
        'Adapted Repo': 'https://github.com/Macxzew/tornet',
    },

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
