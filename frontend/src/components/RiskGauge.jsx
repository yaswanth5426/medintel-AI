import './RiskGauge.css';

import { useEffect, useState } from 'react';

const RISK_COLOR = {
  Low: 'var(--cyan)',
  Medium: 'var(--amber)',
  High: 'var(--coral)',
};

/**
 * Animated semicircular risk meter.
 * props: probability (0-1), risk ("Low"|"Medium"|"High"), label
 */
export default function RiskGauge({ probability = 0, risk = 'Low', label = 'risk' }) {
  const pct = Math.round(probability * 100);
  const color = RISK_COLOR[risk] || 'var(--cyan)';

  // Animate the arc from 0 to pct on mount / when the value changes.
  const [shown, setShown] = useState(0);
  useEffect(() => {
    let raf;
    const start = performance.now();
    const from = 0;
    const dur = 900;
    const tick = (t) => {
      const k = Math.min(1, (t - start) / dur);
      const eased = 1 - Math.pow(1 - k, 3);
      setShown(Math.round(from + (pct - from) * eased));
      if (k < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [pct]);

  // Semicircle path (radius 80, centre 100,100). pathLength=100 -> easy %.
  const arc = 'M20 100 A80 80 0 0 1 180 100';

  return (
    <div className="gauge">
      <svg viewBox="0 0 200 116" className="gauge-svg" role="img" aria-label={`${pct}% ${label}`}>
        <path d={arc} className="gauge-track" pathLength="100" />
        <path
          d={arc}
          className="gauge-value"
          pathLength="100"
          style={{ stroke: color, strokeDasharray: `${shown} 100` }}
        />
        <defs>
          <filter id="gauge-glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="3" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
      </svg>
      <div className="gauge-readout">
        <span className="gauge-pct" style={{ color }}>{shown}%</span>
        <span className="gauge-label">{label}</span>
      </div>
    </div>
  );
}
