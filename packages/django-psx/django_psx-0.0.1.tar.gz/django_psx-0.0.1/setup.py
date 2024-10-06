from setuptools import setup, find_packages

setup(
    name='django-psx',
    version='0.0.1',
    packages=find_packages(),
    description='A placeholder package to reserve my project name',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cory Fitz',
    url='https://github.com/coryfitz/django-psx',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)