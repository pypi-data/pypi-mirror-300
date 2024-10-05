from setuptools import setup, find_packages

setup(
    name='django-zero-theme',
    version='0.1.16',
    packages=find_packages(),
    include_package_data=True,  # Include static and templates
    license='MIT License',
    description='A reusable Django app for ...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/farjanul/django-zero-theme',
    author='Farjanul Nayem',
    author_email='mr.farjanul@gmail.com',
    install_requires=[
        'django>=3.2',
        'django-import-export>=4.1.1',
    ],
    extras_require={
        'dev': ['pytest', 'tox', 'black'],  # Optional dependencies for development
    },
    project_urls={
        'Source': 'https://github.com/farjanul/django-zero-theme',
        'Issue Tracker': 'https://github.com/farjanul/django-zero-theme/issues',  # GitHub Issues page
    },
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
