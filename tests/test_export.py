"""
Unit Tests for Export Module
Tests the export functionality for TXT and PDF formats.
"""

import pytest
import os
import sys
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from summarizer.export import (
    export_to_txt,
    export_to_pdf,
    format_content,
    validate_export_inputs
)


class TestExportToTxt:
    """Test cases for TXT export."""
    
    def test_export_txt_basic(self):
        """Test basic TXT export."""
        transcript = "This is a test transcript."
        summary = "This is a test summary."
        
        result = export_to_txt(transcript, summary)
        
        assert isinstance(result, bytes)
        assert len(result) > 0
        
        # Decode and check content
        content = result.decode('utf-8')
        assert "MEETING SUMMARY REPORT" in content
        assert transcript in content
        assert summary in content
    
    def test_export_txt_with_timestamp(self):
        """Test TXT export with timestamp."""
        transcript = "Test transcript"
        summary = "Test summary"
        
        result = export_to_txt(transcript, summary, include_timestamp=True)
        content = result.decode('utf-8')
        
        assert "Generated on:" in content
    
    def test_export_txt_without_timestamp(self):
        """Test TXT export without timestamp."""
        transcript = "Test transcript"
        summary = "Test summary"
        
        result = export_to_txt(transcript, summary, include_timestamp=False)
        content = result.decode('utf-8')
        
        assert "Generated on:" not in content
    
    def test_export_txt_special_characters(self):
        """Test TXT export with special characters."""
        transcript = "Transcript with special chars: éàü 中文 🎙️"
        summary = "Summary with symbols: @#$%"
        
        result = export_to_txt(transcript, summary)
        content = result.decode('utf-8')
        
        assert transcript in content
        assert summary in content
    
    def test_export_txt_empty_raises_error(self):
        """Test that empty content raises error."""
        with pytest.raises(Exception):
            export_to_txt("", "")


class TestExportToPdf:
    """Test cases for PDF export."""
    
    def test_export_pdf_basic(self):
        """Test basic PDF export."""
        transcript = "This is a test transcript for PDF export."
        summary = "This is a test summary for PDF."
        
        result = export_to_pdf(transcript, summary)
        
        assert isinstance(result, bytes)
        assert len(result) > 0
        # Check PDF magic number
        assert result[:4] == b'%PDF'
    
    def test_export_pdf_with_long_text(self):
        """Test PDF export with long text."""
        transcript = "This is a long transcript. " * 500
        summary = "This is a summary. " * 50
        
        result = export_to_pdf(transcript, summary)
        
        assert isinstance(result, bytes)
        assert len(result) > 0
        assert result[:4] == b'%PDF'
    
    def test_export_pdf_special_characters(self):
        """Test PDF export with special characters."""
        transcript = "Transcript with special characters: éàü"
        summary = "Summary with symbols: @#$%"
        
        result = export_to_pdf(transcript, summary)
        
        assert isinstance(result, bytes)
        assert result[:4] == b'%PDF'
    
    def test_export_pdf_empty_raises_error(self):
        """Test that empty content raises error."""
        with pytest.raises(Exception):
            export_to_pdf("", "")


class TestFormatContent:
    """Test cases for format_content function."""
    
    def test_format_content_basic(self):
        """Test basic content formatting."""
        transcript = "Test transcript"
        summary = "Test summary"
        
        result = format_content(transcript, summary)
        
        assert isinstance(result, str)
        assert "MEETING SUMMARY REPORT" in result
        assert "EXECUTIVE SUMMARY" in result
        assert "FULL TRANSCRIPT" in result
        assert transcript in result
        assert summary in result
    
    def test_format_content_with_timestamp(self):
        """Test formatting with timestamp."""
        transcript = "Test"
        summary = "Test"
        
        result = format_content(transcript, summary, include_timestamp=True)
        assert "Generated on:" in result
    
    def test_format_content_without_timestamp(self):
        """Test formatting without timestamp."""
        transcript = "Test"
        summary = "Test"
        
        result = format_content(transcript, summary, include_timestamp=False)
        assert "Generated on:" not in result
    
    def test_format_content_statistics(self):
        """Test that statistics are included."""
        transcript = "One two three four five"
        summary = "One two"
        
        result = format_content(transcript, summary)
        
        assert "STATISTICS" in result
        assert "Word Count" in result
        assert "Compression Ratio" in result


class TestValidateExportInputs:
    """Test cases for export input validation."""
    
    def test_validate_valid_inputs(self):
        """Test validation with valid inputs."""
        error = validate_export_inputs("Valid transcript", "Valid summary")
        assert error is None
    
    def test_validate_empty_transcript(self):
        """Test validation with empty transcript."""
        error = validate_export_inputs("", "Valid summary")
        assert error is not None
        assert "transcript" in error.lower()
    
    def test_validate_empty_summary(self):
        """Test validation with empty summary."""
        error = validate_export_inputs("Valid transcript", "")
        assert error is not None
        assert "summary" in error.lower()
    
    def test_validate_whitespace_only(self):
        """Test validation with whitespace-only content."""
        error = validate_export_inputs("   ", "   ")
        assert error is not None


class TestExportIntegration:
    """Integration tests for export functionality."""
    
    def test_export_both_formats(self):
        """Test exporting to both TXT and PDF formats."""
        transcript = "Integration test transcript. This contains multiple sentences. It's testing the export."
        summary = "Integration test summary."
        
        # Export to TXT
        txt_result = export_to_txt(transcript, summary)
        assert isinstance(txt_result, bytes)
        assert len(txt_result) > 0
        
        # Export to PDF
        pdf_result = export_to_pdf(transcript, summary)
        assert isinstance(pdf_result, bytes)
        assert len(pdf_result) > 0
        assert pdf_result[:4] == b'%PDF'
    
    def test_export_with_realistic_content(self):
        """Test export with realistic meeting content."""
        transcript = """
        Welcome everyone to today's meeting. We'll be discussing the project timeline.
        First, let's review what we accomplished last week. The development team completed
        the authentication module and began testing. The design team finalized the mockups
        for the dashboard. Looking ahead, we need to focus on integrating the payment system
        and conducting user testing. Any questions before we dive into the details?
        """
        
        summary = """
        Team meeting covering project timeline. Last week: authentication module completed,
        dashboard mockups finalized. Next steps: payment system integration and user testing.
        """
        
        # Test both formats
        txt_result = export_to_txt(transcript, summary)
        assert isinstance(txt_result, bytes)
        
        pdf_result = export_to_pdf(transcript, summary)
        assert isinstance(pdf_result, bytes)
        assert pdf_result[:4] == b'%PDF'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
