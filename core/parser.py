"""
Media Parser Engine - Extracts text from documents and videos for Quiz Generation.
Supports PDF, DOCX, PPTX, and basic audio/video transcription (via Whisper).
"""
import os
import json
import subprocess
from pathlib import Path

# Note: In a real environment, we'd use pypdf, python-docx, pptx, and whisper.
# For the hackathon/MVP, we provide robust mock/stub methods that can be easily replaced.

class MediaParser:
    def __init__(self):
        self.supported_extensions = ['.pdf', '.docx', '.pptx', '.mp4', '.mp3']

    def parse_file(self, file_path: str) -> str:
        """Parse a file based on its extension and return text content."""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file format: {ext}")
            
        if ext == '.pdf':
            return self._parse_pdf(path)
        elif ext == '.docx':
            return self._parse_docx(path)
        elif ext == '.pptx':
            return self._parse_pptx(path)
        elif ext in ['.mp4', '.mp3']:
            return self._parse_media(path)
            
    def _parse_pdf(self, path: Path) -> str:
        # Stub for PyPDF2 / pdfplumber
        return f"[Extracted PDF Content from {path.name}]\nThis document covers statistical methodologies and index numbers calculation."

    def _parse_docx(self, path: Path) -> str:
        # Stub for python-docx
        return f"[Extracted DOCX Content from {path.name}]\nThis document discusses Data Privacy and the DPDP Act 2023."

    def _parse_pptx(self, path: Path) -> str:
        # Stub for python-pptx
        return f"[Extracted PPTX Content from {path.name}]\nSlide 1: Big Data Analytics in MoSPI.\nSlide 2: Implementing scalable pipelines."

    def _parse_media(self, path: Path) -> str:
        # Stub for ffmpeg audio extraction + local Whisper transcription
        # Real implementation would run: `ffmpeg -i input.mp4 output.wav` 
        # followed by `whisper output.wav --model base`
        return f"[Whisper Transcription from {path.name}]\nWelcome to the NSSTA induction training on National Accounts..."

    def chunk_text(self, text: str, chunk_size: int = 2000) -> list[str]:
        """Simple text chunker for LLM processing."""
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


if __name__ == "__main__":
    parser = MediaParser()
    print("Testing Media Parser...")
    print(parser.parse_file("sample_training.pdf"))
    print(parser.parse_file("nssta_lecture.mp4"))
