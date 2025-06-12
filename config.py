"""
Configuration management for different environments
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    NEMO_API_KEY = os.environ.get('NEMO_API_KEY') or os.environ.get('NGC_API_KEY')
    API_KEY = os.environ.get('API_KEY') or 'default-api-key'

    # Vector store settings
    CHROMA_PERSIST_DIRECTORY = os.environ.get('CHROMA_PERSIST_DIRECTORY') or './chroma_db'

    # LLM settings
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL') or 'nemo-llama3-8b'
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', 1000))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))

    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or './uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Chunking settings
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 200))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    CHROMA_PERSIST_DIRECTORY = './test_chroma_db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
