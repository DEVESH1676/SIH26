"""
Multi-format file processor for learning materials.
Handles PDF, DOCX, PPTX, video (with transcription), and audio extraction.
"""
import os
import sys
import tempfile
import asyncio
import subprocess
from typing import Optional, Tuple
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class FileProcessor:
    """Process uploaded learning materials into extractable text."""

    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def process_file(
        self,
        file_path: str,
        file_type: str,
        max_chars: int = None,
    ) -> str:
        """
        Process any supported file type and return extracted text.
        
        Args:
            file_path: Path to the uploaded file
            file_type: File extension (pdf, docx, pptx, txt, mp4, mp3)
            max_chars: Maximum characters to return (default: from settings)
        
        Returns:
            Extracted text content
        """
        max_chars = max_chars or settings.max_document_chars
        file_type = file_type.lower().lstrip(".")

        handlers = {
            "pdf": self._process_pdf,
            "docx": self._process_docx,
            "pptx": self._process_pptx,
            "txt": self._process_txt,
            "mp4": self._process_video,
            "mp3": self._process_audio,
            "wav": self._process_audio,
        }

        handler = handlers.get(file_type)
        if not handler:
            raise ValueError(
                f"Unsupported file type: {file_type}. "
                f"Supported: {', '.join(handlers.keys())}"
            )

        # Limit text length
        text = await handler(file_path)
        return text[:max_chars]

    async def _process_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("pypdf not installed. Run: pip install pypdf")

    async def _process_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            from docx import Document
            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except ImportError:
            raise ImportError("python-docx not installed. Run: pip install python-docx")

    async def _process_pptx(self, file_path: str) -> str:
        """Extract text from PPTX file."""
        try:
            from pptx import Presentation
            pres = Presentation(file_path)
            text_parts = []
            for slide in pres.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            text = paragraph.text.strip()
                            if text:
                                text_parts.append(text)
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("python-pptx not installed. Run: pip install python-pptx")

    async def _process_txt(self, file_path: str) -> str:
        """Read plain text file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    async def _process_video(self, file_path: str) -> Tuple[str, list[dict]]:
        """
        Extract transcription from video file.
        Uses Whisper (local Ollama) for transcription.
        
        Returns:
            (full_text, chapter_marks) where chapter_marks is list of
            {"timestamp": str, "text": str}
        """
        try:
            # Use Whisper via Ollama for local transcription
            result = subprocess.run(
                ["ollama", "run", "whisper", file_path],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
            )
            if result.returncode == 0:
                return result.stdout, []
            else:
                raise Exception(f"Whisper transcription failed: {result.stderr}")
        except FileNotFoundError:
            raise Exception(
                "Ollama not available. Install Ollama and run: ollama pull whisper"
            )

    async def _process_audio(self, file_path: str) -> str:
        """Extract transcription from audio file."""
        # Similar to video processing
        return await self._process_video(file_path)

    async def chunk_document(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[dict]:
        """
        Split document into overlapping chunks for embedding.
        
        Returns list of {"text": str, "start": int, "end": int, "chunk_index": int}
        """
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                break_point = max(
                    text.rfind(". ", start + chunk_size // 2, end),
                    text.rfind("\n", start + chunk_size // 2, end),
                )
                if break_point > start + chunk_size // 2:
                    end = break_point + 1

            chunks.append({
                "text": text[start:end].strip(),
                "start": start,
                "end": end,
                "chunk_index": chunk_index,
            })
            chunk_index += 1
            start = end - overlap

        return chunks
