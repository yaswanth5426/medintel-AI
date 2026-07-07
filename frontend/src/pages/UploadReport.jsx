import './UploadReport.css';

import { useState } from 'react';

import UploadBox from '../components/UploadBox';

export default function UploadReport() {
  const [file, setFile] = useState(null);

  return (
    <section className="upload-page">
      <h2>Upload a medical report</h2>
      <p className="upload-page-sub">
        PDF lab reports are parsed automatically — including scanned copies,
        via OCR — and the extracted values are run through the same
        prediction model used for symptom chats.
      </p>

      <UploadBox file={file} onFileSelect={setFile} />

      <div className="upload-page-actions">
        <button className="btn btn-primary" disabled={!file} type="button">
          Analyze report
        </button>
        <span className="upload-page-note">
          {file
            ? "Analysis pipeline isn't wired up yet — this button is a placeholder."
            : "Choose a PDF above to enable analysis."}
        </span>
      </div>

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
