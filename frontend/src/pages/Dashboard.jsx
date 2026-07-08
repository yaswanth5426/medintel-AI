import './Dashboard.css';

import {
  useCallback,
  useEffect,
  useState,
} from 'react';
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
import {
  HiOutlineArrowPath,
  HiOutlineArrowTrendingUp,
  HiOutlineBoltSlash,
  HiOutlineHeart,
  HiOutlineInbox,
  HiOutlineShieldCheck,
} from 'react-icons/hi2';

import { getHistory } from '../api/client';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

const riskClass = {
  Low: 'risk-low',
  Medium: 'risk-medium',
  High: 'risk-high',
};

const STATUS = {
  LOADING: 'loading',
  ERROR: 'error',
  SUCCESS: 'success',
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
      ticks: { color: '#8993A8', callback: (v) => `${v}%` },
      grid: { color: 'rgba(255, 255, 255, 0.06)' },
    },
    x: {
      ticks: { color: '#8993A8' },
      grid: { display: false },
    },
  },
};

export default function Dashboard() {
  const [status, setStatus] = useState(STATUS.LOADING);
  const [history, setHistory] = useState([]);
  const [note, setNote] = useState('');

  // No synchronous setState at the top of this function — it's called
  // directly from an effect on mount, and only from a click handler on
  // retry. The "loading" state itself comes from useState's initial value
  // / the retry handler, not from here.
  const fetchHistory = useCallback(() => {
    getHistory()
      .then((data) => {
        setHistory(data.predictions || []);
        setNote(data.note || '');
        setStatus(STATUS.SUCCESS);
      })
      .catch(() => {
        setStatus(STATUS.ERROR);
      });
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleRetry = () => {
    setStatus(STATUS.LOADING);
    fetchHistory();
  };

  if (status === STATUS.LOADING) {
    return (
      <section className="dashboard">
        <div className="dashboard-center glass">
          <span className="spinner" />
          <p>Loading dashboard…</p>
        </div>
      </section>
    );
  }

  if (status === STATUS.ERROR) {
    return (
      <section className="dashboard">
        <div className="dashboard-center glass">
          <span className="dashboard-center-icon dashboard-center-icon-error">
            <HiOutlineBoltSlash />
          </span>
          <p>Failed to connect to the backend.</p>
          <button className="btn btn-primary" onClick={handleRetry} type="button">
            <HiOutlineArrowPath /> Try again
          </button>
        </div>
      </section>
    );
  }

  const metrics = [
    {
      label: 'Predictions run',
      value: history.length.toString(),
      unit: '',
      icon: HiOutlineArrowTrendingUp,
    },
    {
      label: 'Avg. confidence',
      value: history.length
        ? Math.round(
            (history.reduce((s, h) => s + h.confidence, 0) / history.length) * 100
          ).toString()
        : '0',
      unit: '%',
      icon: HiOutlineShieldCheck,
    },
    {
      label: 'Conditions tracked',
      value: new Set(history.map((h) => h.disease)).size.toString(),
      unit: '',
      icon: HiOutlineHeart,
    },
  ];

  const chartData = {
    labels: history.map((h) => h.date),
    datasets: [
      {
        label: 'Confidence score',
        data: history.map((h) => Math.round(h.confidence * 100)),
        borderColor: '#22D3EE',
        backgroundColor: 'rgba(34, 211, 238, 0.12)',
        pointBackgroundColor: '#8B5CF6',
        pointBorderColor: '#8B5CF6',
        tension: 0.35,
        fill: true,
      },
    ],
  };

  return (
    <section className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <div className="dashboard-status">
          <span className="signal" />
          <span>{note || 'Live from backend'}</span>
        </div>
      </div>

      <div className="metric-grid">
        {metrics.map((m) => {
          const Icon = m.icon;
          return (
            <div className="metric-card glass" key={m.label}>
              <span className="metric-icon">
                <Icon />
              </span>
              <p className="metric-label">{m.label}</p>
              <p className="metric-value">
                {m.value}<span className="metric-unit">{m.unit}</span>
              </p>
            </div>
          );
        })}
      </div>

      {history.length === 0 ? (
        <div className="dashboard-panel glass dashboard-panel-empty">
          <span className="dashboard-empty-icon">
            <HiOutlineInbox />
          </span>
          <p className="dashboard-empty">No predictions yet — try the chat or upload a report.</p>
        </div>
      ) : (
        <>
          <div className="dashboard-panel glass">
            <h3>Confidence over recent predictions</h3>
            <Line data={chartData} options={chartOptions} />
          </div>

          <div className="dashboard-panel glass">
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
                  <span className={`risk-chip ${riskClass[h.risk_level]}`}>{h.risk_level}</span>
                  <span>{Math.round(h.confidence * 100)}%</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
