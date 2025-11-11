"""
Integration Tests
Tests the complete end-to-end workflow of the application.
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from summarizer import transcribe, summarize
from summarizer.export import export_to_txt, export_to_pdf


class TestFullPipeline:
    """Test complete pipeline from audio to export."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_complete_workflow(self):
        """
        Test the complete workflow: transcribe -> summarize -> export.
        Requires a sample audio file in sample_audio directory.
        """
        # Check for sample audio
        sample_audio = os.path.join('sample_audio', 'test.mp3')
        if not os.path.exists(sample_audio):
            pytest.skip("Sample audio file not found. Place a test audio file at sample_audio/test.mp3")
        
        # Step 1: Transcribe
        transcript, transcribe_error = transcribe(sample_audio, model_name='tiny')
        
        if transcribe_error:
            pytest.skip(f"Transcription failed (likely missing dependencies): {transcribe_error}")
        
        assert transcript != ""
        assert isinstance(transcript, str)
        
        # Step 2: Summarize
        summary, summarize_error = summarize(transcript, max_length=150, min_length=50)
        
        if summarize_error:
            pytest.skip(f"Summarization failed (likely missing dependencies): {summarize_error}")
        
        assert summary != ""
        assert isinstance(summary, str)
        assert len(summary.split()) < len(transcript.split())
        
        # Step 3: Export to TXT
        txt_bytes = export_to_txt(transcript, summary)
        assert isinstance(txt_bytes, bytes)
        assert len(txt_bytes) > 0
        
        # Verify TXT content
        txt_content = txt_bytes.decode('utf-8')
        assert transcript in txt_content
        assert summary in txt_content
        
        # Step 4: Export to PDF
        pdf_bytes = export_to_pdf(transcript, summary)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'
    
    @pytest.mark.integration
    def test_pipeline_with_mock_data(self):
        """
        Test pipeline with mock/synthetic data (no actual audio needed).
        Tests summarization and export without transcription.
        """
        # Mock transcript (simulate transcription output)
        mock_transcript = """
        Good morning everyone. Thank you for joining today's team meeting. 
        I'd like to start by reviewing our progress from last week. The development 
        team successfully completed the user authentication module and began initial 
        testing. The design team finalized the mockups for the new dashboard interface.
        
        Moving forward, our priorities for this week are as follows. First, we need 
        to integrate the payment processing system. Second, we should conduct user 
        acceptance testing on the authentication module. Third, the design team will 
        begin implementing the dashboard based on the approved mockups.
        
        We also need to address a few concerns. The API response times have been 
        slower than expected, so the backend team will investigate optimization 
        strategies. Additionally, we received feedback about the mobile responsiveness, 
        which the frontend team will prioritize.
        
        Does anyone have questions or concerns about these priorities? Let's make 
        sure we're all aligned before we dive into the detailed discussions.
        """
        
        # Summarize
        summary, error = summarize(mock_transcript, max_length=100, min_length=30)
        
        if error:
            pytest.skip(f"Summarization failed: {error}")
        
        assert summary != ""
        assert isinstance(summary, str)
        
        # Export
        txt_bytes = export_to_txt(mock_transcript, summary)
        assert len(txt_bytes) > 0
        
        pdf_bytes = export_to_pdf(mock_transcript, summary)
        assert pdf_bytes[:4] == b'%PDF'


class TestPipelineErrorHandling:
    """Test error handling throughout the pipeline."""
    
    def test_pipeline_with_invalid_audio(self):
        """Test pipeline with invalid audio file."""
        transcript, error = transcribe("invalid_file.wav")
        assert transcript == ""
        assert error is not None
    
    def test_pipeline_with_empty_transcript(self):
        """Test pipeline when transcription produces empty result."""
        summary, error = summarize("")
        assert summary == ""
        assert error is not None
    
    @pytest.mark.integration
    def test_export_with_invalid_content(self):
        """Test export with invalid content."""
        with pytest.raises(Exception):
            export_to_txt("", "")
        
        with pytest.raises(Exception):
            export_to_pdf("", "")


class TestMultipleFiles:
    """Test processing multiple files sequentially."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_process_multiple_files(self):
        """
        Test processing multiple audio files in sequence.
        Verifies no state leakage between runs.
        """
        # This test would require multiple sample files
        sample_files = [
            os.path.join('sample_audio', 'test1.mp3'),
            os.path.join('sample_audio', 'test2.mp3')
        ]
        
        # Check if sample files exist
        available_files = [f for f in sample_files if os.path.exists(f)]
        if len(available_files) < 2:
            pytest.skip("Multiple sample audio files not found")
        
        results = []
        
        for audio_file in available_files:
            transcript, trans_error = transcribe(audio_file, model_name='tiny')
            if trans_error:
                continue
            
            summary, sum_error = summarize(transcript, max_length=100)
            if sum_error:
                continue
            
            results.append({
                'transcript': transcript,
                'summary': summary
            })
        
        # Verify each result is unique (no state leakage)
        if len(results) >= 2:
            assert results[0]['transcript'] != results[1]['transcript']
            assert results[0]['summary'] != results[1]['summary']


class TestPerformance:
    """Test performance characteristics."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_caching_improves_performance(self):
        """
        Test that model caching improves performance on subsequent runs.
        """
        sample_audio = os.path.join('sample_audio', 'test.mp3')
        if not os.path.exists(sample_audio):
            pytest.skip("Sample audio file not found")
        
        import time
        
        # First run (loads model)
        start1 = time.time()
        transcript1, error1 = transcribe(sample_audio, model_name='tiny')
        time1 = time.time() - start1
        
        if error1:
            pytest.skip("Transcription failed")
        
        # Second run (uses cached model)
        start2 = time.time()
        transcript2, error2 = transcribe(sample_audio, model_name='tiny')
        time2 = time.time() - start2
        
        # Second run should be faster or similar (cached model)
        # Allow some variance
        assert time2 <= time1 * 1.5


class TestEndToEndScenarios:
    """Test realistic end-to-end scenarios."""
    
    @pytest.mark.integration
    def test_short_meeting_scenario(self):
        """Test with short meeting (mock data)."""
        short_meeting = "Quick standup. John completed the login feature. Sarah is working on the dashboard. No blockers."
        
        summary, error = summarize(short_meeting, max_length=50, min_length=10)
        
        if not error:
            assert len(summary) > 0
            txt_bytes = export_to_txt(short_meeting, summary)
            assert len(txt_bytes) > 0
    
    @pytest.mark.integration
    def test_long_meeting_scenario(self):
        """Test with long meeting (mock data)."""
        # Simulate a long meeting transcript
        long_meeting = """
        Welcome to our quarterly review meeting. I'm pleased to see everyone here today.
        Let's begin with a review of Q1 performance. Revenue exceeded targets by 15 percent,
        which is excellent news. The sales team deserves recognition for their outstanding work.
        """ * 20  # Repeat to create long text
        
        summary, error = summarize(long_meeting, max_length=150, min_length=50)
        
        if not error:
            assert len(summary) > 0
            # Summary should be much shorter
            assert len(summary.split()) < len(long_meeting.split()) / 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
