"""
Configuration Module
Centralized configuration settings for the AI Meeting Summarizer application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Whisper Model Configuration
WHISPER_MODEL_SIZES = ['tiny', 'base', 'small', 'medium', 'large']
DEFAULT_WHISPER_MODEL = os.getenv('DEFAULT_WHISPER_MODEL', 'base')

# Audio File Configuration
MAX_AUDIO_SIZE_MB = int(os.getenv('MAX_AUDIO_SIZE_MB', '200'))
SUPPORTED_AUDIO_FORMATS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']

# Summarization Model Configuration
SUMMARIZATION_MODEL = 'facebook/bart-large-cnn'
DEFAULT_SUMMARY_MAX_LENGTH = int(os.getenv('SUMMARY_MAX_LENGTH', '150'))
DEFAULT_SUMMARY_MIN_LENGTH = int(os.getenv('SUMMARY_MIN_LENGTH', '50'))

# Text Processing Configuration
CHUNK_SIZE_TOKENS = 1024
MAX_TOKENS_PER_CHUNK = 1024

# File Storage Configuration
TEMP_UPLOAD_DIR = os.getenv('TEMP_UPLOAD_DIR', './temp_uploads')
MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', '')

# OpenAI Configuration (optional)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Application Settings
APP_TITLE = "AI Meeting Summarizer"
APP_ICON = "🎙️"
PAGE_LAYOUT = "wide"

# Export Settings
EXPORT_TIMESTAMP_FORMAT = "%B %d, %Y at %I:%M %p"

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


def get_config(key: str, default=None):
    """
    Get configuration value by key.
    
    Args:
        key (str): Configuration key
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    """
    return globals().get(key, default)


def validate_config() -> tuple:
    """
    Validate required configuration settings.
    
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Validate Whisper model
    if DEFAULT_WHISPER_MODEL not in WHISPER_MODEL_SIZES:
        errors.append(f"Invalid DEFAULT_WHISPER_MODEL: {DEFAULT_WHISPER_MODEL}. Must be one of {WHISPER_MODEL_SIZES}")
    
    # Validate audio size limit
    if MAX_AUDIO_SIZE_MB <= 0:
        errors.append(f"Invalid MAX_AUDIO_SIZE_MB: {MAX_AUDIO_SIZE_MB}. Must be positive.")
    
    # Validate summary lengths
    if DEFAULT_SUMMARY_MIN_LENGTH >= DEFAULT_SUMMARY_MAX_LENGTH:
        errors.append(f"SUMMARY_MIN_LENGTH ({DEFAULT_SUMMARY_MIN_LENGTH}) must be less than SUMMARY_MAX_LENGTH ({DEFAULT_SUMMARY_MAX_LENGTH})")
    
    # Create temp directory if it doesn't exist
    if not os.path.exists(TEMP_UPLOAD_DIR):
        try:
            os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
        except Exception as e:
            errors.append(f"Could not create TEMP_UPLOAD_DIR: {str(e)}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def print_config():
    """
    Print current configuration for debugging.
    """
    print("=" * 60)
    print("AI MEETING SUMMARIZER - CONFIGURATION")
    print("=" * 60)
    print(f"Whisper Model: {DEFAULT_WHISPER_MODEL}")
    print(f"Max Audio Size: {MAX_AUDIO_SIZE_MB} MB")
    print(f"Supported Formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}")
    print(f"Summarization Model: {SUMMARIZATION_MODEL}")
    print(f"Summary Length: {DEFAULT_SUMMARY_MIN_LENGTH}-{DEFAULT_SUMMARY_MAX_LENGTH} tokens")
    print(f"Temp Upload Dir: {TEMP_UPLOAD_DIR}")
    print(f"Model Cache Dir: {MODEL_CACHE_DIR if MODEL_CACHE_DIR else 'Default'}")
    print(f"OpenAI API Key: {'Configured' if OPENAI_API_KEY else 'Not configured'}")
    print("=" * 60)


# Validate configuration on import
is_valid, validation_errors = validate_config()
if not is_valid:
    print("Configuration validation warnings:")
    for error in validation_errors:
        print(f"  - {error}")
