from setuptools import setup, find_packages

setup(
    name='sentineltools',
    version=open("version.txt").read(),
    author='Matthew Sanchez',
    author_email='xxspicymelonxx@gmail.com',
    description='A collection of AI, video, image, sound, and text tools among other things. Designed for windows.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'chatollama',
        'diffusers',
        'accelerate',
        'pillow',
        'opencv-python',
        'numpy',
    ],
)
