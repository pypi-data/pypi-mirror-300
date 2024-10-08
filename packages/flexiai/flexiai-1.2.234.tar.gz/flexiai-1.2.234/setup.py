# setup.py
from setuptools import setup, find_packages

def read_readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

setup(
    name='flexiai',
    version='1.2.234',
    packages=find_packages(where='src', exclude=['tests', 'tests.*']),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'flexiai': [
            'assistant_actions/*.py',
            'cfg/*.py',
            'core/*.py',
            'core/flexi_managers/*.py',
            'core/utils/*.py',
            'credentials/*.py',
            'scripts/*.py'
        ],
    },
    install_requires=[
        'annotated-types>=0.7.0,<0.8.0',
        'anyio>=4.4.0,<5.0.0',
        'azure-common>=1.1.28,<2.0.0',
        'azure-core>=1.30.2,<2.0.0',
        'azure-identity>=1.17.1,<2.0.0',
        'azure-mgmt-core>=1.4.0,<2.0.0',
        'azure-mgmt-resource>=23.1.1,<24.0.0',
        'blinker>=1.8.2,<2.0.0',
        'certifi>=2024.7.4,<2025.0.0',
        'cffi>=1.16.0,<2.0.0',
        'charset-normalizer>=3.3.2,<4.0.0',
        'click>=8.1.7,<9.0.0',
        'cryptography>=43.0.0,<44.0.0',
        'distro>=1.9.0,<2.0.0',
        'Flask>=3.0.3,<4.0.0',
        'h11>=0.14.0,<0.15.0',
        'httpcore>=1.0.5,<2.0.0',
        'httpx>=0.27.0,<0.28.0',
        'idna>=3.7,<4.0.0',
        'iniconfig>=2.0.0,<3.0.0',
        'isodate>=0.6.1,<1.0.0',
        'itsdangerous>=2.2.0,<3.0.0',
        'Jinja2>=3.1.4,<4.0.0',
        'MarkupSafe>=2.1.5,<3.0.0',
        'msal>=1.30.0,<2.0.0',
        'msal-extensions>=1.2.0,<2.0.0',
        'nest-asyncio>=1.6.0,<2.0.0',
        'openai>=1.51.0,<2.0.0',
        'packaging>=24.1,<25.0',
        'platformdirs>=3.7.0,<5.0.0',
        'pluggy>=1.5.0,<2.0.0',
        'portalocker>=2.10.1,<3.0.0',
        'pycparser>=2.22,<3.0.0',
        'pydantic>=2.8.2,<3.0.0',
        'pydantic-settings>=2.3.3,<3.0.0',
        'pydantic_core>=2.20.1,<3.0.0',
        'PyJWT>=2.8.0,<3.0.0',
        'pytest>=8.3.1,<9.0.0',
        'python-dotenv>=1.0.1,<2.0.0',
        'pillow>=10.4.0,<11.0.0',
        'pypandoc>=1.13,<2.0.0',
        'requests>=2.32.3,<3.0.0',
        'six>=1.16.0,<2.0.0',
        'sniffio>=1.3.1,<2.0.0',
        'tqdm>=4.66.4,<5.0.0',
        'typing_extensions>=4.12.2,<5.0.0',
        'urllib3>=2.2.2,<3.0.0',
        'Werkzeug>=3.0.3,<4.0.0',
        'faiss-cpu>=1.8.0,<2.0.0',
        'numpy>=1.26.4,<2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'setup-flexiai-rag=flexiai.scripts.flexiai_rag_extension:setup_project',
            'setup-flexiai-flask-app=flexiai.scripts.flexiai_basic_flask_app:setup_project',
            'flexiai=flexiai.scripts.cli:main',
        ],
    },
    author='Savin Ionut Razvan',
    author_email='razvan.i.savin@gmail.com',
    description=(
        "FlexiAI: A dynamic and modular AI framework leveraging Multi-Agent Systems and "
        "Retrieval Augmented Generation (RAG) for seamless integration with OpenAI and "
        "Azure OpenAI services."
    ),
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SavinRazvan/flexiai',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
    ],
    python_requires='>=3.11',
    project_urls={
        'Bug Reports': 'https://github.com/SavinRazvan/flexiai/issues',
        'Source': 'https://github.com/SavinRazvan/flexiai',
    },
    license='MIT',
)
