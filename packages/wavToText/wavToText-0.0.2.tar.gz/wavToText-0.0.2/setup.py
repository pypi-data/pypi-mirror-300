import config
from typing import List
from setuptools import find_packages, setup


def get_requirements(requi_file=config.requirements_path)->List[str]:
    try:
        with open(requi_file, 'r') as f:
            requi = f.readlines()
    except Exception as e:
        raise Exception(f"Error reading {requi_file} file: {e}")
        
    requirements = [req.replace("\n", '') for req in requi]
    if '-e .' in requirements:
        requirements.remove('-e .')
    print(requirements)
    return requirements


setup(
    name = 'wavToText',
    version = '0.0.2',
    author = 'LAKHAL Badr',
    author_email = 'lakhalbadr2@gmail.com',
    description = 'Conevrting english wav audio into text.',
    long_description = 'Voice recognition using a pretrained model called DeepSpeech v0.9.3 to convert English wav audio into text.',
    packages = find_packages(),
    install_requires = get_requirements()
)