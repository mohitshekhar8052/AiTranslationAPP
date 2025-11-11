"""
Utility Functions Module
Common helper functions used throughout the application.
"""

import os
import re
import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_audio_file(file_path: str, supported_formats: list = None, max_size_mb: int = 200) -> Tuple[bool, Optional[str]]:
    """
    Validate an audio file for processing.
    
    Args:
        file_path (str): Path to the audio file
        supported_formats (list): List of supported file extensions
        max_size_mb (int): Maximum file size in megabytes
    
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if supported_formats is None:
        supported_formats = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
    
    # Check if file exists
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    # Check if file is readable
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    # Check file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in supported_formats:
        return False, f"Unsupported format: {file_ext}. Supported: {', '.join(supported_formats)}"
    
    # Check file size
    file_size_mb = get_file_size_mb(file_path)
    if file_size_mb > max_size_mb:
        return False, f"File too large: {file_size_mb:.1f}MB (max: {max_size_mb}MB)"
    
    return True, None


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    except Exception as e:
        logger.error(f"Error getting file size: {str(e)}")
        return 0.0


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds (float): Duration in seconds
    
    Returns:
        str: Formatted duration (MM:SS or HH:MM:SS)
    """
    if seconds < 0:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text (str): Input text
    
    Returns:
        int: Word count
    """
    if not text:
        return 0
    return len(text.split())


def count_tokens(text: str, model: str = 'gpt2') -> int:
    """
    Estimate token count for text.
    
    Args:
        text (str): Input text
        model (str): Tokenizer model to use
    
    Returns:
        int: Estimated token count
    """
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model)
        tokens = tokenizer.encode(text)
        return len(tokens)
    except Exception as e:
        logger.warning(f"Could not count tokens accurately: {str(e)}. Using word-based estimate.")
        # Fallback: rough estimate (1 word ≈ 1.3 tokens)
        return int(len(text.split()) * 1.3)


def sanitize_filename(filename: str) -> str:
    """
    Remove or replace invalid characters from filename.
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = 'untitled'
    
    # Limit length
    max_length = 200
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        name = name[:max_length - len(ext)]
        filename = name + ext
    
    return filename


def create_temp_directory(base_dir: str = './temp_uploads') -> str:
    """
    Create temporary directory for file uploads.
    
    Args:
        base_dir (str): Base directory path
    
    Returns:
        str: Created directory path
    """
    try:
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"Temporary directory ensured: {base_dir}")
        return base_dir
    except Exception as e:
        logger.error(f"Could not create temp directory: {str(e)}")
        raise


def cleanup_temp_files(directory: str, max_age_hours: int = 24):
    """
    Remove old temporary files to prevent disk space issues.
    
    Args:
        directory (str): Directory to clean up
        max_age_hours (int): Maximum age of files to keep (in hours)
    """
    if not os.path.exists(directory):
        logger.warning(f"Directory does not exist: {directory}")
        return
    
    try:
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=max_age_hours)
        
        deleted_count = 0
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_modified < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Deleted old temp file: {filename}")
                    except Exception as e:
                        logger.error(f"Could not delete {filename}: {str(e)}")
        
        if deleted_count > 0:
            logger.info(f"Cleanup complete: {deleted_count} files deleted from {directory}")
        else:
            logger.info(f"Cleanup complete: No old files found in {directory}")
            
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable string.
    
    Args:
        size_bytes (int): Size in bytes
    
    Returns:
        str: Formatted size (e.g., "2.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
    
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_filename_from_path(file_path: str) -> str:
    """
    Extract filename from path.
    
    Args:
        file_path (str): Full file path
    
    Returns:
        str: Filename without path
    """
    return os.path.basename(file_path)
