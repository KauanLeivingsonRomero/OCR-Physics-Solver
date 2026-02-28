# OCR Physics Solver

Python script that reads the latest image from `images/`, extracts text with Tesseract OCR, and sends it to a local Ollama model (`gemma3:4b`) to generate a step-by-step physics solution.

## Features
- Picks the newest image automatically (`.png`, `.jpg`, `.jpeg`)
- Improves OCR accuracy with OpenCV preprocessing
- Extracts bilingual text with Tesseract (`por+eng`)
- Sends the prompt to a local LLM with Ollama
- Prints extracted text and final answer in the terminal

## Project Structure
```text
.
├── images/          # Input images (physics questions)
├── main.py          # Main script
├── .gitignore
└── README.md
```

## Requirements
- Python 3.9+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed and available in PATH
- [Ollama](https://ollama.com/download) installed
- Ollama model: `gemma3:4b`

## Setup
1. Create and activate a virtual environment (recommended):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:
```powershell
pip install opencv-python pytesseract ollama
```

3. Pull the Ollama model:
```powershell
ollama pull gemma3:4b
```

## Usage
1. Put at least one image in `images/`.
2. Run:
```powershell
python main.py
```

The script will:
- select the latest image,
- run OCR,
- send the extracted text to Gemma,
- print a structured solution.

## Windows Notes
If Tesseract is installed but not detected, set the executable path in `main.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Troubleshooting
- `No images found at /images.`
  - Add images to the `images/` folder.
- OCR output is empty or poor
  - Try a clearer image (higher contrast and resolution).
- Ollama errors / connection issues
  - Make sure Ollama is running and `gemma3:4b` is available.

