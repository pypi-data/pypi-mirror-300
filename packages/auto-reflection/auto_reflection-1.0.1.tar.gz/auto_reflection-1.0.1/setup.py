from setuptools import setup, find_packages

# Safely read the README.md file with UTF-8 encoding
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='auto_reflection',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'pypubsub',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'topics=auto_reflection.topics:main',
            'titles=auto_reflection.titles:main',
        ],
    },
    include_package_data=True,
    author='Alex Buzunov',
    author_email='alex_buz@yahoo.com',
    description='An AI-powered blog-writing pipeline with reflection-based agents using YAML configuration and mock data handling',
    long_description=long_description,  # Long description from README.md
    long_description_content_type='text/markdown',  # Specify that it's in Markdown
    url='https://github.com/myaichat/auto_reflection',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    project_urls={
        'Source': 'https://github.com/myaichat/auto_reflection',
        'Tracker': 'https://github.com/myaichat/auto_reflection/issues',
    },
)
