import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='maven',
    version='0.0.3',
    description=("Maven's goal is to reduce the time data scientists spend on data cleaning and preparation"
                 "by providing easy access to open datasets in both raw and processed formats."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='maven open data etl pipeline',
    author='John Sandall',
    author_email='contact@coefficient.ai',
    url='https://github.com/john-sandall/maven',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
