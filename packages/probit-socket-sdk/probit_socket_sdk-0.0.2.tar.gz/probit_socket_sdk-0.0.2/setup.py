from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='probit_socket_sdk',
    version='0.0.2',
    description='Software Development Kit designated for Probit Global Exchange',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Probit Global',
    author_email='dev@probit.com',
    url='https://github.com/probitexchange/ProbitSocketSDK-python.git',
    install_requires=['requests', 'websocket-client'],
    packages=find_packages(exclude=[]),
    keywords=['probit exchange', 'probit', 'probit global', 'probit sdk', 'probit socket', 'probit websocket'],
    python_requires='>=3.12',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ],
)