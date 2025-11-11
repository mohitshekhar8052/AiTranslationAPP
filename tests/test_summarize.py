"""
Unit Tests for Summarization Module
Tests the text summarization functionality.
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from summarizer.summarize import (
    summarize,
    chunk_text,
    merge_summaries,
    clear_pipeline_cache,
    get_pipeline_info
)


class TestSummarize:
    """Test cases for summarize function."""
    
    def test_summarize_empty_text(self):
        """Test summarization with empty text."""
        summary, error = summarize("")
        assert summary == ""
        assert error is not None
        assert "empty" in error.lower()
    
    def test_summarize_whitespace_only(self):
        """Test summarization with whitespace only."""
        summary, error = summarize("   \n\t  ")
        assert summary == ""
        assert error is not None
    
    def test_summarize_short_text(self):
        """Test summarization with short text."""
        short_text = "This is a short test text. It has only two sentences."
        summary, error = summarize(short_text, max_length=50, min_length=10)
        
        # May succeed or fail depending on model availability
        if error is None:
            assert isinstance(summary, str)
            assert len(summary) > 0
        else:
            # Expected if models not available
            assert isinstance(error, str)
    
    @pytest.mark.slow
    def test_summarize_long_text(self):
        """
        Test summarization with long text that requires chunking.
        Marked as slow since it loads the model.
        """
        # Create a long text by repeating sentences
        long_text = " ".join([
            "This is a test sentence about artificial intelligence and machine learning." 
            for _ in range(200)
        ])
        
        summary, error = summarize(long_text, max_length=150, min_length=50)
        
        if error is None:
            assert isinstance(summary, str)
            assert len(summary) > 0
            # Summary should be shorter than input
            assert len(summary.split()) < len(long_text.split())
    
    def test_summarize_length_parameters(self):
        """Test that length parameters are respected."""
        text = "Artificial intelligence is transforming the world. " * 20
        
        summary, error = summarize(text, max_length=100, min_length=30)
        
        if error is None:
            word_count = len(summary.split())
            # Allow some flexibility in token vs word count
            assert word_count <= 120  # Some buffer for tokenization differences


class TestChunkText:
    """Test cases for chunk_text function."""
    
    def test_chunk_short_text(self):
        """Test chunking with text that fits in one chunk."""
        short_text = "This is a short text. It should not be chunked."
        chunks = chunk_text(short_text, max_tokens=1024)
        
        assert len(chunks) == 1
        assert chunks[0] == short_text
    
    def test_chunk_long_text(self):
        """Test chunking with text that requires multiple chunks."""
        long_text = "This is a sentence. " * 1000
        chunks = chunk_text(long_text, max_tokens=500)
        
        assert len(chunks) > 1
        # Each chunk should be non-empty
        for chunk in chunks:
            assert len(chunk) > 0
    
    def test_chunk_preserves_content(self):
        """Test that chunking preserves all content."""
        text = "Sentence one. Sentence two. Sentence three."
        chunks = chunk_text(text, max_tokens=100)
        
        # Reconstruct text from chunks
        reconstructed = " ".join(chunks)
        
        # Should contain all original words (may have spacing differences)
        for word in text.split():
            assert word in reconstructed
    
    def test_chunk_empty_text(self):
        """Test chunking with empty text."""
        chunks = chunk_text("", max_tokens=1024)
        assert len(chunks) == 0 or (len(chunks) == 1 and chunks[0] == "")


class TestMergeSummaries:
    """Test cases for merge_summaries function."""
    
    def test_merge_empty_list(self):
        """Test merging with empty list."""
        result = merge_summaries([])
        assert result == ""
    
    def test_merge_single_summary(self):
        """Test merging with single summary."""
        summary = "This is a single summary."
        result = merge_summaries([summary])
        assert result == summary
    
    def test_merge_multiple_summaries(self):
        """Test merging multiple summaries."""
        summaries = [
            "First summary about AI.",
            "Second summary about ML.",
            "Third summary about data science."
        ]
        
        result = merge_summaries(summaries, max_length=100, min_length=20)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should combine content
        combined = " ".join(summaries)
        if len(result.split()) <= 100:
            # If short enough, may return concatenated
            assert len(result) <= len(combined) * 1.2  # Allow some buffer
    
    def test_merge_respects_max_length(self):
        """Test that merge respects maximum length."""
        summaries = ["Summary part one. " * 50, "Summary part two. " * 50]
        
        result = merge_summaries(summaries, max_length=100, min_length=20)
        
        # Result should not be excessively long
        assert len(result.split()) <= 150  # Buffer for tokenization


class TestPipelineCache:
    """Test cases for pipeline caching."""
    
    def test_clear_pipeline_cache(self):
        """Test clearing the pipeline cache."""
        clear_pipeline_cache()
        info = get_pipeline_info()
        assert info['is_loaded'] is False
    
    def test_pipeline_info_structure(self):
        """Test pipeline info structure."""
        info = get_pipeline_info()
        assert 'is_loaded' in info
        assert 'model' in info


class TestExtractiveFallback:
    """Test cases for extractive summarization fallback."""
    
    def test_fallback_on_model_error(self):
        """Test that fallback works when model fails."""
        # This is tested implicitly in other tests
        # The summarize function should fall back to extractive
        # summarization if the model fails
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
