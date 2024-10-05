from setuptools import setup, find_packages

setup(
    name='SamTech_STT',
    version='0.6',
    author_email='sam@samtech.gmail.com',
    description='A simple Speech-To-Text Package developed by Samrat Paul',
    url='https://github.com/SamratPaul16',
    packages=find_packages(),
    include_package_data=True,  # Add this line to include non-Python files
    install_requires=[
        'selenium',
        'webdriver_manager',
    ],
)
