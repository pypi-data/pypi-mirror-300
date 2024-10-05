from setuptools import setup,find_packages

setup(
    name='SamTech_STT',
    version='0.4',
    author_email='sam@samtech.gmail.com',
    description='A simple Speech-To-Text Package developed by Samrat Paul',
    url='https://github.com/SamratPaul16',  
)

packages=find_packages(),

install_requirements=[
        'selenium',
        'webdriver_manager']