import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='italian-holidays',
    version='0.0.2',
    author='Giuseppe Bruno',
    author_email='info@gbrunodev.it',
    description='A simple Python helper class to determine Italian holidays.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/giuseppebruno/italian-holidays',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)