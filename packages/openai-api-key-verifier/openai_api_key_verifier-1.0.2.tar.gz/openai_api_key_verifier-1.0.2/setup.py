from setuptools import setup, find_packages

setup(
    name='openai_api_key_verifier',
    version='1.0.2',  # Update to the new version
    packages=find_packages(),
    description='A Python library for validating OpenAI API keys, and listing available models and verifying model access, and retrieving detailed account usage metrics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marcus Deacey',
    author_email='marcusdeacey@duck.com',
    url='https://github.com/mdeacey/openai-api-key-verifier/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'verify_openai_api_key=openai_api_key_verifier:main',
        ],
    },
)