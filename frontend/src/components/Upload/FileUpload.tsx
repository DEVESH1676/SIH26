/**
 * File upload component with drag-and-drop.
 */
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload({ onFileSelect }: { onFileSelect: (file: File) => void }) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles[0]) onFileSelect(acceptedFiles[0]);
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'video/mp4': ['.mp4'],
      'audio/mpeg': ['.mp3'],
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition ${
        isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'
      }`}
    >
      <input {...getInputProps()} />
      <p className="text-lg font-medium text-gray-700">
        {isDragActive ? 'Drop the file here' : 'Drag & drop a file or click to browse'}
      </p>
      <p className="text-sm text-gray-500 mt-2">
        Supported: PDF, DOCX, PPTX, MP4, MP3 (max 100MB)
      </p>
    </div>
  );
}
