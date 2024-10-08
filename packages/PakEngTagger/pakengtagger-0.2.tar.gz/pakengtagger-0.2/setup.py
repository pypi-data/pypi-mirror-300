from setuptools import setup, find_packages

setup(
    name='PakEngTagger',
    version='0.2',
    packages=['pak_eng_tagger'],
    install_requires=[],
    description='A POS tagger for Pakistani English developed by Muhammad Owais',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

