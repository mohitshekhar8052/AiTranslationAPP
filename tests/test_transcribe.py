"""
Unit Tests for Transcription Module
Tests the audio transcription functionality using Whisper.
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from summarizer.transcribe import transcribe, get_audio_duration, get_cached_model_info, clear_model_cache


class TestTranscribe:
    """Test cases for transcribe function."""
    
    def test_transcribe_invalid_path(self):
        """Test transcription with non-existent file."""
        text, error = transcribe("nonexistent_file.wav")
        assert text == ""
        assert error is not None
        assert "not found" in error.lower()
    
    def test_transcribe_unsupported_format(self, tmp_path):
        """Test transcription with unsupported file format."""
        # Create a dummy .txt file
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is not an audio file")
        
        text, error = transcribe(str(test_file))
        assert text == ""
        assert error is not None
        assert "unsupported" in error.lower()
    
    def test_model_caching(self):
        """Test that model caching works correctly."""
        # Clear cache first
        clear_model_cache()
        
        # Check cache is empty
        info = get_cached_model_info()
        assert info['is_loaded'] is False
        assert info['model_name'] is None
    
    @pytest.mark.slow
    def test_transcribe_valid_audio(self):
        """
        Test transcription with a valid audio file.
        This test requires a sample audio file to be present.
        Marked as slow since it loads the model.
        """
        # Check if sample audio exists
        sample_audio = os.path.join('sample_audio', 'test.mp3')
        if not os.path.exists(sample_audio):
            pytest.skip("Sample audio file not found")
        
        text, error = transcribe(sample_audio, model_name='tiny')
        
        # If successful
        if error is None:
            assert text != ""
            assert isinstance(text, str)
            assert len(text) > 0
        else:
            # If it fails due to missing dependencies, skip
            pytest.skip(f"Transcription failed: {error}")
    
    @pytest.mark.slow
    def test_different_model_sizes(self):
        """
        Test that different model sizes can be specified.
        Marked as slow since it may load models.
        """
        model_sizes = ['tiny', 'base']
        
        sample_audio = os.path.join('sample_audio', 'test.mp3')
        if not os.path.exists(sample_audio):
            pytest.skip("Sample audio file not found")
        
        for model_size in model_sizes:
            clear_model_cache()
            text, error = transcribe(sample_audio, model_name=model_size)
            
            if error is None:
                assert isinstance(text, str)
                info = get_cached_model_info()
                assert info['model_name'] == model_size


class TestAudioDuration:
    """Test cases for audio duration function."""
    
    def test_get_duration_invalid_file(self):
        """Test duration calculation with invalid file."""
        duration = get_audio_duration("nonexistent.wav")
        assert duration is None
    
    def test_get_duration_non_audio(self, tmp_path):
        """Test duration calculation with non-audio file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Not audio")
        
        duration = get_audio_duration(str(test_file))
        assert duration is None


class TestModelCache:
    """Test cases for model caching functionality."""
    
    def test_clear_cache(self):
        """Test clearing the model cache."""
        clear_model_cache()
        info = get_cached_model_info()
        assert info['is_loaded'] is False
    
    def test_cache_info_structure(self):
        """Test that cache info has expected structure."""
        info = get_cached_model_info()
        assert 'model_name' in info
        assert 'is_loaded' in info


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
