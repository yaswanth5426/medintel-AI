import './Chat.css';

import {
  useEffect,
  useRef,
  useState,
} from 'react';

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

    try {
      const data = await sendChatMessage({ message: text, context });
      setMessages((prev) => [...prev, { sender: "bot", text: data.reply }]);
    } catch {
      // Backend not running yet / request failed — degrade gracefully
      // instead of leaving the user stuck. Real answers come from the
      // GenAI engineer's RAG + Gemini pipeline in backend/rag/.
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
        <h2 className="chat-title">Chat</h2>
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

      <div className="chat-window">
        {messages.map((m, i) => (
          <ChatBubble key={i} text={m.text} sender={m.sender} />
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
        <button className="btn btn-primary" onClick={sendMessage} disabled={isTyping}>
          Send
        </button>
      </div>
    </section>
  );
}
