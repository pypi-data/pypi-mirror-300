from setuptools import setup, find_packages

setup(
    name='bib_vk_bots',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'vk-api',
    ],
    entry_points={
        'console_scripts': [
            'bib_vk_bots=bib_vk_bots.bot:main',
        ],
    },
)