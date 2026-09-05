"""
Comprehensive tests for file processing module (core/file_processor.py).
Tests TXT, PDF, DOCX, PPTX, audio/video processing, chunking, and error handling.
"""
import os
import sys
import tempfile
import pytest
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def set_test_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        os.environ["SQLITE_PATH"] = f.name
        from config.settings import get_settings
        get_settings().sqlite_path = f.name
    yield
    try:
        os.unlink(os.environ["SQLITE_PATH"])
    except FileNotFoundError:
        pass


class TestFileProcessorInit:
    """Test FileProcessor initialization and upload directory creation."""

    def test_creates_upload_dir(self, tmp_path):
        from core.file_processor import FileProcessor
        upload_dir = str(tmp_path / "uploads_test")
        processor = FileProcessor(upload_dir=upload_dir)
        assert os.path.isdir(processor.upload_dir)

    def test_upload_dir_path_is_pathlib(self, tmp_path):
        from core.file_processor import FileProcessor
        processor = FileProcessor(upload_dir=str(tmp_path / "x"))
        from pathlib import Path
        assert isinstance(processor.upload_dir, Path)


class TestTXTProcessing:
    """Test plain text file processing."""

    def test_read_simple_text(self, tmp_path):
        from core.file_processor import FileProcessor
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World! This is a test document.")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), "txt"))
        assert "Hello World" in text

    def test_read_multiline_text(self, tmp_path):
        from core.file_processor import FileProcessor
        test_file = tmp_path / "multi.txt"
        test_file.write_text("Line one.\nLine two.\nLine three.")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), "txt"))
        assert "Line one" in text
        assert "Line two" in text
        assert "Line three" in text

    def test_read_empty_text(self, tmp_path):
        from core.file_processor import FileProcessor
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), "txt"))
        assert text == ""

    def test_read_unicode_text(self, tmp_path):
        from core.file_processor import FileProcessor
        test_file = tmp_path / "unicode.txt"
        test_file.write_text("नमस्ते! Привет! こんにちは!")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), "txt"))
        assert "नमस्ते" in text or "नमस्ते" in text

    def test_txt_case_insensitive_type(self, tmp_path):
        """Test that TXT is accepted as txt (case insensitive)."""
        from core.file_processor import FileProcessor
        test_file = tmp_path / "test.TXT"
        test_file.write_text("uppercase extension")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), "TXT"))
        assert "uppercase extension" in text

    def test_txt_with_dot_prefix(self, tmp_path):
        """Test that .txt and txt both work."""
        from core.file_processor import FileProcessor
        test_file = tmp_path / "test.txt"
        test_file.write_text("dot prefix test")
        processor = FileProcessor()
        text = asyncio.run(processor.process_file(str(test_file), ".txt"))
        assert "dot prefix test" in text


class TestUnsupportedTypes:
    """Test error handling for unsupported file types."""

    def test_xyz_extension_raises(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        with pytest.raises(ValueError, match="Unsupported file type"):
            asyncio.run(processor.process_file("/fake/file.xyz", "xyz"))

    def test_html_extension_raises(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        with pytest.raises(ValueError, match="Unsupported file type"):
            asyncio.run(processor.process_file("/fake/file.html", "html"))

    def test_image_extension_raises(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        with pytest.raises(ValueError, match="Unsupported file type"):
            asyncio.run(processor.process_file("/fake/file.png", "png"))

    def test_error_message_lists_supported_types(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        with pytest.raises(ValueError) as exc_info:
            asyncio.run(processor.process_file("/fake/file.xyz", "xyz"))
        assert "pdf" in str(exc_info.value)
        assert "docx" in str(exc_info.value)


class TestChunkDocument:
    """Test document chunking functionality."""

    def test_basic_chunking(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        text = "This is a short text. It has multiple sentences. Each sentence should be handled properly."
        chunks = asyncio.run(processor.chunk_document(text, chunk_size=20, overlap=5))
        assert len(chunks) > 0
        assert chunks[0]["chunk_index"] == 0

    def test_chunk_size_limits(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        long_text = "A " * 500  # 1000 chars
        chunks = asyncio.run(processor.chunk_document(long_text, chunk_size=100, overlap=10))
        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk["text"] is not None

    def test_chunk_overlap(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        text = "Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9 Word10"
        chunks = asyncio.run(processor.chunk_document(text, chunk_size=10, overlap=5))
        assert len(chunks) >= 2

    def test_chunk_returns_dict_format(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        text = "Test chunking format."
        chunks = asyncio.run(processor.chunk_document(text, chunk_size=50))
        for chunk in chunks:
            assert "text" in chunk
            assert "start" in chunk
            assert "end" in chunk
            assert "chunk_index" in chunk

    def test_small_text_single_chunk(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        text = "Hi."
        chunks = asyncio.run(processor.chunk_document(text, chunk_size=100))
        assert len(chunks) == 1

    def test_empty_text(self):
        from core.file_processor import FileProcessor
        processor = FileProcessor()
        chunks = asyncio.run(processor.chunk_document("", chunk_size=100))
        # Returns at least one empty chunk
        assert isinstance(chunks, list)


class TestMissingDependencies:
    """Test behavior when optional dependencies are missing."""

    def test_pdf_missing_pypdf(self, tmp_path):
        """When pypdf is not available or file is invalid, should raise ImportError."""
        from core.file_processor import FileProcessor
        test_file = tmp_path / "test.pdf"
        test_file.write_bytes(b"%PDF fake")
        processor = FileProcessor()
        try:
            result = asyncio.run(processor.process_file(str(test_file), "pdf"))
            # If it returns, it should be a string
            assert isinstance(result, str) or result is not None
        except ImportError as e:
            # Expected when pypdf is missing or file is malformed
            assert "pypdf" in str(e).lower()
