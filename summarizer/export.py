"""
Export Module
Handles exporting transcripts and summaries to TXT and PDF formats.
"""

import logging
from datetime import datetime
from typing import Optional
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_to_txt(
    transcript: str,
    summary: str,
    filename: str = 'meeting_summary.txt',
    include_timestamp: bool = True
) -> bytes:
    """
    Export transcript and summary to a TXT file.
    
    Args:
        transcript (str): Full transcript text
        summary (str): Summary text
        filename (str): Desired filename
        include_timestamp (bool): Whether to include generation timestamp
    
    Returns:
        bytes: File content as bytes for download
    """
    try:
        content = format_content(transcript, summary, include_timestamp)
        
        # Convert to bytes
        file_bytes = content.encode('utf-8')
        
        logger.info(f"TXT file created successfully: {filename}")
        return file_bytes
        
    except Exception as e:
        error_msg = f"Error creating TXT file: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg)


def export_to_pdf(
    transcript: str,
    summary: str,
    filename: str = 'meeting_summary.pdf'
) -> bytes:
    """
    Export transcript and summary to a PDF file.
    
    Args:
        transcript (str): Full transcript text
        summary (str): Summary text
        filename (str): Desired filename
    
    Returns:
        bytes: PDF file content as bytes for download
    """
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Container for PDF elements
        elements = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#1f4788',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor='#2e5090',
            spaceAfter=12,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=12
        )
        
        # Add title
        title = Paragraph("Meeting Summary Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add metadata
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        metadata = Paragraph(f"<i>Generated on {timestamp}</i>", styles['Normal'])
        elements.append(metadata)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add summary section
        summary_heading = Paragraph("Executive Summary", heading_style)
        elements.append(summary_heading)
        
        # Split summary into paragraphs for better formatting
        summary_paragraphs = summary.split('\n')
        for para in summary_paragraphs:
            if para.strip():
                summary_para = Paragraph(para.strip(), body_style)
                elements.append(summary_para)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Add transcript section
        transcript_heading = Paragraph("Full Transcript", heading_style)
        elements.append(transcript_heading)
        
        # Split transcript into paragraphs
        transcript_paragraphs = transcript.split('\n')
        for para in transcript_paragraphs:
            if para.strip():
                transcript_para = Paragraph(para.strip(), body_style)
                elements.append(transcript_para)
        
        # Add statistics
        elements.append(Spacer(1, 0.3*inch))
        stats_heading = Paragraph("Statistics", heading_style)
        elements.append(stats_heading)
        
        word_count_transcript = len(transcript.split())
        word_count_summary = len(summary.split())
        compression_ratio = (1 - word_count_summary / word_count_transcript) * 100 if word_count_transcript > 0 else 0
        
        stats_text = f"""
        Transcript Word Count: {word_count_transcript}<br/>
        Summary Word Count: {word_count_summary}<br/>
        Compression Ratio: {compression_ratio:.1f}%
        """
        stats_para = Paragraph(stats_text, body_style)
        elements.append(stats_para)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"PDF file created successfully: {filename}")
        return pdf_bytes
        
    except Exception as e:
        error_msg = f"Error creating PDF file: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg)


def format_content(
    transcript: str,
    summary: str,
    include_timestamp: bool = True
) -> str:
    """
    Format transcript and summary content for text export.
    
    Args:
        transcript (str): Full transcript text
        summary (str): Summary text
        include_timestamp (bool): Whether to include timestamp
    
    Returns:
        str: Formatted content string
    """
    lines = []
    
    # Header
    lines.append("=" * 80)
    lines.append("MEETING SUMMARY REPORT")
    lines.append("=" * 80)
    lines.append("")
    
    # Timestamp
    if include_timestamp:
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        lines.append(f"Generated on: {timestamp}")
        lines.append("")
    
    # Summary section
    lines.append("-" * 80)
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 80)
    lines.append("")
    lines.append(summary)
    lines.append("")
    
    # Transcript section
    lines.append("-" * 80)
    lines.append("FULL TRANSCRIPT")
    lines.append("-" * 80)
    lines.append("")
    lines.append(transcript)
    lines.append("")
    
    # Statistics
    word_count_transcript = len(transcript.split())
    word_count_summary = len(summary.split())
    compression_ratio = (1 - word_count_summary / word_count_transcript) * 100 if word_count_transcript > 0 else 0
    
    lines.append("-" * 80)
    lines.append("STATISTICS")
    lines.append("-" * 80)
    lines.append(f"Transcript Word Count: {word_count_transcript}")
    lines.append(f"Summary Word Count: {word_count_summary}")
    lines.append(f"Compression Ratio: {compression_ratio:.1f}%")
    lines.append("")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def validate_export_inputs(transcript: str, summary: str) -> Optional[str]:
    """
    Validate inputs for export functions.
    
    Args:
        transcript (str): Transcript text
        summary (str): Summary text
    
    Returns:
        Optional[str]: Error message if validation fails, None otherwise
    """
    if not transcript or not transcript.strip():
        return "Transcript is empty. Cannot export."
    
    if not summary or not summary.strip():
        return "Summary is empty. Cannot export."
    
    return None
