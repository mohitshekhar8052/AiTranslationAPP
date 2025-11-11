# Installation Notes

## Python Version Compatibility

This project was developed with **Python 3.14.0**. Some packages have version-specific compatibility:

### ⚠️ Important Note on Whisper

The original `openai-whisper` package is **not compatible with Python 3.14**. We've implemented an alternative approach:

- **Current Implementation**: Uses `SpeechRecognition` with Google Speech Recognition API
- **Requirements**: Internet connection for transcription
- **Alternative**: For offline Whisper support, use **Python 3.10-3.13**

### Installed Packages

✅ Successfully installed:
- `streamlit` - Web UI framework
- `transformers` - For text summarization (BART model)
- `torch` & `torchaudio` - Deep learning framework
- `SpeechRecognition` - Audio transcription (fallback)
- `reportlab` & `PyPDF2` - PDF export
- `python-dotenv` - Environment management  
- `pytest` & `pytest-cov` - Testing framework
- `accelerate` - Model optimization
- All other required dependencies

### Optional: Using Python 3.10-3.13 for Full Whisper Support

If you need offline Whisper transcription:

1. Install Python 3.10, 3.11, 3.12, or 3.13
2. Create a new virtual environment:
   ```bash
   python3.11 -m venv venv311
   source venv311/bin/activate
   ```
3. Install with original requirements:
   ```bash
   pip install openai-whisper==20231117
   ```

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=summarizer --cov-report=html

# Run only fast tests
pytest -m "not slow"
```

## Known Limitations

1. **Transcription**: Currently uses Google Speech Recognition (requires internet)
2. **Model Size**: BART model (~1.6GB) will be downloaded on first run
3. **Performance**: Initial model loading takes time; subsequent runs are faster

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Streamlit won't start
```bash
# Check Streamlit installation
streamlit --version

# Reinstall if needed
pip install --upgrade streamlit
```

### Memory errors
- Use smaller models
- Reduce audio file size
- Close other applications

## Next Steps

1. Add sample audio files to `sample_audio/` directory
2. Configure `.env` file (copy from `.env.example`)
3. Run the application: `streamlit run app.py`
4. Upload an audio file and test transcription

For more details, see the main [README.md](README.md).
