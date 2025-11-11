# Sample Audio Files

This directory is for storing sample audio files used for testing and demonstration purposes.

## Purpose

Use this directory to store test audio recordings that can be used to:
- Test the transcription functionality
- Verify summarization quality
- Demo the application
- Develop and debug features

## Adding Test Audio Files

### Recording Your Own

1. Record a short meeting or conversation (2-5 minutes recommended)
2. Save in a supported format (.wav, .mp3, or .m4a)
3. Keep file size under 50MB for quick testing
4. Place the file in this directory

### Sample Content Ideas

- Business meeting discussion
- Technical presentation
- Interview recording
- Lecture or educational content
- Podcast segment

### Recommended Formats

- **WAV**: Uncompressed, high quality, larger file size
- **MP3**: Compressed, good quality, smaller file size (recommended for testing)
- **M4A**: Compressed, good quality, Apple format

## File Size Guidelines

For testing purposes:
- **Quick tests**: 1-3 minutes, < 10MB
- **Standard tests**: 3-5 minutes, < 25MB
- **Full tests**: 5-15 minutes, < 50MB

## Sources for Sample Audio

### Public Domain Sources
- [LibriVox](https://librivox.org/) - Free public domain audiobooks
- [Free Music Archive](https://freemusicarchive.org/) - Free audio content
- [Archive.org](https://archive.org/details/audio) - Various audio recordings

### Recording Your Own
- Use your phone's voice recorder
- Use Zoom/Teams to record a test meeting
- Use Audacity (free software) to record and edit

## Important Notes

- **Do not commit large audio files to Git** - Use .gitignore to exclude them
- **Respect copyright** - Only use audio you have rights to
- **Privacy** - Do not include recordings with sensitive or personal information
- **Test variety** - Include samples with different accents, speaking speeds, and audio quality

## Example File Names

- `test_meeting_5min.mp3`
- `sample_interview.wav`
- `quick_test_short.mp3`
- `long_presentation_10min.m4a`

## Usage in Tests

Place your sample files here and reference them in test cases:

```python
sample_audio_path = os.path.join('sample_audio', 'test_meeting_5min.mp3')
```

---

**Note**: This directory should contain small test files only. Production audio files should be uploaded through the application interface.
