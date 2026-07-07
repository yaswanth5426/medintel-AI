import './ChatBubble.css';

export default function ChatBubble({ text, sender, typing = false, sources = [] }) {
  const isUser = sender === "user";
  return (
    <div className={`bubble-row ${isUser ? "from-user" : "from-bot"}`}>
      {!isUser && <span className="signal bubble-signal" />}
      <div className={`bubble ${isUser ? "bubble-user" : "bubble-bot"}`}>
        {typing ? (
          <span className="typing-dots">
            <span /><span /><span />
          </span>
        ) : (
          <>
            {text}
            {sources?.length > 0 && (
              <div className="bubble-sources">
                {sources.map((s, i) => (
                  <span className="bubble-source-pill" key={i}>{s}</span>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
