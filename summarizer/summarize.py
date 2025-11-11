"""
Text Summarization Module
Generates concise summaries from long text using transformer models.
"""

import logging
from typing import List, Optional, Tuple
from transformers import pipeline
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Module-level cache for the summarization pipeline
_cached_pipeline = None


def summarize(
    text: str,
    max_length: int = 150,
    min_length: int = 50,
    method: str = 'abstractive'
) -> Tuple[str, Optional[str]]:
    """
    Generate a summary from the input text.
    
    Args:
        text (str): Input text to summarize
        max_length (int): Maximum length of summary in tokens
        min_length (int): Minimum length of summary in tokens
        method (str): Summarization method ('abstractive' or 'extractive')
    
    Returns:
        Tuple[str, Optional[str]]: (summary_text, error_message)
        Returns summary and None if successful, empty string and error message if failed
    """
    global _cached_pipeline
    
    try:
        # Validate input
        if not text or not text.strip():
            error_msg = "Input text is empty"
            logger.error(error_msg)
            return "", error_msg
        
        # Initialize pipeline if not cached
        if _cached_pipeline is None:
            logger.info("Loading summarization model: facebook/bart-large-cnn")
            _cached_pipeline = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU, change to 0 for GPU
            )
            logger.info("Summarization model loaded successfully")
        
        # Check if text needs chunking
        max_tokens = 1024
        estimated_tokens = len(text.split()) * 1.3  # Rough estimate
        
        if estimated_tokens > max_tokens:
            logger.info(f"Text exceeds token limit ({estimated_tokens:.0f} > {max_tokens}). Chunking text...")
            chunks = chunk_text(text, max_tokens=max_tokens)
            summaries = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Summarizing chunk {i+1}/{len(chunks)}")
                chunk_summary = _cached_pipeline(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )[0]['summary_text']
                summaries.append(chunk_summary)
            
            # Merge chunk summaries
            final_summary = merge_summaries(summaries, max_length=max_length, min_length=min_length)
            logger.info("Multi-chunk summarization completed")
            return final_summary, None
        else:
            # Summarize directly
            logger.info("Summarizing text...")
            summary = _cached_pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
            
            logger.info(f"Summarization completed. Summary length: {len(summary)} characters")
            return summary, None
    
    except Exception as e:
        error_msg = f"Summarization error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        # Fallback to extractive summarization
        try:
            logger.info("Attempting fallback extractive summarization...")
            fallback_summary = _extractive_fallback(text, num_sentences=3)
            return fallback_summary, None
        except Exception as fallback_error:
            logger.error(f"Fallback summarization failed: {str(fallback_error)}")
            return "", error_msg


def chunk_text(text: str, max_tokens: int = 1024) -> List[str]:
    """
    Split text into chunks that fit within model's token limit.
    Attempts to split on sentence boundaries.
    
    Args:
        text (str): Text to chunk
        max_tokens (int): Maximum tokens per chunk
    
    Returns:
        List[str]: List of text chunks
    """
    # Split into sentences (basic approach)
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Rough token estimation: 1 word ≈ 1.3 tokens
    for sentence in sentences:
        sentence_tokens = len(sentence.split()) * 1.3
        
        if current_length + sentence_tokens > max_tokens:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_tokens
            else:
                # Single sentence exceeds limit, split it
                words = sentence.split()
                chunk_size = int(max_tokens / 1.3)
                for i in range(0, len(words), chunk_size):
                    chunks.append(' '.join(words[i:i+chunk_size]))
        else:
            current_chunk.append(sentence)
            current_length += sentence_tokens
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.info(f"Text chunked into {len(chunks)} parts")
    return chunks


def merge_summaries(
    summary_chunks: List[str],
    max_length: int = 150,
    min_length: int = 50
) -> str:
    """
    Merge multiple summary chunks into a single coherent summary.
    
    Args:
        summary_chunks (List[str]): List of summary texts to merge
        max_length (int): Maximum length for final summary
        min_length (int): Minimum length for final summary
    
    Returns:
        str: Merged summary
    """
    global _cached_pipeline
    
    if not summary_chunks:
        return ""
    
    if len(summary_chunks) == 1:
        return summary_chunks[0]
    
    # Concatenate summaries
    combined = ' '.join(summary_chunks)
    
    # If combined text is short enough, return as is
    if len(combined.split()) <= max_length:
        return combined
    
    # Otherwise, run another summarization pass
    try:
        logger.info("Running second summarization pass to merge chunks...")
        final_summary = _cached_pipeline(
            combined,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']
        return final_summary
    except Exception as e:
        logger.warning(f"Could not merge summaries: {str(e)}. Returning concatenated version.")
        # Return truncated concatenated version
        words = combined.split()[:max_length]
        return ' '.join(words)


def _extractive_fallback(text: str, num_sentences: int = 3) -> str:
    """
    Simple extractive summarization fallback.
    Returns the first N sentences.
    
    Args:
        text (str): Text to summarize
        num_sentences (int): Number of sentences to extract
    
    Returns:
        str: Extractive summary
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary_sentences = sentences[:num_sentences]
    return ' '.join(summary_sentences)


def clear_pipeline_cache():
    """
    Clear the cached summarization pipeline from memory.
    """
    global _cached_pipeline
    _cached_pipeline = None
    logger.info("Summarization pipeline cache cleared")


def get_pipeline_info() -> dict:
    """
    Get information about the cached pipeline.
    
    Returns:
        dict: Pipeline information
    """
    return {
        'is_loaded': _cached_pipeline is not None,
        'model': 'facebook/bart-large-cnn' if _cached_pipeline else None
    }
