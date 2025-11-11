"""
AI Meeting Summarizer - Streamlit Application
Main application file for the web interface.
"""

import streamlit as st
import os
import time
from pathlib import Path

# Import modules
from summarizer import transcribe, summarize
from summarizer.export import export_to_txt, export_to_pdf, validate_export_inputs
import config
import utils

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="collapsed"
)

# Custom CSS for ultra-modern UI with glassmorphism and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Modern background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 50%, #ec4899 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        padding-top: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        backdrop-filter: blur(10px);
    }
    
    /* Glassmorphism header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 20px rgba(255,255,255,0.3);
        animation: fadeIn 0.8s ease-in;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #e0e7ff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Glassmorphism boxes */
    .summary-box, .transcript-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1.5rem 0;
        color: #1e293b;
        font-size: 1rem;
        line-height: 1.8;
        transition: all 0.3s ease;
    }
    
    .summary-box:hover, .transcript-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    .summary-box h3, .transcript-box h3 {
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .summary-box p, .transcript-box p {
        color: #374151;
        margin-bottom: 0.75rem;
    }
    
    /* Modern stats cards with glassmorphism */
    .stats-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.8rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    .stats-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 1);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        transition: all 0.3s ease;
        color: white;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card h4 {
        color: white;
        font-weight: 700;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    
    /* Modern gradient buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.6);
        background: linear-gradient(135deg, #8b5cf6 0%, #0ea5e9 100%);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
    }
    
    /* Metrics with gradient */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Modern file uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.9);
        border: 3px dashed rgba(14, 165, 233, 0.5);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0ea5e9;
        background: rgba(255, 255, 255, 1);
        transform: scale(1.02);
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.2);
    }
    
    /* Gradient progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0ea5e9 0%, #8b5cf6 50%, #ec4899 100%);
    }
    
    /* Modern expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        font-weight: 600;
        color: #1e293b;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 15px;
        border-bottom: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.95);
        color: #0ea5e9;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Modern alerts */
    .stAlert {
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    /* Floating particles background */
    .particle {
        position: fixed;
        width: 10px;
        height: 10px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        animation: float 6s infinite ease-in-out;
    }
    
    /* Loading spinner */
    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid #0ea5e9;
        width: 40px;
        height: 40px;
        animation: rotate 1s linear infinite;
        margin: 0 auto;
    }
    
    /* Text areas */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid rgba(14, 165, 233, 0.3);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'processing_time' not in st.session_state:
        st.session_state.processing_time = 0
    if 'audio_file_path' not in st.session_state:
        st.session_state.audio_file_path = None
    if 'files_processed' not in st.session_state:
        st.session_state.files_processed = 0
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True


def render_header():
    """Render the main header with branding"""
    # Animated header with icon
    st.markdown("""
        <div class="main-header" style="animation: fadeIn 0.8s ease-in;">
            <div style="display: inline-block; animation: bounce 2s infinite ease-in-out;">
                🎙️
            </div>
            AI Meeting Summarizer
        </div>
        <div class="sub-header" style="animation: fadeIn 1s ease-in;">
            <span style="display: inline-block; animation: shimmer 3s infinite; background: linear-gradient(90deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,1) 50%, rgba(255,255,255,0.6) 100%); background-size: 1000px 100%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                Transform your meeting recordings into clear, actionable summaries using advanced AI
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights with modern glassmorphism design and animations
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="feature-card" style="animation: slideUp 0.5s ease-out;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite;">🎯</div>
                <h4>Accurate Transcription</h4>
                <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.9); margin: 0;">Speech-to-text precision</p>
                <div style="margin-top: 10px; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, white, transparent); opacity: 0.5;"></div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card" style="animation: slideUp 0.6s ease-out;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite 0.2s;">⚡</div>
                <h4>Fast Processing</h4>
                <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.9); margin: 0;">Get results in minutes</p>
                <div style="margin-top: 10px; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, white, transparent); opacity: 0.5;"></div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card" style="animation: slideUp 0.7s ease-out;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite 0.4s;">🤖</div>
                <h4>AI Summarization</h4>
                <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.9); margin: 0;">Intelligent insights</p>
                <div style="margin-top: 10px; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, white, transparent); opacity: 0.5;"></div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="feature-card" style="animation: slideUp 0.8s ease-out;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite 0.6s;">📄</div>
                <h4>Easy Export</h4>
                <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.9); margin: 0;">PDF & TXT formats</p>
                <div style="margin-top: 10px; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, white, transparent); opacity: 0.5;"></div>
            </div>
        """, unsafe_allow_html=True)


def process_audio(uploaded_file, model_size, max_length, min_length):
    """Process uploaded audio file with enhanced progress tracking."""
    # Create temp directory
    temp_dir = utils.create_temp_directory(config.TEMP_UPLOAD_DIR)
    
    # Save uploaded file
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.session_state.audio_file_path = file_path
    
    # Validate file
    is_valid, error_msg = utils.validate_audio_file(
        file_path,
        config.SUPPORTED_AUDIO_FORMATS,
        config.MAX_AUDIO_SIZE_MB
    )
    
    if not is_valid:
        st.error(f"❌ Validation Error: {error_msg}")
        return False
    
    # Create a progress container
    progress_container = st.container()
    
    with progress_container:
        # Overall progress bar
        progress_bar = st.progress(0, text="Starting processing...")
        status_text = st.empty()
        
        # Step 1: Transcription
        status_text.markdown("### 🎤 Step 1: Transcribing Audio")
        progress_bar.progress(10, text="Preparing audio for transcription...")
        
        with st.spinner("Converting and transcribing audio... This may take a few minutes."):
            start_time = time.time()
            
            progress_bar.progress(30, text="Transcribing audio...")
            transcript_text, transcribe_error = transcribe(file_path, model_name=model_size)
            
            if transcribe_error:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Transcription failed: {transcribe_error}")
                return False
            
            st.session_state.transcript = transcript_text
            transcribe_time = time.time() - start_time
            
            progress_bar.progress(50, text="Transcription complete!")
            st.success(f"✅ Transcription completed in {transcribe_time:.1f} seconds!")
        
        # Step 2: Summarization
        status_text.markdown("### 🤖 Step 2: Generating AI Summary")
        progress_bar.progress(60, text="Loading summarization model...")
        
        with st.spinner("Analyzing text and generating summary..."):
            start_time = time.time()
            
            progress_bar.progress(70, text="Generating summary...")
            summary_text, summarize_error = summarize(
                transcript_text,
                max_length=max_length,
                min_length=min_length
            )
            
            if summarize_error:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Summarization failed: {summarize_error}")
                return False
            
            st.session_state.summary = summary_text
            summarize_time = time.time() - start_time
            st.session_state.processing_time = transcribe_time + summarize_time
            
            progress_bar.progress(90, text="Finalizing results...")
        
        # Complete
        progress_bar.progress(100, text="Processing complete!")
        st.success(f"✅ Summary generated in {summarize_time:.1f} seconds!")
        
        # Show total time
        st.info(f"⏱️ **Total processing time:** {st.session_state.processing_time:.1f} seconds")
        
        # Increment files processed counter
        st.session_state.files_processed += 1
        
        # Clean up progress indicators
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
    
    return True


def render_results():
    """Render transcript and summary results with interactive elements."""
    if not st.session_state.transcript:
        return
    
    st.divider()
    
    # Animated success message
    st.success("✅ Processing Complete! Here are your results:")
    
    # Statistics with animated cards
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 20px; margin: 20px 0; animation: slideUp 0.5s ease-out; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
            <h3 style='color: #0ea5e9; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 10px;'>
                <span style='animation: rotate 3s linear infinite;'>📊</span>
                Processing Statistics
                <span style='font-size: 0.8rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; animation: pulse 2s infinite;'>Success</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric(
            "📄 Transcript Words", 
            utils.count_words(st.session_state.transcript),
            help="Total words in the transcript"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric(
            "📝 Summary Words", 
            utils.count_words(st.session_state.summary),
            help="Total words in the summary"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        compression = (1 - utils.count_words(st.session_state.summary) / utils.count_words(st.session_state.transcript)) * 100
        st.metric(
            "🗜️ Compression", 
            f"{compression:.1f}%",
            delta=f"{compression:.1f}%",
            help="Percentage reduction in word count"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric(
            "⏱️ Time", 
            f"{st.session_state.processing_time:.1f}s",
            help="Total processing time"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display results in tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📄 Summary", "📝 Full Transcript", "📊 Comparison"])
    
    with tab1:
        st.markdown("### Executive Summary")
        if st.session_state.summary:
            # Display summary in a styled container
            st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            
            # Also show in a text area for better visibility and copying
            st.text_area(
                "Summary Content (for easy copying):",
                value=st.session_state.summary,
                height=300,
                disabled=True,
                key="summary_display"
            )
        else:
            st.info("No summary available. Please process an audio file first.")
        
        # Copy button functionality
        if st.button("📋 Copy Summary", key="copy_summary"):
            st.code(st.session_state.summary, language=None)
            st.info("💡 Tip: Select and copy the text above!")
    
    with tab2:
        st.markdown("### Complete Transcript")
        if st.session_state.transcript:
            # Display transcript in a styled container
            st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
            
            # Also show in a text area for better visibility and copying
            st.text_area(
                "Transcript Content (for easy copying):",
                value=st.session_state.transcript,
                height=400,
                disabled=True,
                key="transcript_display"
            )
        else:
            st.info("No transcript available. Please process an audio file first.")
        
        # Copy button functionality
        if st.button("📋 Copy Transcript", key="copy_transcript"):
            st.code(st.session_state.transcript, language=None)
            st.info("💡 Tip: Select and copy the text above!")
    
    with tab3:
        st.markdown("### Side-by-Side Comparison")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 📝 Original Transcript")
            st.text_area(
                "Transcript",
                st.session_state.transcript,
                height=300,
                label_visibility="collapsed"
            )
        
        with col_right:
            st.markdown("#### 📄 AI Summary")
            st.text_area(
                "Summary",
                st.session_state.summary,
                height=300,
                label_visibility="collapsed"
            )


def render_export_section():
    """Render export options with enhanced UI and animations."""
    if not st.session_state.transcript or not st.session_state.summary:
        return
    
    st.divider()
    
    # Animated export header
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; margin: 20px 0; animation: slideUp 0.5s ease-out; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
            <h3 style='color: #0ea5e9; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 10px; font-size: 1.5rem;'>
                <span style='animation: float 2s infinite ease-in-out;'>💾</span>
                Step 3: Export Your Results
                <span style='font-size: 0.8rem; background: linear-gradient(135deg, #ec4899 0%, #f97316 100%); color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; animation: pulse 2s infinite;'>Ready!</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Validate export inputs
    validation_error = validate_export_inputs(st.session_state.transcript, st.session_state.summary)
    if validation_error:
        st.error(validation_error)
        return
    
    st.info("📥 Choose your preferred export format below:")
    
    # Create tabs for different export options
    export_tab1, export_tab2, export_tab3 = st.tabs(["📄 Text Format", "📑 PDF Format", "📊 Both Formats"])
    
    with export_tab1:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; animation: slideUp 0.6s ease-out;'>
                <h4 style='color: #0ea5e9; font-weight: 700; display: flex; align-items: center; gap: 8px;'>
                    <span style='animation: pulse 2s infinite;'>📄</span>
                    Plain Text Export
                </h4>
                <p style='color: #64748b; margin: 10px 0; font-weight: 500;'>Perfect for quick sharing and editing</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Features:**")
            st.markdown("- ✅ Lightweight file size")
            st.markdown("- ✅ Easy to edit")
            st.markdown("- ✅ Universal compatibility")
        
        with col2:
            try:
                txt_bytes = export_to_txt(
                    st.session_state.transcript,
                    st.session_state.summary,
                    include_timestamp=True
                )
                st.download_button(
                    label="📄 Download TXT",
                    data=txt_bytes,
                    file_name="meeting_summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                    type="primary"
                )
                st.success("✅ Ready!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with export_tab2:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; animation: slideUp 0.7s ease-out;'>
                <h4 style='color: #0ea5e9; font-weight: 700; display: flex; align-items: center; gap: 8px;'>
                    <span style='animation: pulse 2s infinite 0.3s;'>📁</span>
                    Professional PDF Export
                </h4>
                <p style='color: #64748b; margin: 10px 0; font-weight: 500;'>Formatted document with styling and sections</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Features:**")
            st.markdown("- ✅ Professional formatting")
            st.markdown("- ✅ Preserves layout")
            st.markdown("- ✅ Print-ready")
        
        with col2:
            try:
                pdf_bytes = export_to_pdf(
                    st.session_state.transcript,
                    st.session_state.summary
                )
                st.download_button(
                    label="📑 Download PDF",
                    data=pdf_bytes,
                    file_name="meeting_summary.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
                st.success("✅ Ready!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with export_tab3:
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; animation: slideUp 0.8s ease-out;'>
                <h4 style='color: #0ea5e9; font-weight: 700; display: flex; align-items: center; gap: 8px;'>
                    <span style='animation: pulse 2s infinite 0.6s;'>📊</span>
                    Download Both Formats
                </h4>
                <p style='color: #64748b; margin: 10px 0; font-weight: 500;'>Get both TXT and PDF versions at once</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            try:
                txt_bytes = export_to_txt(
                    st.session_state.transcript,
                    st.session_state.summary,
                    include_timestamp=True
                )
                st.download_button(
                    label="📄 Get TXT",
                    data=txt_bytes,
                    file_name="meeting_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"TXT Error: {str(e)}")
        
        with col2:
            try:
                pdf_bytes = export_to_pdf(
                    st.session_state.transcript,
                    st.session_state.summary
                )
                st.download_button(
                    label="📑 Get PDF",
                    data=pdf_bytes,
                    file_name="meeting_summary.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF Error: {str(e)}")
        
        with col3:
            st.markdown("**Bundle:**")
            st.markdown("Download both formats separately")
    
    # Additional export info
    st.markdown("---")
    with st.expander("ℹ️ Export Information"):
        st.markdown("""
        **What's included in exports:**
        - 📝 Complete transcript
        - 📄 AI-generated summary
        - 📊 Word count statistics
        - 🕐 Generation timestamp
        - 📈 Compression ratio
        
        **File naming:**
        - Files are named `meeting_summary.[txt/pdf]`
        - Rename after download if needed
        """)


def main():
    """Main application logic."""
    # Initialize
    initialize_session_state()
    
    # Render components
    render_header()
    
    # Show welcome message on first visit with modern design
    if st.session_state.show_welcome:
        with st.container():
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 25px; color: #1e293b; margin-bottom: 30px; text-align: center; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); animation: slideUp 0.5s ease-out;'>
                <h2 style='color: #0ea5e9; font-weight: 800; font-size: 2.5rem; margin-bottom: 1rem;'>👋 Welcome to AI Meeting Summarizer!</h2>
                <p style='font-size: 1.2rem; margin-top: 15px; color: #475569; font-weight: 500;'>
                    Transform your audio recordings into concise summaries in just 3 easy steps:
                </p>
                <div style='display: flex; justify-content: space-around; margin-top: 30px; gap: 20px;'>
                    <div style='flex: 1; background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); padding: 25px; border-radius: 20px; color: white; box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);'>
                        <h3 style='font-size: 2.5rem; margin: 0;'>1️⃣</h3>
                        <p style='font-weight: 600; font-size: 1.1rem; margin: 10px 0 0 0;'>Upload Audio</p>
                    </div>
                    <div style='flex: 1; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); padding: 25px; border-radius: 20px; color: white; box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);'>
                        <h3 style='font-size: 2.5rem; margin: 0;'>2️⃣</h3>
                        <p style='font-weight: 600; font-size: 1.1rem; margin: 10px 0 0 0;'>Process</p>
                    </div>
                    <div style='flex: 1; background: linear-gradient(135deg, #ec4899 0%, #f97316 100%); padding: 25px; border-radius: 20px; color: white; box-shadow: 0 8px 20px rgba(236, 72, 153, 0.3);'>
                        <h3 style='font-size: 2.5rem; margin: 0;'>3️⃣</h3>
                        <p style='font-weight: 600; font-size: 1.1rem; margin: 10px 0 0 0;'>Export</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("✨ Got it! Let's start", use_container_width=True):
                    st.session_state.show_welcome = False
                    st.rerun()
    
    # Set default values instead of sidebar
    model_size = config.DEFAULT_WHISPER_MODEL
    max_length = config.DEFAULT_SUMMARY_MAX_LENGTH
    min_length = config.DEFAULT_SUMMARY_MIN_LENGTH
    
    # File upload section with modern UI
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 20px; margin: 20px 0; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #0ea5e9; font-weight: 700; margin: 0; font-size: 1.5rem;'>🎙️ Step 1: Upload Your Audio File</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a nice container for file upload
    with st.container():
        uploaded_file = st.file_uploader(
            "Drag and drop or browse for an audio file",
            type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
            help=f"Maximum file size: {config.MAX_AUDIO_SIZE_MB}MB",
            label_visibility="collapsed"
        )
    
    if uploaded_file is not None:
        # Display file info in an animated attractive card
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; margin: 15px 0; animation: slideUp 0.5s ease-out; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <div style='font-size: 3rem; animation: float 3s infinite ease-in-out;'>🎵</div>
                    <div style='flex: 1;'>
                        <h4 style='margin: 0; color: #0ea5e9; font-weight: 700;'>File Uploaded Successfully!</h4>
                        <p style='margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;'>Ready for processing</p>
                    </div>
                    <div style='font-size: 2rem; color: #10b981; animation: pulse 1s infinite;'>✅</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); padding: 15px; border-radius: 12px; color: white; animation: slideUp 0.6s ease-out;'>
                    <div style='font-size: 1.5rem; margin-bottom: 5px;'>📁</div>
                    <p style='margin: 0; font-size: 0.85rem; opacity: 0.9;'>File Name</p>
                    <p style='margin: 5px 0 0 0; font-weight: 700; font-size: 1rem;'>{uploaded_file.name}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); padding: 15px; border-radius: 12px; color: white; animation: slideUp 0.7s ease-out;'>
                    <div style='font-size: 1.5rem; margin-bottom: 5px;'>💾</div>
                    <p style='margin: 0; font-size: 0.85rem; opacity: 0.9;'>Size</p>
                    <p style='margin: 5px 0 0 0; font-weight: 700; font-size: 1rem;'>{file_size:.2f} MB</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            file_ext = uploaded_file.name.split('.')[-1].upper()
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ec4899 0%, #f97316 100%); padding: 15px; border-radius: 12px; color: white; animation: slideUp 0.8s ease-out;'>
                    <div style='font-size: 1.5rem; margin-bottom: 5px;'>🎵</div>
                    <p style='margin: 0; font-size: 0.85rem; opacity: 0.9;'>Format</p>
                    <p style='margin: 5px 0 0 0; font-weight: 700; font-size: 1rem;'>{file_ext}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Audio player with animated label
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; margin: 20px 0; animation: slideUp 0.9s ease-out; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
                <h3 style='color: #0ea5e9; font-weight: 700; margin: 0 0 15px 0; display: flex; align-items: center; gap: 10px;'>
                    <span style='animation: float 2s infinite ease-in-out;'>🎧</span>
                    Preview Your Audio
                    <span style='font-size: 0.8rem; background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600;'>Live Preview</span>
                </h3>
            </div>
        """, unsafe_allow_html=True)
        st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')
        
        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
        
        # Process button with modern design
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 20px; margin: 20px 0; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: #0ea5e9; font-weight: 700; margin: 0; font-size: 1.5rem;'>⚡ Step 2: Process Your Audio</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
                <div style='animation: pulse 2s infinite;'>
            """, unsafe_allow_html=True)
            process_button = st.button(
                "🚀 Start Processing",
                type="primary",
                use_container_width=True,
                help="Click to transcribe and summarize your audio"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        if process_button:
            # Show animated processing indicator
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); padding: 30px; border-radius: 20px; text-align: center; animation: pulse 2s infinite; margin: 20px 0; box-shadow: 0 8px 32px rgba(14, 165, 233, 0.4);'>
                    <div style='margin-bottom: 15px;'>
                        <div class='spinner' style='display: inline-block;'></div>
                    </div>
                    <h3 style='color: white; margin: 0; font-weight: 700;'>Processing Your Audio...</h3>
                    <p style='color: rgba(255, 255, 255, 0.9); margin: 10px 0 0 0; font-size: 0.95rem;'>This may take a few minutes</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.spinner("Processing..."):
                success = process_audio(uploaded_file, model_size, max_length, min_length)
                if success:
                    # Success animation
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px; border-radius: 20px; text-align: center; animation: slideUp 0.5s ease-out; margin: 20px 0; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);'>
                            <div style='font-size: 4rem; margin-bottom: 15px; animation: bounce 1s infinite;'>✨</div>
                            <h2 style='color: white; margin: 0; font-weight: 800; font-size: 2rem;'>Processing Complete!</h2>
                            <p style='color: rgba(255, 255, 255, 0.95); margin: 15px 0 0 0; font-size: 1.1rem; font-weight: 600;'>Your summary is ready below ⬇️</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.snow()
    else:
        # Show helpful animated message when no file is uploaded
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 20px; text-align: center; animation: slideUp 0.5s ease-out; margin: 20px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
                <div style='font-size: 4rem; margin-bottom: 15px; animation: float 3s infinite ease-in-out;'>☁️</div>
                <h3 style='color: #0ea5e9; margin: 0 0 10px 0; font-weight: 700;'>No File Uploaded Yet</h3>
                <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Drag & drop your audio file or click browse to get started! 👆</p>
                <div style='margin-top: 20px;'>
                    <span style='display: inline-block; animation: bounce 2s infinite; font-size: 2rem;'>⬆️</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display supported formats with animations
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; margin: 20px 0; animation: slideUp 0.7s ease-out; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.3);'>
                <h3 style='color: #0ea5e9; margin: 0 0 20px 0; font-weight: 700; text-align: center;'>📋 Supported Audio Formats</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        formats = [
            ("🎵", "WAV", "#0ea5e9", "0.5s"),
            ("🎵", "MP3", "#8b5cf6", "0.6s"),
            ("🎵", "M4A", "#ec4899", "0.7s"),
            ("🎵", "FLAC", "#f97316", "0.8s"),
            ("🎵", "OGG", "#10b981", "0.9s")
        ]
        
        for col, (icon, format_name, color, delay) in zip([col1, col2, col3, col4, col5], formats):
            with col:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {color} 0%, #8b5cf6 100%); padding: 20px; border-radius: 15px; text-align: center; animation: slideUp {delay} ease-out; transition: transform 0.3s ease;' onmouseover='this.style.transform="translateY(-10px) scale(1.05)"' onmouseout='this.style.transform="translateY(0) scale(1)"'>
                        <div style='font-size: 2.5rem; margin-bottom: 10px; animation: pulse 2s infinite;'>{icon}</div>
                        <p style='color: white; font-weight: 700; font-size: 1.2rem; margin: 0;'>{format_name}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Display results
    render_results()
    
    # Export section
    render_export_section()
    
    # Modern glassmorphic footer
    st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.95); border-radius: 25px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);'>
        <div style='margin-bottom: 20px;'>
            <span style='font-size: 2.5rem;'>🎙️</span>
        </div>
        <p style='margin: 0; color: #475569; font-size: 1.1rem; font-weight: 600;'>
            Built with <strong style='background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Streamlit</strong>, <strong style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>BART AI</strong>, and <strong style='background: linear-gradient(135deg, #ec4899 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SpeechRecognition</strong>
        </p>
        <p style='margin: 1rem 0 0 0; color: #94a3b8; font-size: 0.95rem; font-weight: 500;'>
            Transform meetings into insights • © 2025 AI Meeting Summarizer
        </p>
        <div style='margin-top: 20px; padding-top: 20px; border-top: 2px solid rgba(14, 165, 233, 0.2);'>
            <p style='margin: 0; color: #94a3b8; font-size: 0.875rem;'>Powered by Advanced AI Technology ✨</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
