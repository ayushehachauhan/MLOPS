from setuptools import find_packages,setup
from typing import List
HYPEN_edot="-e ."
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file:
        requirements=file.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        if HYPEN_edot in requirements:
            requirements.remove(HYPEN_edot)
        return requirements

setup(
name="MLOPS project",
version="0.0.1",
author="Ayush Chauhan",
author_email="ayushchauhan317@gmail.com",
packages=find_packages(),
install_requires=get_requirements('requirements.txt')#give the required list like ['pandas','numpy']
)