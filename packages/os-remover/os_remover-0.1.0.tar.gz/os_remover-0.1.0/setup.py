from setuptools import setup, find_packages

setup(
    name='os_remover',
    version='0.1.0',
    packages=find_packages(),
    description='Easy OS remover for WIndows/MacOS/Linux. Has demo mode.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='George Andreyanov',
    author_email='andreyanov.egor07@mail.ru',
    url='https://github.com/panicattacksss/os_remover/tree/main',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
