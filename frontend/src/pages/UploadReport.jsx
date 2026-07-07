import './UploadReport.css';

import { useState } from 'react';

import { uploadReport } from '../api/client';
import UploadBox from '../components/UploadBox';

const STATUS = {
  IDLE: 'idle',
  UPLOADING: 'uploading',
  SUCCESS: 'success',
  ERROR: 'error',
};

export default function UploadReport() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(STATUS.IDLE);
  const [result, setResult] = useState(null);

  // Per the intended flow — selecting a PDF sends it straight to the
  // backend, no separate "analyze" click needed.
  const handleFileSelect = async (selected) => {
    setFile(selected);

    if (!selected) {
      setStatus(STATUS.IDLE);
      setResult(null);
      return;
    }

    setStatus(STATUS.UPLOADING);
    setResult(null);

    try {
      const data = await uploadReport(selected);
      setResult(data);
      setStatus(STATUS.SUCCESS);
    } catch {
      setStatus(STATUS.ERROR);
    }
  };

  return (
    <section className="upload-page">
      <h2>Upload a medical report</h2>
      <p className="upload-page-sub">
        PDF lab reports are parsed automatically — including scanned copies,
        via OCR — and the extracted values are run through the same
        prediction model used for symptom chats.
      </p>

      <UploadBox file={file} onFileSelect={handleFileSelect} />

      {status !== STATUS.IDLE && (
        <div className={`upload-status upload-status-${status}`}>
          {status === STATUS.UPLOADING && (
            <>
              <span className="upload-status-dot" />
              Sending to the backend…
            </>
          )}
          {status === STATUS.SUCCESS && result && (
            <>
              <strong>{result.filename}</strong> received (
              {(result.size_bytes / 1024).toFixed(1)} KB). {result.note}
            </>
          )}
          {status === STATUS.ERROR && (
            "Couldn't reach the backend — make sure the API server is running, then try selecting the file again."
          )}
        </div>
      )}

      <div className="upload-page-steps">
        <h3>What happens next</h3>
        <ol>
          <li>Text and tables are pulled from the PDF (PyMuPDF, OCR fallback for scans).</li>
          <li>Key lab values are extracted and matched to the model's expected features.</li>
          <li>The XGBoost model returns a disease risk and confidence score.</li>
          <li>SHAP explains which values drove the prediction, and Gemini summarizes it in plain language.</li>
        </ol>
      </div>
    </section>
  );
}
