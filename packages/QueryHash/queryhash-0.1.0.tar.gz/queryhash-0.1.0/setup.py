from setuptools import setup, find_packages

setup(
    name='QueryHash',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django app for hashing queries and responses with count increment.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ganesh-shipsy/QueryHash',
    author='GuvvalaGanesh',
    author_email='ganeshguvvala44@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 5.1',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=5.1.1',
        'mysqlclient',
    ],
)
