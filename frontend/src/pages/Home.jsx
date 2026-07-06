import './Home.css';

import { Link } from 'react-router-dom';

const conditions = ['Diabetes', 'Heart Disease', 'Chronic Kidney Disease'];

const entryPoints = [
  {
    to: '/chat',
    tag: 'Symptoms',
    title: 'Describe your symptoms',
    body: 'Chat with the assistant about what you’re experiencing and get a risk read-out backed by the prediction model.',
    cta: 'Start a symptom chat',
  },
  {
    to: '/upload',
    tag: 'Lab report',
    title: 'Upload a medical report',
    body: 'Drop in a PDF of your lab results — values are extracted automatically and run through the same model.',
    cta: 'Upload a report',
  },
];

export default function Home() {
  return (
    <section className="home">
      <p className="home-eyebrow">AI-powered clinical decision support</p>
      <h1 className="home-title">
        Know your risk.<br />Understand why.
      </h1>
      <p className="home-sub">
        MedIntel AI estimates disease risk from symptoms or lab reports, then
        explains the prediction, answers follow-up questions, and puts
        together a lifestyle plan — all in one place.
      </p>

      <div className="home-entry-grid">
        {entryPoints.map((e) => (
          <Link to={e.to} className="entry-card" key={e.to}>
            <span className="entry-tag">{e.tag}</span>
            <h3 className="entry-title">{e.title}</h3>
            <p className="entry-body">{e.body}</p>
            <span className="entry-cta">{e.cta} &rarr;</span>
          </Link>
        ))}
      </div>

      <div className="home-conditions">
        <span className="home-conditions-label">Currently supports</span>
        <div className="condition-pills">
          {conditions.map((c) => (
            <span className="condition-pill" key={c}>{c}</span>
          ))}
        </div>
      </div>

      <div className="home-actions">
        <Link to="/dashboard" className="btn btn-ghost">View dashboard</Link>
      </div>
    </section>
  );
}
