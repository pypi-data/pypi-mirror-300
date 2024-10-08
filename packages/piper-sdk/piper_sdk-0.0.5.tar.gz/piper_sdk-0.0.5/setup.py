from setuptools import setup, find_packages

setup(
    name='piper_sdk',
    version='0.0.5',
    packages=find_packages(include=['piper_sdk', 'piper_sdk.*']),
    include_package_data=True,
    install_requires=[
        'python-can>=4.3.1',
    ],
    entry_points={
    },
    author='RosenYin',
    author_email='yinruocheng321@gmail.com',
    description='A sdk to control piper',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

