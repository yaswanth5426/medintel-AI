import './ChatBubble.css';

export default function ChatBubble({ text, sender, typing = false }) {
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
          text
        )}
      </div>
    </div>
  );
}