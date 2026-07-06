import './Dashboard.css';

import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

// Mock prediction history — real data will come from GET /history
// (backend/database, Member 3's own module) once MongoDB is wired up.
const history = [
  { date: 'Jun 30', source: 'Symptoms', disease: 'Diabetes', risk: 'Low', confidence: 0.22 },
  { date: 'Jul 1', source: 'Lab report', disease: 'Heart Disease', risk: 'Medium', confidence: 0.54 },
  { date: 'Jul 2', source: 'Symptoms', disease: 'CKD', risk: 'Low', confidence: 0.18 },
  { date: 'Jul 4', source: 'Lab report', disease: 'Diabetes', risk: 'High', confidence: 0.81 },
  { date: 'Jul 5', source: 'Symptoms', disease: 'Heart Disease', risk: 'Medium', confidence: 0.47 },
  { date: 'Jul 6', source: 'Lab report', disease: 'CKD', risk: 'Medium', confidence: 0.39 },
];

const riskClass = {
  Low: 'risk-low',
  Medium: 'risk-medium',
  High: 'risk-high',
};

const metrics = [
  { label: 'Predictions run', value: history.length.toString(), unit: '' },
  {
    label: 'Avg. confidence',
    value: Math.round(
      (history.reduce((s, h) => s + h.confidence, 0) / history.length) * 100
    ).toString(),
    unit: '%',
  },
  { label: 'Conditions tracked', value: '3', unit: '' },
];

const chartData = {
  labels: history.map((h) => h.date),
  datasets: [
    {
      label: 'Confidence score',
      data: history.map((h) => Math.round(h.confidence * 100)),
      borderColor: '#4FA1A0',
      backgroundColor: 'rgba(79, 161, 160, 0.15)',
      pointBackgroundColor: '#E8A13D',
      tension: 0.35,
      fill: true,
    },
  ],
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      min: 0,
      max: 100,
      ticks: { color: '#9AA5AF', callback: (v) => `${v}%` },
      grid: { color: '#2A333D' },
    },
    x: {
      ticks: { color: '#9AA5AF' },
      grid: { display: false },
    },
  },
};

export default function Dashboard() {
  return (
    <section className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <div className="dashboard-status">
          <span className="signal" />
          <span>Mock data — history API not connected yet</span>
        </div>
      </div>

      <div className="metric-grid">
        {metrics.map((m) => (
          <div className="metric-card" key={m.label}>
            <p className="metric-label">{m.label}</p>
            <p className="metric-value">
              {m.value}<span className="metric-unit">{m.unit}</span>
            </p>
          </div>
        ))}
      </div>

      <div className="dashboard-panel">
        <h3>Confidence over recent predictions</h3>
        <Line data={chartData} options={chartOptions} />
      </div>

      <div className="dashboard-panel">
        <h3>Prediction history</h3>
        <div className="history-table">
          <div className="history-row history-head">
            <span>Date</span>
            <span>Source</span>
            <span>Condition</span>
            <span>Risk</span>
            <span>Confidence</span>
          </div>
          {history.map((h, i) => (
            <div className="history-row" key={i}>
              <span>{h.date}</span>
              <span>{h.source}</span>
              <span>{h.disease}</span>
              <span className={`risk-chip ${riskClass[h.risk]}`}>{h.risk}</span>
              <span>{Math.round(h.confidence * 100)}%</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
