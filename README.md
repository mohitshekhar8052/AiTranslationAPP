# AI Meeting Summarizer

An intelligent application that transcribes audio recordings from meetings and generates concise summaries using state-of-the-art AI models.

## Overview

This project leverages OpenAI's Whisper model for accurate speech-to-text transcription and Hugging Face's transformer models for generating meaningful summaries. Built with Streamlit for an intuitive web interface, it helps users quickly extract key insights from lengthy meeting recordings.

## Features

- **Audio Upload**: Support for multiple audio formats (.wav, .mp3, .m4a)
- **AI-Powered Transcription**: Uses OpenAI Whisper for accurate speech recognition
- **Intelligent Summarization**: Generates concise summaries using BART transformer model
- **Export Functionality**: Download transcripts and summaries as TXT or PDF files
- **User-Friendly Interface**: Clean Streamlit web UI with real-time progress indicators
- **Configurable Settings**: Adjust model parameters and summarization length
- **Model Caching**: Optimized performance with cached model loading

## Tech Stack

- **Python 3.10+**: Core programming language
- **Streamlit**: Web application framework
- **OpenAI Whisper**: Speech-to-text transcription
- **Hugging Face Transformers**: Text summarization (BART model)
- **PyTorch**: Deep learning backend
- **ReportLab**: PDF generation
- **python-dotenv**: Environment variable management

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment tool (recommended)

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   cd ai-meeting-summarizer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Quick Start

1. **Activate your virtual environment**:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to the URL shown (typically `http://localhost:8501`)

4. **Upload an audio file** and click "Transcribe" to process

## How It Works

1. **Upload**: User uploads an audio file through the Streamlit interface
2. **Transcription**: Whisper model converts speech to text
3. **Summarization**: BART model generates a concise summary from the transcript
4. **Display**: Results are shown in the web interface
5. **Export**: User can download results as TXT or PDF files

## Folder Structure

```
ai-meeting-summarizer/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── LICENSE                    # Project license
├── CONTRIBUTING.md            # Contribution guidelines
├── pytest.ini                 # Pytest configuration
├── summarizer/                # Core package
│   ├── __init__.py
│   ├── transcribe.py         # Audio transcription module
│   ├── summarize.py          # Text summarization module
│   └── export.py             # Export functionality
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_transcribe.py
│   ├── test_summarize.py
│   ├── test_export.py
│   └── test_integration.py
└── sample_audio/             # Sample audio files for testing
    └── README.md
```

## Usage

### Basic Workflow

1. Launch the application using `streamlit run app.py`
2. Select your preferred Whisper model size (base recommended for balance)
3. Upload an audio file (max 200MB recommended)
4. Click "Transcribe" and wait for processing
5. Review the transcript and generated summary
6. Export results using TXT or PDF download buttons

### Model Selection

- **Tiny**: Fastest, lowest accuracy (~1GB)
- **Base**: Good balance of speed and accuracy (~1.5GB) - **Recommended**
- **Small**: Better accuracy, slower (~2.5GB)
- **Medium**: High accuracy, requires more resources (~5GB)
- **Large**: Best accuracy, slowest (~10GB)

### Summarization Parameters

- **Max Length**: Maximum words in summary (default: 150)
- **Min Length**: Minimum words in summary (default: 50)

## Demo Checklist

- [ ] Prepare a sample meeting audio file (2-5 minutes)
- [ ] Test transcription with different model sizes
- [ ] Verify summarization quality
- [ ] Test TXT export functionality
- [ ] Test PDF export functionality
- [ ] Check error handling with invalid files

## Development

### Running Tests

```bash
pytest tests/
```

### Running Specific Test Categories

```bash
pytest tests/ -m unit          # Run unit tests only
pytest tests/ -m integration   # Run integration tests only
```

## Troubleshooting

### Common Issues

1. **Out of Memory**: Use smaller Whisper model (tiny/base) or reduce audio file size
2. **Slow Processing**: First run downloads models (~1-2GB), subsequent runs are faster
3. **CUDA Errors**: Install PyTorch with CUDA support for GPU acceleration
4. **Import Errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## References

- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines on how to contribute to this project.
