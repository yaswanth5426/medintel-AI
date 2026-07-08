import './Chat.css';

import {
  useEffect,
  useRef,
  useState,
} from 'react';
import { HiOutlinePaperAirplane } from 'react-icons/hi2';

import { sendChatMessage } from '../api/client';
import ChatBubble from '../components/ChatBubble';

const CONTEXTS = ['General', 'Diabetes', 'Heart Disease', 'CKD'];

export default function Chat() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi — tell me what symptoms you're noticing, or upload a report instead. I'll flag a risk level and explain the reasoning behind it." },
  ]);
  const [input, setInput] = useState("");
  const [context, setContext] = useState("General");
  const [isTyping, setIsTyping] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || isTyping) return;

    setMessages((prev) => [...prev, { sender: "user", text }]);
    setInput("");
    setIsTyping(true);

    // The backend's ChatRequest only takes a single "question" field, so
    // fold the selected disease context into the question itself rather
    // than dropping the pill selector.
    const question = context === "General" ? text : `[${context}] ${text}`;

    try {
      const data = await sendChatMessage(question);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.answer, sources: data.sources },
      ]);
    } catch {
      // Backend not reachable at all (not even the dummy fallback) —
      // degrade gracefully instead of leaving the user stuck.
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "(offline) Backend isn't reachable — this is a placeholder reply." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <section className="chat-page">
      <div className="chat-page-header">
        <div>
          <h2 className="chat-title">Symptom chat</h2>
          <p className="chat-subtitle">Ask about symptoms, conditions, or your last prediction.</p>
        </div>
        <div className="context-pills">
          {CONTEXTS.map((c) => (
            <button
              key={c}
              className={`context-pill ${context === c ? "active" : ""}`}
              onClick={() => setContext(c)}
              type="button"
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      <div className="chat-window glass">
        {messages.map((m, i) => (
          <ChatBubble key={i} text={m.text} sender={m.sender} sources={m.sources} />
        ))}
        {isTyping && <ChatBubble sender="bot" typing />}
        <div ref={endRef} />
      </div>
      <div className="chat-input-row">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Describe a symptom or ask a question…"
        />
        <button
          className="btn btn-primary chat-send"
          onClick={sendMessage}
          disabled={isTyping || !input.trim()}
          type="button"
        >
          <HiOutlinePaperAirplane />
        </button>
      </div>
    </section>
  );
}
