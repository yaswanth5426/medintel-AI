import './UploadBox.css';

import {
  useRef,
  useState,
} from 'react';
import {
  HiOutlineCloudArrowUp,
  HiOutlineDocumentText,
  HiOutlineXMark,
} from 'react-icons/hi2';

const MAX_SIZE_MB = 15;

export default function UploadBox({ file, onFileSelect }) {
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const handleFiles = (files) => {
    const f = files[0];
    if (!f) return;

    if (f.type !== "application/pdf") {
      setError("Only PDF files are supported.");
      return;
    }
    if (f.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`File is larger than ${MAX_SIZE_MB}MB.`);
      return;
    }

    setError('');
    onFileSelect(f);
  };

  const clear = (e) => {
    e.stopPropagation();
    onFileSelect(null);
    setError('');
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div>
      <div
        className={`upload-box glass ${dragOver ? "drag-over" : ""} ${file ? "has-file" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          hidden
          onChange={(e) => handleFiles(e.target.files)}
        />
        <span className="upload-box-icon">
          {file ? <HiOutlineDocumentText /> : <HiOutlineCloudArrowUp />}
        </span>
        {file ? (
          <>
            <p className="upload-filename">{file.name}</p>
            <p className="upload-hint">
              {(file.size / 1024 / 1024).toFixed(2)} MB &middot;{' '}
              <button className="upload-clear" onClick={clear} type="button">
                <HiOutlineXMark /> remove
              </button>
            </p>
          </>
        ) : (
          <>
            <p className="upload-cta">Drop a lab report PDF here, or click to browse</p>
            <p className="upload-hint">PDF only, up to {MAX_SIZE_MB}MB</p>
          </>
        )}
      </div>
      {error && <p className="upload-error">{error}</p>}
    </div>
  );
}
