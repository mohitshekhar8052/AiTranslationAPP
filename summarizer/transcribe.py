"""
Audio Transcription Module
Converts audio files to text using SpeechRecognition with pydub for format conversion.
"""

import speech_recognition as sr
import os
import logging
from typing import Optional, Tuple
from pydub import AudioSegment
from pydub.utils import which
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Module-level cache for the recognizer
_cached_recognizer = None

# Set ffmpeg path for pydub
AudioSegment.converter = which("ffmpeg") or which("avconv")


def convert_to_wav(audio_path: str) -> Tuple[str, Optional[str]]:
    """
    Convert audio file to WAV format if needed.
    
    Args:
        audio_path (str): Path to the audio file
    
    Returns:
        Tuple[str, Optional[str]]: (wav_path, error_message)
    """
    try:
        file_ext = os.path.splitext(audio_path)[1].lower()
        
        # If already WAV, return as is
        if file_ext == '.wav':
            return audio_path, None
        
        logger.info(f"Converting {file_ext} to WAV format...")
        
        # Load audio file
        if file_ext == '.mp3':
            audio = AudioSegment.from_mp3(audio_path)
        elif file_ext == '.m4a':
            audio = AudioSegment.from_file(audio_path, format='m4a')
        elif file_ext == '.ogg':
            audio = AudioSegment.from_ogg(audio_path)
        elif file_ext == '.flac':
            audio = AudioSegment.from_file(audio_path, format='flac')
        else:
            # Try generic import
            audio = AudioSegment.from_file(audio_path)
        
        # Convert to mono and set sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # Create temporary WAV file
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()
        
        # Export as WAV
        audio.export(temp_wav_path, format='wav')
        
        logger.info(f"Converted to WAV: {temp_wav_path}")
        return temp_wav_path, None
        
    except Exception as e:
        error_msg = f"Audio conversion error: {str(e)}. Make sure ffmpeg is installed: brew install ffmpeg"
        logger.error(error_msg, exc_info=True)
        return "", error_msg


def transcribe(audio_path: str, model_name: str = 'base') -> Tuple[str, Optional[str]]:
    """
    Transcribe audio file to text using SpeechRecognition.
    
    Args:
        audio_path (str): Path to the audio file
        model_name (str): Ignored (kept for compatibility)
    
    Returns:
        Tuple[str, Optional[str]]: (transcribed_text, error_message)
        Returns text and None if successful, empty string and error message if failed
    """
    global _cached_recognizer
    
    temp_wav_path = None
    
    try:
        # Validate audio file
        if not os.path.exists(audio_path):
            error_msg = f"Audio file not found: {audio_path}"
            logger.error(error_msg)
            return "", error_msg
        
        # Check file extension
        valid_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext not in valid_extensions:
            error_msg = f"Unsupported audio format: {file_ext}. Supported formats: {', '.join(valid_extensions)}"
            logger.error(error_msg)
            return "", error_msg
        
        # Convert to WAV if needed
        wav_path, convert_error = convert_to_wav(audio_path)
        if convert_error:
            return "", convert_error
        
        # Track if we created a temp file
        if wav_path != audio_path:
            temp_wav_path = wav_path
        
        # Initialize recognizer
        if _cached_recognizer is None:
            logger.info("Initializing speech recognizer")
            _cached_recognizer = sr.Recognizer()
            logger.info("Speech recognizer initialized")
        
        # Load audio file
        logger.info(f"Loading WAV file: {wav_path}")
        
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            _cached_recognizer.adjust_for_ambient_noise(source, duration=0.5)
            logger.info("Recording audio data...")
            audio_data = _cached_recognizer.record(source)
        
        # Transcribe using Google Speech Recognition (free)
        logger.info("Processing audio with Google Speech Recognition...")
        text = _cached_recognizer.recognize_google(audio_data)
        
        if not text:
            error_msg = "Transcription produced empty text"
            logger.warning(error_msg)
            return "", error_msg
        
        logger.info(f"Transcription completed. Length: {len(text)} characters")
        return text, None
        
    except sr.UnknownValueError:
        error_msg = "Could not understand audio. Please ensure the audio is clear and contains speech."
        logger.error(error_msg)
        return "", error_msg
    except sr.RequestError as e:
        error_msg = f"Could not request results from speech recognition service: {str(e)}"
        logger.error(error_msg)
        return "", error_msg
    except Exception as e:
        error_msg = f"Transcription error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return "", error_msg
    finally:
        # Clean up temporary WAV file
        if temp_wav_path and os.path.exists(temp_wav_path):
            try:
                os.unlink(temp_wav_path)
                logger.info("Cleaned up temporary WAV file")
            except Exception as e:
                logger.warning(f"Could not delete temp file: {e}")


def get_audio_duration(audio_path: str) -> Optional[float]:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        audio_path (str): Path to the audio file
    
    Returns:
        Optional[float]: Duration in seconds, or None if unable to determine
    """
    try:
        # Use pydub to get duration for any format
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000.0  # Convert milliseconds to seconds
        return duration
        
    except Exception as e:
        logger.warning(f"Could not determine audio duration: {str(e)}")
        return None


def get_cached_model_info() -> dict:
    """
    Get information about the currently cached recognizer.
    
    Returns:
        dict: Information about cached recognizer (loaded status)
    """
    return {
        'model_name': 'SpeechRecognition',
        'is_loaded': _cached_recognizer is not None
    }


def clear_model_cache():
    """
    Clear the cached recognizer from memory.
    Useful for freeing up memory.
    """
    global _cached_recognizer
    _cached_recognizer = None
    logger.info("Recognizer cache cleared")
