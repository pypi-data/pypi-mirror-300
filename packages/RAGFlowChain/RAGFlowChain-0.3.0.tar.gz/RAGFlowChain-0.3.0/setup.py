from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="RAGFlowChain",
    version="0.3.0",  # Updated version
    description="A comprehensive toolkit for building Retrieval-Augmented Generation (RAG) pipelines, including data loading, vector database creation, retrieval, and chain management.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kwadwo Daddy Nyame Owusu - Boakye',
    author_email='kwadwo.owusuboakye@outlook.com',
    url='https://github.com/knowusuboaky/RAGFlowChain',
    packages=find_packages(include=["ragflowchain", "ragflowchain.*"]),
    install_requires=[
        "pandas>=1.1.0",
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "langchain>=0.0.200",
        "langchain-community>=0.0.8",
        "typing_extensions>=4.12.2",
        "google-api-python-client>=2.0.2",
        "youtube-transcript-api>=0.4.3",
        "pyyaml>=5.4.1",
        "chromadb>=0.3.21",
        "sentence-transformers>=2.2.0",
        "python-pptx>=0.6.21",
        "python-docx>=0.8.11",
        "docx>=0.2.4",
        "lxml>=4.6.3",
        "faiss-cpu>=1.7.2",  # FAISS for CPU-only systems
        "annoy>=1.17.0",     # Annoy for Approximate Nearest Neighbors
        "pytube>=12.0.0",
        "pypdf>=3.0.0",
        "nltk>=3.6.3",       # Natural Language Toolkit for NLP
        "spacy>=3.0.0",      # spaCy for advanced NLP
        "transformers>=4.0.0",  # Huggingface Transformers library for models
        "torch>=1.8.0",      # PyTorch for deep learning models
        "tensorflow>=2.5.0", # TensorFlow for deep learning models
        "scikit-learn>=0.24.2", # Machine Learning utilities
        "gensim>=4.0.0",     # Topic Modeling and Document Processing
        "tqdm>=4.56.0",      # Progress bars for loops
        "matplotlib>=3.3.4", # Plotting and visualization
        "seaborn>=0.11.1",   # Statistical data visualization
        "openai>=0.6.0",     # OpenAI API for GPT models
        "azure-ai-textanalytics>=5.1.0", # Azure AI Text Analytics API
        "boto3>=1.17.0",     # AWS SDK for Python
        "Pillow>=8.1.0",     # Image processing
        "dataclasses>=0.6",  # Backport for Python 3.6
        "aiohttp>=3.7.4",    # Asynchronous HTTP Client/Server
        "fastapi>=0.65.0",   # FastAPI for building web APIs
        "uvicorn>=0.14.0",   # ASGI server for FastAPI
        "pydantic>=1.8.2",   # Data validation and settings management using Python type annotations
        "httpx>=0.18.2",     # The next generation HTTP client for Python
        "orjson>=3.5.2",     # Ultra fast JSON parsing and serialization
        "aiobotocore>=1.4.2", # Async version of boto3 (AWS SDK)
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.3.0",
            "flake8>=3.9.0",
            "isort>=5.7.0"
        ],
        "docs": [
            "sphinx>=3.4.3",
            "sphinx_rtd_theme>=0.5.1"
        ]
    },
    entry_points={
        "console_scripts": [
            "ragflowchain=ragflowchain.cli:main",
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords=[
        "RAG", "Retrieval-Augmented Generation", "Vector Database", "Data Fetching",
        "Generative AI", "AI", "Machine Learning", "ML", "GenAI", "Agent", "LangChain",
        "Data Processing", "Information Retrieval", "NLP", "Natural Language Processing",
        "Data Science", "Python", "Text Mining", "Deep Learning", "Document Processing",
        "FAISS", "Annoy", "Chroma", "pytube", "nltk", "spacy", "transformers", 
        "torch", "tensorflow", "scikit-learn", "gensim"
    ],
)
