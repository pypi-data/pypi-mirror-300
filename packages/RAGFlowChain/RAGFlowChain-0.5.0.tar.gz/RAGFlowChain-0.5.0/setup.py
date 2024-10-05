from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="RAGFlowChain",
    version="0.5.0",  # Updated version
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
        "langchain==0.1.16",
        "langchain-community==0.0.33",
        "langchain-core==0.1.52",
        "langchain-experimental==0.0.57",
        "langchain-groq==0.1.3",
        "langchain-openai==0.0.8",
        "langchain-text-splitters==0.0.1",
        "langgraph==0.0.48",
        "typing_extensions>=4.12.2",
        "google-api-python-client>=2.0.2",
        "youtube-transcript-api>=0.4.3",
        "pyyaml>=5.4.1",
        "chromadb>=0.3.21",
        "python-pptx>=0.6.21",
        "python-docx>=0.8.11",
        "docx>=0.2.4",
        "faiss-cpu>=1.7.2",  # FAISS for CPU-only systems
        "annoy>=1.17.0",     # Annoy for Approximate Nearest Neighbors
        "pytube>=12.0.0",
        "pypdf>=3.0.0",
        "nltk>=3.6.3"
    ],
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
