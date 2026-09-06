/**
 * Virtual Assistant — floating AI chatbot widget.
 * Sends messages to POST /api/assistant and displays responses.
 */
import { useState, useRef, useEffect } from 'react';
import { ArrowUp, Bot, MessageCircle, Sparkles, X } from 'lucide-react';
import * as api from '../lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  suggestions?: Array<{ label: string; action: string }>;
}

export default function VirtualAssistant() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I\'m your KarmaSetu AI assistant. I can help you with:\n• Finding courses\n• Understanding competency frameworks\n• Quiz preparation tips\n• Navigation help\n\nHow can I assist you today?',
      suggestions: [
        { label: 'Find courses', action: 'Show me recommended courses' },
        { label: 'Skill gaps', action: 'What are my skill gaps?' },
        { label: 'Quiz help', action: 'Help me prepare for quizzes' },
      ],
    },
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { id: `u-${Date.now()}`, role: 'user', content: text.trim() };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.chatWithAssistant({ message: text.trim(), language: 'en' });
      const assistantMsg: Message = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        content: res.response,
        suggestions: res.suggested_actions?.map((a: any) => ({ label: a.label || a.action, action: a.action || a.label })),
      };
      setMessages((m) => [...m, assistantMsg]);
    } catch {
      setMessages((m) => [...m, {
        id: `a-${Date.now()}`,
        role: 'assistant',
        content: 'I\'m having trouble connecting right now. Please make sure the backend server is running on port 8000 and try again.',
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  if (!open) {
    return (
      <button className="assistant-fab" onClick={() => setOpen(true)} title="AI Assistant">
        <MessageCircle size={22} />
        <span className="fab-pulse" />
      </button>
    );
  }

  return (
    <div className="assistant-panel">
      <div className="assistant-header">
        <div className="assistant-title">
          <Bot size={18} />
          <span><strong>KarmaSetu AI</strong><small>Virtual Assistant</small></span>
        </div>
        <button className="assistant-close" onClick={() => setOpen(false)}><X size={18} /></button>
      </div>

      <div className="assistant-messages">
        {messages.map((msg) => (
          <div className={`assistant-msg ${msg.role}`} key={msg.id}>
            {msg.role === 'assistant' && <div className="msg-avatar"><Sparkles size={13} /></div>}
            <div className="msg-bubble">
              <p>{msg.content}</p>
              {msg.suggestions && msg.suggestions.length > 0 && (
                <div className="msg-suggestions">
                  {msg.suggestions.map((s, i) => (
                    <button key={i} onClick={() => sendMessage(s.action)}>{s.label}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="assistant-msg assistant">
            <div className="msg-avatar"><Sparkles size={13} /></div>
            <div className="msg-bubble typing"><span /><span /><span /></div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="assistant-input" onSubmit={handleSubmit}>
        <input
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          <ArrowUp size={16} />
        </button>
      </form>
    </div>
  );
}
