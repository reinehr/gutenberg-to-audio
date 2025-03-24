# Gutenberg to Audio

Convert Project Gutenberg books to high-quality audiobooks using AI text-to-speech technology.

## Overview

This project provides tools to transform public domain books from Project Gutenberg into professional-quality audiobooks. It handles the entire process from downloading and cleaning the text to generating and processing audio files.

## Audio Samples

Listen to these sample audiobook chapters generated with different TTS engines:

- **OpenAI TTS Sample**: [Chapter 1 of "A Lady's Captivity Among Chinese Pirates" by Fanny Loviot](https://drive.google.com/file/d/141xn8SJgpYraJJZAXIwFERzZ7jpnmuFf/view?usp=sharing)  
  *Generated using OpenAI's gpt-4o-mini-tts model with the "coral" voice*
- **Kokoro TTS Sample**: [Chapter 1 of "A Lady's Captivity Among Chinese Pirates" by Fanny Loviot](https://drive.google.com/file/d/1CE310UgOmIQLzracZWWqESnaCp62eVhZ/view?usp=sharing)  
  *Generated using Kokoro TTS with the "af_heart" voice*
- **Original Text**: [Read the complete book on Project Gutenberg](https://www.gutenberg.org/ebooks/34167)

### Try the TTS Models

- **OpenAI TTS**: Try the gpt-4o-mini-tts model yourself at [OpenAI.fm](https://www.openai.fm/)
- **Kokoro TTS**: Experiment with Kokoro TTS at [Hugging Face Space](https://huggingface.co/spaces/hexgrad/Kokoro-TTS)

## Features

- **Automated Book Processing**: Download and clean books from Project Gutenberg
- **Intelligent Text Preparation**: Analyze and prepare text specifically for TTS
- **High-Quality Audio Generation**: Generate natural-sounding narration using OpenAI's TTS models
- **Alternative TTS Options**: Support for both OpenAI TTS and Kokoro TTS
- **Quality Control**: Detect and fix issues in generated audio
- **Chapter Assembly**: Combine audio segments into complete chapter files

## Requirements

```
requests
openai
pydub
numpy
jupyter
```

For the Kokoro TTS alternative:
```
kokoro>=0.3.4
soundfile
espeak-ng
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/reinehr/gutenberg-to-audio.git
cd gutenberg-to-audio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Main Workflow (OpenAI TTS)

1. Open `gutenberg_to_audio_gpt4o.ipynb` in Jupyter Notebook
2. Set the `BOOK_ID` variable to your desired Project Gutenberg book ID
3. Run the cells sequentially to:
   - Download and clean the book
   - Analyze text for TTS preparation
   - Process text for optimal narration
   - Generate audio using OpenAI's TTS
   - Perform quality control
   - Assemble final chapter files

### Alternative Workflow (Kokoro TTS)

For an open-source alternative to OpenAI's TTS:

1. Open `kokoro.ipynb` in Jupyter Notebook
2. Set the `BOOK_ID` variable to match your Project Gutenberg book
3. Run the cells to process the book with Kokoro TTS

## Project Structure

```
books/
  ├── {BOOK_ID}/
  │   ├── gutenberg_{BOOK_ID}.txt       # Original cleaned text
  │   ├── hints/                        # TTS preparation hints
  │   ├── txt/                          # Processed text sections
  │   ├── audio/                        # Generated audio sections (OpenAI)
  │   ├── kokoro_audio/                 # Generated audio sections (Kokoro)
  │   └── chapters/                     # Final assembled chapters
```

## Workflow Details

1. **Text Acquisition**: Download and clean text from Project Gutenberg
2. **Text Analysis**: Identify abbreviations, formatting, and other TTS challenges
3. **Text Processing**: Prepare text for optimal TTS performance
4. **Audio Generation**: Convert text to speech using AI models
5. **Quality Control**: Detect and fix issues in audio files
6. **Chapter Assembly**: Combine audio segments into complete chapters

## Cost Estimation

When using OpenAI's models, the approximate costs are:
- **Audio Generation**: ~€1.50 per hour of audio using gpt-4o-mini-tts
- **Text Processing**: ~€1.50 for text analysis and preparation with o3-mini
- **Total**: ~€3 per hour of audiobook

For reference, one hour of audio corresponds to approximately 60,000 characters of text.

## Notes

- Manual chapter marking is required before text processing
- For best results, review and regenerate any audio files with detected issues
- The Kokoro TTS alternative provides an open-source option but may have different quality characteristics

## License

This project is licensed under the MIT License - see the LICENSE file for details.