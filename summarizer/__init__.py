"""
AI Meeting Summarizer Package
Provides transcription and summarization functionality for audio files.
"""

from .transcribe import transcribe, get_audio_duration
from .summarize import summarize, chunk_text, merge_summaries

__all__ = [
    'transcribe',
    'get_audio_duration',
    'summarize',
    'chunk_text',
    'merge_summaries'
]

__version__ = '1.0.0'
