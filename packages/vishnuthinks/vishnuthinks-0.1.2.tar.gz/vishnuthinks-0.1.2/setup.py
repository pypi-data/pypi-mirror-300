from setuptools import setup, find_packages

setup(
    name="vishnuthinks",  
    version="0.1.2",  
    author="Vishnu",  
    author_email="vishnurajalbandi18@gmail.com",  
    description="A Python Quiz module for learning Python with random questions.",
    long_description=open('README.md').read(),
    
    
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vishnuthinks-quiz = vishnuthinks:run_quiz',  
        ],
    },
)
