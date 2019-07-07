import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='maven',
    version='0.0.1',
    author='John Sandall',
    author_email='contact@coefficient.ai',
    description='A trusted expert who seeks to pass timely and relevant knowledge on to others.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/john-sandall/maven',
    packages=setuptools.find_packages(),
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
