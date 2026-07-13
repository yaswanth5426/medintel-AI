import './DynamicField.css';

/**
 * Renders one input from a backend feature spec. The backend decides the
 * type/options/units, so nothing here is hardcoded per-disease.
 * spec: { name, label, type: 'number'|'select', unit, min, max, step, normal, hint, options }
 */
export default function DynamicField({ spec, value, onChange }) {
  const id = `f-${spec.name}`;

  return (
    <label className="field" htmlFor={id}>
      <span className="field-head">
        <span className="field-label">{spec.label}</span>
        {spec.unit && <span className="field-unit">{spec.unit}</span>}
      </span>

      {spec.type === 'select' ? (
        <select
          id={id}
          className="field-input"
          value={value ?? ''}
          onChange={(e) => onChange(spec.name, e.target.value)}
        >
          <option value="" disabled>Select…</option>
          {(spec.options || []).map((o) => (
            <option key={String(o.value)} value={o.value}>{o.label}</option>
          ))}
        </select>
      ) : (
        <input
          id={id}
          className="field-input"
          type="number"
          inputMode="decimal"
          value={value ?? ''}
          min={spec.min}
          max={spec.max}
          step={spec.step ?? 'any'}
          placeholder={spec.normal && spec.normal !== '—' ? `normal ${spec.normal}` : ''}
          onChange={(e) => onChange(spec.name, e.target.value)}
        />
      )}

      {(spec.hint || (spec.normal && spec.normal !== '—')) && (
        <span className="field-hint">
          {spec.hint}
          {spec.normal && spec.normal !== '—' && (
            <span className="field-normal"> · normal {spec.normal}</span>
          )}
        </span>
      )}
    </label>
  );
}
