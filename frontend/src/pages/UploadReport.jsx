import './UploadReport.css';

import { useMemo, useState } from 'react';
import {
  HiOutlineArrowLeft,
  HiOutlineArrowPath,
  HiOutlineBeaker,
  HiOutlineCheckCircle,
  HiOutlineExclamationTriangle,
  HiOutlineHeart,
  HiOutlineSparkles,
  HiOutlineUser,
} from 'react-icons/hi2';
import { GiKidneys } from 'react-icons/gi';

import { predictDisease, uploadReport } from '../api/client';
import UploadBox from '../components/UploadBox';
import DynamicField from '../components/DynamicField';
import RiskGauge from '../components/RiskGauge';

// Turn an axios failure into something diagnostic instead of a generic message.
function describeError(err, fallback) {
  // eslint-disable-next-line no-console
  console.error('[MedIntel] request failed:', err);
  if (err && err.response) {
    const detail = err.response.data && err.response.data.detail;
    return `Backend responded ${err.response.status}: ${detail || err.response.statusText}. Check the backend terminal for the traceback.`;
  }
  if (err && err.request) {
    const url = (err.config && err.config.baseURL) || 'http://localhost:8000';
    return `Can't reach the backend at ${url}. Is it running? Open ${url}/docs in your browser to confirm.`;
  }
  return fallback;
}

const DISEASES = [
  { key: 'diabetes', label: 'Diabetes', icon: HiOutlineBeaker },
  { key: 'heart', label: 'Heart Disease', icon: HiOutlineHeart },
  { key: 'kidney', label: 'Chronic Kidney Disease', icon: GiKidneys },
];

// Lab keys the backend may extract — for a friendly "what we found" panel.
const LAB_LABELS = {
  fasting_glucose: 'Fasting glucose',
  post_meal_glucose: 'Post-meal glucose',
  hba1c: 'HbA1c',
  creatinine: 'Creatinine',
  hemoglobin: 'Hemoglobin',
  cholesterol: 'Cholesterol',
  urea: 'Urea',
  blood_pressure: 'Blood pressure',
};

const STEPS = ['Upload', 'Review', 'Result'];

export default function UploadReport() {
  const [step, setStep] = useState(0);            // 0 upload · 1 review · 2 result
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');

  const [patient, setPatient] = useState({});
  const [labs, setLabs] = useState({});

  const [disease, setDisease] = useState(null);
  const [missing, setMissing] = useState([]);
  const [mapped, setMapped] = useState({});
  const [manual, setManual] = useState({});
  const [predicting, setPredicting] = useState(false);
  const [predictError, setPredictError] = useState('');
  const [result, setResult] = useState(null);

  const handleFileSelect = async (selected) => {
    setFile(selected);
    setUploadError('');
    if (!selected) return;

    setUploading(true);
    try {
      const res = await uploadReport(selected);
      setPatient(res?.data?.patient || {});
      setLabs(res?.data?.lab_values || {});
      setStep(1);
    } catch (err) {
      setUploadError(describeError(err, "Couldn't reach the backend — make sure the API server is running, then try again."));
    } finally {
      setUploading(false);
    }
  };

  // Choosing a condition asks the backend what it can auto-fill and what's missing.
  const chooseDisease = async (key) => {
    setDisease(key);
    setManual({});
    setResult(null);
    setPredictError('');
    setPredicting(true);
    try {
      const res = await predictDisease({ disease: key, patient, lab_values: labs });
      if (res.status === 'needs_user_input') {
        setMapped(res.mapped_features || {});
        setMissing(res.missing_features || []);
      } else if (res.status === 'success') {
        setMapped(res.used_features || {});
        setMissing([]);
        setResult(res);
        setStep(2);
      }
    } catch (err) {
      setPredictError(describeError(err, 'Prediction failed — is the backend running?'));
    } finally {
      setPredicting(false);
    }
  };

  const setField = (name, value) => setManual((m) => ({ ...m, [name]: value }));

  const allFilled = useMemo(
    () => missing.every((m) => manual[m.name] !== undefined && manual[m.name] !== ''),
    [missing, manual]
  );

  const runPrediction = async () => {
    setPredicting(true);
    setPredictError('');
    try {
      const res = await predictDisease({
        disease,
        patient,
        lab_values: labs,
        manual_values: manual,
      });
      if (res.status === 'success') {
        setResult(res);
        setStep(2);
      } else {
        setMissing(res.missing_features || []);
        setPredictError('Some values are still needed.');
      }
    } catch (err) {
      setPredictError(describeError(err, 'Prediction failed — is the backend running?'));
    } finally {
      setPredicting(false);
    }
  };

  const reset = () => {
    setStep(0); setFile(null); setPatient({}); setLabs({});
    setDisease(null); setMissing([]); setMapped({}); setManual({}); setResult(null);
    setUploadError(''); setPredictError('');
  };

  const extractedLabs = Object.entries(labs).filter(([, v]) => v !== null && v !== undefined);
  const patientEntries = Object.entries(patient).filter(([, v]) => v);

  return (
    <section className="upload-page">
      <div className="upload-page-badge">
        <HiOutlineSparkles /> Lab report intake
      </div>
      <h2>Upload &amp; analyze a report</h2>
      <p className="upload-page-sub">
        Drop in a PDF, review what we pulled out, fill any gaps the model needs,
        and get an explained risk read-out — all in one flow.
      </p>

      <Stepper step={step} />

      {/* ---------------- STEP 0 — UPLOAD ---------------- */}
      {step === 0 && (
        <>
          <UploadBox file={file} onFileSelect={handleFileSelect} />
          {uploading && (
            <div className="upload-status glass upload-status-uploading">
              <span className="upload-status-dot" /> Extracting values from the PDF…
            </div>
          )}
          {uploadError && (
            <div className="upload-status glass upload-status-error">
              <HiOutlineExclamationTriangle className="upload-status-icon" />
              <span>{uploadError}</span>
            </div>
          )}
        </>
      )}

      {/* ---------------- STEP 1 — REVIEW ---------------- */}
      {step === 1 && (
        <div className="review">
          <div className="review-grid">
            <div className="glass info-card">
              <h3><HiOutlineUser /> Patient</h3>
              {patientEntries.length ? (
                <ul className="kv">
                  {patientEntries.map(([k, v]) => (
                    <li key={k}><span>{k.replace(/_/g, ' ')}</span><strong>{String(v)}</strong></li>
                  ))}
                </ul>
              ) : (
                <p className="muted">No patient details detected — you can still continue.</p>
              )}
            </div>

            <div className="glass info-card">
              <h3><HiOutlineBeaker /> Extracted lab values</h3>
              <div className="chips">
                {Object.keys(LAB_LABELS).map((k) => {
                  const v = labs[k];
                  const found = v !== null && v !== undefined;
                  return (
                    <span key={k} className={`chip ${found ? 'chip-found' : 'chip-missing'}`}>
                      {LAB_LABELS[k]}{found && <strong>{String(v)}</strong>}
                    </span>
                  );
                })}
              </div>
              {extractedLabs.length === 0 && (
                <p className="muted">
                  Nothing parsed cleanly from this PDF — no problem, you can enter
                  the values the model needs on the next step.
                </p>
              )}
            </div>
          </div>

          <h3 className="review-heading">Choose a condition to assess</h3>
          <div className="disease-grid">
            {DISEASES.map((d) => {
              const Icon = d.icon;
              return (
                <button
                  key={d.key}
                  className={`disease-card glass ${disease === d.key ? 'active' : ''}`}
                  onClick={() => chooseDisease(d.key)}
                  type="button"
                  disabled={predicting}
                >
                  <span className="disease-icon"><Icon /></span>
                  <span className="disease-label">{d.label}</span>
                </button>
              );
            })}
          </div>

          {predicting && !result && (
            <div className="upload-status glass upload-status-uploading">
              <span className="upload-status-dot" /> Mapping report values to the model…
            </div>
          )}

          {/* Dynamic missing-value form */}
          {disease && !predicting && missing.length > 0 && (
            <div className="glass form-panel">
              <div className="form-panel-head">
                <h3>A few more values for {DISEASES.find((d) => d.key === disease)?.label}</h3>
                <p className="muted">
                  {Object.keys(mapped).length > 0
                    ? `${Object.keys(mapped).length} value(s) came from the report. `
                    : ''}
                  {missing.length} still needed — the model asks for exactly these.
                </p>
              </div>

              {Object.keys(mapped).length > 0 && (
                <div className="mapped-row">
                  {Object.entries(mapped).map(([k, v]) => (
                    <span key={k} className="chip chip-auto">
                      <HiOutlineCheckCircle /> {k}<strong>{String(v)}</strong>
                    </span>
                  ))}
                </div>
              )}

              <div className="form-grid">
                {missing.map((spec) => (
                  <DynamicField
                    key={spec.name}
                    spec={spec}
                    value={manual[spec.name]}
                    onChange={setField}
                  />
                ))}
              </div>

              {predictError && <p className="form-error">{predictError}</p>}

              <button
                className="btn btn-primary form-submit"
                onClick={runPrediction}
                disabled={!allFilled || predicting}
                type="button"
              >
                {predicting ? 'Predicting…' : 'Run prediction'} <HiOutlineSparkles />
              </button>
            </div>
          )}

          <button className="btn btn-ghost back-btn" onClick={reset} type="button">
            <HiOutlineArrowLeft /> Start over
          </button>
        </div>
      )}

      {/* ---------------- STEP 2 — RESULT ---------------- */}
      {step === 2 && result && (
        <ResultView result={result} onAnother={() => setStep(1)} onReset={reset} />
      )}
    </section>
  );
}

function Stepper({ step }) {
  return (
    <div className="stepper">
      {STEPS.map((label, i) => (
        <div key={label} className={`step ${i === step ? 'current' : ''} ${i < step ? 'done' : ''}`}>
          <span className="step-dot">{i < step ? <HiOutlineCheckCircle /> : i + 1}</span>
          <span className="step-label">{label}</span>
          {i < STEPS.length - 1 && <span className="step-line" />}
        </div>
      ))}
    </div>
  );
}

function ResultView({ result, onAnother, onReset }) {
  const riskClass = `risk-${result.risk?.toLowerCase()}`;
  return (
    <div className="result">
      <div className="glass result-hero">
        <div className="result-gauge">
          <RiskGauge probability={result.probability} risk={result.risk} label="disease risk" />
        </div>
        <div className="result-verdict">
          <span className={`result-chip ${riskClass}`}>{result.risk} risk</span>
          <h3 className="result-pred">{result.prediction}</h3>
          <p className="result-meta">
            {result.disease_label} · model confidence{' '}
            <strong>{Math.round(result.confidence * 100)}%</strong>
          </p>
        </div>
      </div>

      {result.key_factors?.length > 0 && (
        <div className="glass result-factors">
          <h3>What drove this</h3>
          <ul className="factor-list">
            {result.key_factors.map((f) => (
              <li key={f.feature} className="factor">
                <div className="factor-top">
                  <span className="factor-label">{f.label}</span>
                  <span className="factor-value">
                    {String(f.value)}{f.unit ? ` ${f.unit}` : ''}
                  </span>
                </div>
                <div className="factor-bar">
                  <span
                    className={`factor-fill ${f.z > 0 ? 'up' : 'down'}`}
                    style={{ width: `${Math.min(100, Math.abs(f.z) * 33)}%` }}
                  />
                </div>
                <span className="factor-note">{f.direction}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="glass result-summary">
        <h3><HiOutlineSparkles /> AI summary</h3>
        <p>{result.ai_summary}</p>
      </div>

      <div className="result-actions">
        <button className="btn btn-primary" onClick={onAnother} type="button">
          <HiOutlineArrowPath /> Assess another condition
        </button>
        <button className="btn btn-ghost" onClick={onReset} type="button">
          New report
        </button>
      </div>

      <p className="result-disclaimer">
        <HiOutlineExclamationTriangle /> Educational estimate only — not a medical
        diagnosis. Please consult a qualified clinician.
      </p>
    </div>
  );
}
