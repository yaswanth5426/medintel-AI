import './Home.css';

import { Link } from 'react-router-dom';
import { GiKidneys } from 'react-icons/gi';
import {
  HiOutlineArrowRight,
  HiOutlineBeaker,
  HiOutlineChatBubbleLeftRight,
  HiOutlineDocumentArrowUp,
  HiOutlineHeart,
  HiOutlineSparkles,
} from 'react-icons/hi2';

const conditions = [
  { label: 'Diabetes', icon: HiOutlineBeaker },
  { label: 'Heart Disease', icon: HiOutlineHeart },
  { label: 'Chronic Kidney Disease', icon: GiKidneys },
];

const entryPoints = [
  {
    to: '/chat',
    tag: 'Symptoms',
    title: 'Describe your symptoms',
    body: 'Chat with the assistant about what you’re experiencing and get a risk read-out backed by the prediction model.',
    cta: 'Start a symptom chat',
    icon: HiOutlineChatBubbleLeftRight,
  },
  {
    to: '/upload',
    tag: 'Lab report',
    title: 'Upload a medical report',
    body: 'Drop in a PDF of your lab results — values are extracted automatically and run through the same model.',
    cta: 'Upload a report',
    icon: HiOutlineDocumentArrowUp,
  },
];

export default function Home() {
  return (
    <section className="home">
      <div className="home-badge">
        <HiOutlineSparkles />
        AI-powered clinical decision support
      </div>

      <h1 className="home-title">
        Know your risk.
        <br />
        <span className="gradient-text">Understand why.</span>
      </h1>

      <p className="home-sub">
        MedIntel AI estimates disease risk from symptoms or lab reports, then
        explains the prediction, answers follow-up questions, and puts
        together a lifestyle plan — all in one place.
      </p>

      <div className="home-entry-grid">
        {entryPoints.map((e) => {
          const Icon = e.icon;
          return (
            <Link to={e.to} className="entry-card glass" key={e.to}>
              <span className="entry-icon">
                <Icon />
              </span>
              <span className="entry-tag">{e.tag}</span>
              <h3 className="entry-title">{e.title}</h3>
              <p className="entry-body">{e.body}</p>
              <span className="entry-cta">
                {e.cta} <HiOutlineArrowRight />
              </span>
            </Link>
          );
        })}
      </div>

      <div className="home-conditions">
        <span className="home-conditions-label">Currently supports</span>
        <div className="condition-pills">
          {conditions.map((c) => {
            const Icon = c.icon;
            return (
              <span className="condition-pill" key={c.label}>
                <Icon /> {c.label}
              </span>
            );
          })}
        </div>
      </div>

      <div className="home-actions">
        <Link to="/dashboard" className="btn btn-ghost">
          View dashboard
        </Link>
      </div>
    </section>
  );
}
