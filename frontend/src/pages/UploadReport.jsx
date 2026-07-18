import './UploadReport.css';

import { useState } from 'react';
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

// Lab keys the v2 parser may return, for the "what we found" panel.
const LAB_LABELS = {
  glucose: 'Glucose',
  hba1c: 'HbA1c',
  blood_pressure: 'Blood pressure',
  cholesterol: 'Cholesterol',
  blood_urea: 'Blood urea',
  serum_creatinine: 'Creatinine',
  hemoglobin: 'Hemoglobin',
  sodium: 'Sodium',
  potassium: 'Potassium',
  egfr: 'eGFR',
};

// Compact, editable "key values" the user can confirm/correct before predicting.
// These are merged over whatever the parser extracted (sent as manual_values).
const KEY_FIELDS = [
  { name: 'age', label: 'Age', type: 'number', unit: 'years', min: 0, max: 120, step: 1, source: 'patient' },
  { name: 'gender', label: 'Sex', type: 'select', source: 'patient',
    options: [{ value: 'Male', label: 'Male' }, { value: 'Female', label: 'Female' }] },
  { name: 'glucose', label: 'Glucose', type: 'number', unit: 'mg/dL', min: 0, max: 500, step: 1, normal: '70-140' },
  { name: 'hba1c', label: 'HbA1c', type: 'number', unit: '%', min: 0, max: 20, step: 0.1, normal: '4-5.7' },
  { name: 'blood_pressure', label: 'Blood pressure', type: 'number', unit: 'mmHg (systolic)', min: 0, max: 260, step: 1, normal: '90-120' },
  { name: 'cholesterol', label: 'Cholesterol', type: 'number', unit: 'mg/dL', min: 0, max: 700, step: 1, normal: '<200' },
  { name: 'serum_creatinine', label: 'Creatinine', type: 'number', unit: 'mg/dL', min: 0, max: 80, step: 0.1, normal: '0.6-1.3' },
  { name: 'hemoglobin', label: 'Hemoglobin', type: 'number', unit: 'g/dL', min: 0, max: 25, step: 0.1, normal: '12-17' },
];

const STEPS = ['Upload', 'Review', 'Result'];

// backend detected disease ("ckd") -> our picker key ("kidney")
function toKey(detected) {
  if (!detected) return null;
  const d = String(detected).toLowerCase();
  if (d.includes('kidney') || d === 'ckd') return 'kidney';
  if (d.includes('heart') || d === 'cardiac') return 'heart';
  if (d.includes('diabet')) return 'diabetes';
  return null;
}

export default function UploadReport() {
  const [step, setStep] = useState(0);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');

  const [patient, setPatient] = useState({});
  const [labs, setLabs] = useState({});
  const [detected, setDetected] = useState(null);

  const [disease, setDisease] = useState(null);
  const [manual, setManual] = useState({});
  const [predicting, setPredicting] = useState(false);
  const [predictError, setPredictError] = useState('');
  const [result, setResult] = useState(null);

  const seedManual = (p, l) => {
    const seed = {};
    KEY_FIELDS.forEach((f) => {
      const src = f.source === 'patient' ? p : l;
      if (src && src[f.name] !== undefined && src[f.name] !== null) seed[f.name] = src[f.name];
    });
    return seed;
  };

  const handleFileSelect = async (selected) => {
    setFile(selected);
    setUploadError('');
    if (!selected) return;

    setUploading(true);
    try {
      const res = await uploadReport(selected);
      const p = res?.data?.patient || {};
      const l = res?.data?.lab_values || {};
      setPatient(p);
      setLabs(l);
      const key = toKey(res?.disease_detected);
      setDetected(key);
      setDisease(key);
      setManual(seedManual(p, l));
      setResult(null);
      setStep(1);
    } catch (err) {
      setUploadError(describeError(err, "Couldn't reach the backend — make sure the API server is running, then try again."));
    } finally {
      setUploading(false);
    }
  };

  const setField = (name, value) => setManual((m) => ({ ...m, [name]: value }));

  const runPrediction = async () => {
    if (!disease) { setPredictError('Pick a condition to assess first.'); return; }
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
        setPredictError('Prediction did not complete — please try again.');
      }
    } catch (err) {
      setPredictError(describeError(err, 'Prediction failed — is the backend running?'));
    } finally {
      setPredicting(false);
    }
  };

  const reset = () => {
    setStep(0); setFile(null); setPatient({}); setLabs({}); setDetected(null);
    setDisease(null); setManual({}); setResult(null); setUploadError(''); setPredictError('');
  };

  const patientEntries = Object.entries(patient).filter(([, v]) => v !== null && v !== undefined && v !== '');

  return (
    <section className="upload-page">
      <div className="upload-page-badge">
        <HiOutlineSparkles /> Lab report intake
      </div>
      <h2>Upload &amp; analyze a report</h2>
      <p className="upload-page-sub">
        Drop in a PDF, confirm the key values we pulled out, and get an explained
        risk read-out from the model.
      </p>

      <Stepper step={step} />

      {/* STEP 0 — UPLOAD */}
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

      {/* STEP 1 — REVIEW */}
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
                <p className="muted">No patient details detected — enter what you can below.</p>
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
              <p className="muted" style={{ marginTop: '0.85rem' }}>
                Automatic extraction can miss or misread values — confirm the key
                ones below before predicting.
              </p>
            </div>
          </div>

          <h3 className="review-heading">Condition to assess</h3>
          <div className="disease-grid">
            {DISEASES.map((d) => {
              const Icon = d.icon;
              return (
                <button
                  key={d.key}
                  className={`disease-card glass ${disease === d.key ? 'active' : ''}`}
                  onClick={() => setDisease(d.key)}
                  type="button"
                >
                  <span className="disease-icon"><Icon /></span>
                  <span className="disease-label">{d.label}</span>
                  {detected === d.key && <span className="disease-detected">detected</span>}
                </button>
              );
            })}
          </div>

          <div className="glass form-panel">
            <div className="form-panel-head">
              <h3>Confirm key values</h3>
              <p className="muted">Pre-filled from the report where possible. Edit any that look wrong; blanks fall back to model defaults.</p>
            </div>
            <div className="form-grid">
              {KEY_FIELDS.map((spec) => (
                <DynamicField key={spec.name} spec={spec} value={manual[spec.name]} onChange={setField} />
              ))}
            </div>

            {predictError && <p className="form-error">{predictError}</p>}

            <button
              className="btn btn-primary form-submit"
              onClick={runPrediction}
              disabled={predicting || !disease}
              type="button"
            >
              {predicting ? 'Predicting…' : 'Run prediction'} <HiOutlineSparkles />
            </button>
          </div>

          <button className="btn btn-ghost back-btn" onClick={reset} type="button">
            <HiOutlineArrowLeft /> Start over
          </button>
        </div>
      )}

      {/* STEP 2 — RESULT */}
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

// Parse a normal-range string like "0.6-1.3", "60 - 200", "<90" or ">126".
function parseRange(str) {
  if (str == null) return null;
  const s = String(str).replace(/[–—]/g, '-');
  let m = s.match(/<\s*(\d+(?:\.\d+)?)/);
  if (m) return { low: 0, high: parseFloat(m[1]) };
  m = s.match(/>\s*(\d+(?:\.\d+)?)/);
  if (m) return { low: parseFloat(m[1]), high: parseFloat(m[1]) * 1.5 };
  m = s.match(/(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)/);
  if (m) return { low: parseFloat(m[1]), high: parseFloat(m[2]) };
  return null;
}

// First number out of a value that may be 2, "2", "140/90" or "182 mg/dL".
function parseValue(v) {
  if (typeof v === 'number') return v;
  const m = String(v).match(/-?\d+(?:\.\d+)?/);
  return m ? parseFloat(m[0]) : NaN;
}

const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));

// Fill % = how ABNORMAL the value is, so every flagged metric reads as a strong
// bar and the length tracks severity (color already shows direction: warm=high,
// cool=low). Inside the normal band the bar stays modest; the further past the
// nearest bound the value sits, the fuller the bar — in either direction.
function fillPercent(value, normalStr) {
  const val = parseValue(value);
  const range = parseRange(normalStr);
  if (!isFinite(val) || !range || range.high <= range.low) return 60; // safe default
  const { low, high } = range;
  const span = high - low || 1;
  if (val >= low && val <= high) {
    return Math.round(22 + ((val - low) / span) * 23);   // within normal: 22-45%
  }
  const bound = val > high ? high : low;                 // nearest normal bound
  const dist = val > high ? val - high : low - val;      // distance outside it
  const rel = dist / (Math.abs(bound) || span);          // relative to that bound
  return Math.round(clamp(58 + rel * 85, 58, 100));      // abnormal: 58-100%
}

function ResultView({ result, onAnother, onReset }) {
  const riskClass = `risk-${(result.risk || 'low').toLowerCase()}`;
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
            <strong>{Math.round((result.confidence || 0) * 100)}%</strong>
          </p>
        </div>
      </div>

      {result.key_factors?.length > 0 && (
        <div className="glass result-factors">
          <h3>What stood out</h3>
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
                  <span className={`factor-fill ${f.direction?.includes('higher') ? 'up' : 'down'}`}
                    style={{ width: `${fillPercent(f.value, f.normal)}%` }} />
                </div>
                <span className="factor-note">{f.direction}{f.normal ? ` · normal ${f.normal}` : ''}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.shap?.available && result.shap.top?.length > 0 && (
        <div className="glass result-shap">
          <h3><HiOutlineSparkles /> Why the model decided this</h3>
          <p className="shap-caption">
            SHAP shows how each value pushed the model&apos;s risk estimate
            up (warm, to the right) or down (cool, to the left).
          </p>
          <ul className="shap-list">
            {(() => {
              const top = result.shap.top;
              const maxAbs = Math.max(...top.map((s) => Math.abs(s.contribution))) || 1;
              return top.map((s) => {
                const w = (Math.abs(s.contribution) / maxAbs) * 50; // half-track
                const up = s.direction === 'increases';
                return (
                  <li key={s.feature} className="shap-row">
                    <span className="shap-label">
                      {s.label}
                      {s.value != null && s.value !== '' && (
                        <em> {String(s.value)}{s.unit ? ` ${s.unit}` : ''}</em>
                      )}
                    </span>
                    <div className="shap-track">
                      <span className="shap-axis" />
                      <span
                        className={`shap-bar ${up ? 'up' : 'down'}`}
                        style={up ? { left: '50%', width: `${w}%` } : { right: '50%', width: `${w}%` }}
                      />
                    </div>
                    <span className={`shap-tag ${up ? 'up' : 'down'}`}>{up ? '↑ risk' : '↓ risk'}</span>
                  </li>
                );
              });
            })()}
          </ul>
        </div>
      )}

      <div className="glass result-summary">
        <h3><HiOutlineSparkles /> AI summary</h3>
        <p>{result.ai_summary}</p>
      </div>

      <div className="result-actions">
        <button className="btn btn-primary" onClick={onAnother} type="button">
          <HiOutlineArrowPath /> Adjust &amp; re-run
        </button>
        <button className="btn btn-ghost" onClick={onReset} type="button">New report</button>
      </div>

      <p className="result-disclaimer">
        <HiOutlineExclamationTriangle /> Educational estimate only — not a medical
        diagnosis. Please consult a qualified clinician.
      </p>
    </div>
  );
}
