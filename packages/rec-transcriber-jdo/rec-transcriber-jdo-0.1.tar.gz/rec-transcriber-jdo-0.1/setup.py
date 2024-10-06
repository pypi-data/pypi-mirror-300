from setuptools import setup, find_packages

setup(
    name='rec-transcriber-jdo',
    version='0.1',
    description='Quick & Easy reccomendation letter transcription.',
    author='Sebastian Lueders',
    author_email='sebastianjlueders@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyPDF2',
        'fpdf'
    ],
    entry_points={
        'console_scripts': [
            'rec-transcriber-jdo=rec_transcriber_jdo.transcriber:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
