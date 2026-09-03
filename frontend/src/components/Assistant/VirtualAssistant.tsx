/**
 * Floating virtual assistant widget.
 */
import { useState } from 'react';

export default function VirtualAssistant() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<{role: string, text: string}[]>([]);

  const handleSend = async () => {
    if (!message.trim()) return;
    setConversation(prev => [...prev, { role: 'user', text: message }]);

    const res = await fetch('/api/assistant/respond', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, language: 'en' }),
    });
    const data = await res.json();
    setConversation(prev => [...prev, { role: 'assistant', text: data.response }]);
    setMessage('');
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div className="bg-white rounded-xl shadow-2xl w-96 max-h-96 flex flex-col border border-gray-200 mb-4">
          <div className="bg-indigo-600 text-white px-4 py-3 rounded-t-xl flex items-center justify-between">
            <span className="font-semibold">🤖 Learning Assistant</span>
            <button onClick={() => setOpen(false)} className="text-white hover:text-red-200">✕</button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {conversation.map((c, i) => (
              <div key={i} className={`p-3 rounded-lg ${c.role === 'user' ? 'bg-indigo-100 ml-8' : 'bg-gray-100 mr-8'}`}>
                {c.text}
              </div>
            ))}
          </div>
          <div className="p-3 border-t">
            <div className="flex gap-2">
              <input
                value={message}
                onChange={e => setMessage(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
                placeholder="Ask me anything..."
                className="flex-1 border rounded-lg px-3 py-2 text-sm"
              />
              <button onClick={handleSend} className="bg-indigo-600 text-white px-4 py-2 rounded-lg">Send</button>
            </div>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(!open)}
        className="w-14 h-14 bg-indigo-600 hover:bg-indigo-700 rounded-full shadow-lg flex items-center justify-center text-white text-2xl"
      >
        {open ? '✕' : '🤖'}
      </button>
    </div>
  );
}
