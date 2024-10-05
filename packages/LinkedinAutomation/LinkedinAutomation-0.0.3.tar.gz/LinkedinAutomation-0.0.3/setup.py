from setuptools import setup, find_packages
from typing import List

trigger_mode = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.replace("\n", "") for r in requirements]
        if trigger_mode in requirements:
            requirements.remove(trigger_mode)

    return requirements


setup(

    name = 'LinkedinAutomation',
    version= '0.0.3',
    author= 'Ranjeet Aloriya',
    author_email= 'ranjeet.aloriya@gmail.com',
    description='A Python package for remove unwanted linkedin connection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Environment :: Console',
    ],
    python_requires='>=3.6',
    install_requires=get_requirements("requirements.txt"),
    include_package_data=True,
    keywords='breach response, breach notification, notification lists, data consolidation, unique identifiers, affected parties, data merging, efficiency tools, duplicate notifications incident response, document review, data consolidation, unique identifiers, affected parties, data merging, efficiency tools, duplicate notifications, incident response, breach response'
    
)