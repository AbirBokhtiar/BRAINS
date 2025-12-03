// 'use client';
// import { useState } from 'react';
// import { askAssistant } from '@/app/lib/api';


// type Msg = { sender: 'user' | 'bot'; text: string };
// export default function ChatPage() {
// const [messages, setMessages] = useState<Msg[]>([]);
// const [input, setInput] = useState('');
// const [loading, setLoading] = useState(false);


// const sendMessage = async () => {
// if (!input.trim()) return;
// const userMsg: Msg = { sender: 'user', text: input };
// setMessages((m) => [...m, userMsg]);
// setLoading(true);
// try {
// const res = await askAssistant(input);
// setMessages((m) => [...m, { sender: 'bot', text: res.reply }]);
// } catch (err) {
// setMessages((m) => [...m, { sender: 'bot', text: 'Error: ' + (err as Error).message }]);
// } finally { setLoading(false); setInput(''); }
// };


// return (
//     <div className="max-w-2xl mx-auto space-y-4">
//         <div className="h-[500px] overflow-y-auto p-4 bg-white border rounded-2xl space-y-3">
//             {messages.map((m, i) => (
//             <div key={i} className={`p-3 rounded-xl max-w-[80%] ${m.sender === 'user' ? 'bg-sky-600 text-white ml-auto' : 'bg-gray-100'}`}>
//                 {m.text}
//             </div>
//             ))}
//         </div>
//         <div className="flex gap-2">
//             <input value={input} onChange={(e) => setInput(e.target.value)} className="flex-1 p-3 border rounded-xl" placeholder="Ask something mentioning the age of the patient..." />
//             <button onClick={sendMessage} className="px-6 py-3 bg-sky-600 text-white rounded-xl">{loading ? '...' : 'Send'}</button>
//         </div>
        
//         {/* Typing Dots Animation Styling */}
//         <style jsx>{`
//             .dot {
//             width: 7px;
//             height: 7px;
//             border-radius: 50%;
//             display: inline-block;
//             animation: blink 1.4s infinite both;
//             }
//             .dot:nth-child(2) {
//             animation-delay: 0.2s;
//             }
//             .dot:nth-child(3) {
//             animation-delay: 0.4s;
//             }
//             @keyframes blink {
//             0% {
//                 opacity: 0.2;
//             }
//             20% {
//                 opacity: 1;
//             }
//             100% {
//                 opacity: 0.2;
//             }
//             }
//         `}</style>
//     </div>
// );
// }

//////////////////////////////////////////////////////////


// 'use client';

// import { useEffect, useRef, useState } from 'react';
// import { askAssistant } from '@/app/lib/api';

// type Msg = { sender: 'user' | 'bot'; text: string };

// export default function ChatPage() {
//   const [messages, setMessages] = useState<Msg[]>([]);
//   const [input, setInput] = useState('');
//   const [loading, setLoading] = useState(false);
//   const scrollRef = useRef<HTMLDivElement | null>(null);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     const userMsg: Msg = { sender: 'user', text: input };
//     setMessages((m) => [...m, userMsg]);
//     setLoading(true);

//     try {
//       const res = await askAssistant(input);
//       setMessages((m) => [...m, { sender: 'bot', text: res.reply }]);
//     } catch (err) {
//       setMessages((m) => [
//         ...m,
//         { sender: 'bot', text: 'Error: ' + (err as Error).message },
//       ]);
//     } finally {
//       setLoading(false);
//       setInput('');
//     }
//   };

//   // Auto scroll to bottom
//   useEffect(() => {
//     scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages, loading]);

//   return (
//     <div className="flex flex-col h-screen bg-gray-50">
//       {/* HEADER */}
//       <div className="p-4 bg-sky-600 text-white shadow-md">
//         <h1 className="text-xl font-semibold tracking-wide">BRAINS Assistant</h1>
//         <p className="text-sm opacity-80">AI Medical Diagnostics Platform</p>
//       </div>

//       {/* CHAT AREA */}
//       <div className="flex-1 overflow-y-auto p-5 space-y-4">
//         {messages.map((m, i) => (
//           <div
//             key={i}
//             className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
//           >
//             <div
//               className={`max-w-[75%] px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed transition 
//                 ${
//                   m.sender === 'user'
//                     ? 'bg-sky-600 text-white rounded-br-none'
//                     : 'bg-white text-gray-800 border rounded-bl-none'
//                 }`}
//             >
//               {m.text}
//             </div>
//           </div>
//         ))}

//         {/* Typing Animation */}
//         {loading && (
//           <div className="flex items-center space-x-2">
//             <div className="bg-white px-4 py-3 rounded-2xl shadow border text-gray-600 max-w-[60%]">
//               <div className="typing-dots flex space-x-1">
//                 <span className="dot bg-gray-500"></span>
//                 <span className="dot bg-gray-500"></span>
//                 <span className="dot bg-gray-500"></span>
//               </div>
//             </div>
//           </div>
//         )}

//         <div ref={scrollRef} />
//       </div>

//       {/* INPUT BAR */}
//       <div className="p-4 bg-white border-t shadow-sm flex gap-3">
//         <input
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Describe symptoms or ask anything..."
//           className="flex-1 px-4 py-3 border rounded-xl bg-gray-50 focus:ring-2 focus:ring-sky-500 outline-none"
//         />
//         <button
//           onClick={sendMessage}
//           disabled={loading}
//           className="px-6 py-3 bg-sky-600 text-white rounded-xl hover:bg-sky-700 transition disabled:opacity-50"
//         >
//           {loading ? '...' : 'Send'}
//         </button>
//       </div>

//       {/* Typing Dots Animation Styling */}
//       <style jsx>{`
//         .dot {
//           width: 7px;
//           height: 7px;
//           border-radius: 50%;
//           display: inline-block;
//           animation: blink 1.4s infinite both;
//         }
//         .dot:nth-child(2) {
//           animation-delay: 0.2s;
//         }
//         .dot:nth-child(3) {
//           animation-delay: 0.4s;
//         }
//         @keyframes blink {
//           0% {
//             opacity: 0.2;
//           }
//           20% {
//             opacity: 1;
//           }
//           100% {
//             opacity: 0.2;
//           }
//         }
//       `}</style>
//     </div>
//   );
// }


// 'use client';

// import { useEffect, useState, useRef } from 'react';
// // import ReactMarkdown from 'react-markdown';
// import { askAssistant } from '@/app/lib/api';

// type Msg = {
//   sender: 'user' | 'bot';
//   text: string;
//   time: string;
// };

// const DOMAINS = ["Neurology", "Cardiology", "Pulmonology"];

// export default function ChatPage() {
//   const [messages, setMessages] = useState<Msg[]>([]);
//   const [input, setInput] = useState('');
//   const [selectedDomain, setSelectedDomain] = useState<string>('Neurology');
//   const [loading, setLoading] = useState(false);
//   const scrollRef = useRef<HTMLDivElement | null>(null);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

//     const userMsg: Msg = {
//       sender: 'user',
//       text: input,
//       time: timestamp,
//     };

//     setMessages((m) => [...m, userMsg]);
//     setLoading(true);

//     try {
//       const res = await askAssistant(`Domain: ${selectedDomain}. ${input}`);
//       const botMsg: Msg = {
//         sender: 'bot',
//         text: res.reply,
//         time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
//       };
//       setMessages((m) => [...m, botMsg]);
//     } catch (err) {
//       setMessages((m) => [
//         ...m,
//         {
//           sender: 'bot',
//           text: 'Error: ' + (err as Error).message,
//           time: timestamp,
//         },
//       ]);
//     } finally {
//       setInput('');
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages, loading]);

//   return (
//     <div className="h-screen flex bg-gray-50">

//       {/* SIDEBAR */}
//       <aside className="w-56 bg-white border-r p-5 shadow-sm">
//         <h2 className="text-lg font-semibold mb-4">Select Domain</h2>
//         <div className="space-y-2">
//           {DOMAINS.map((d) => (
//             <button
//               key={d}
//               onClick={() => setSelectedDomain(d)}
//               className={`block w-full text-left p-2 rounded-lg
//               ${selectedDomain === d ? 'bg-sky-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
//             >
//               {d}
//             </button>
//           ))}
//         </div>
//       </aside>

//       {/* MAIN CHAT */}
//       <div className="flex flex-col flex-1 h-full">
//         {/* HEADER */}
//         <div className="p-4 bg-sky-600 text-white shadow">
//           <h1 className="text-xl font-semibold">BRAINS Assistant</h1>
//           <p className="text-sm opacity-80">Specialist: {selectedDomain}</p>
//         </div>

//         {/* CHAT WINDOW */}
//         <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
//           {messages.map((m, i) => (
//             <div key={i} className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>

//               {/* Avatar */}
//               {m.sender === 'bot' && (
//                 <div className="w-10 h-10 bg-sky-600 text-white rounded-full flex items-center justify-center">
//                   🤖
//                 </div>
//               )}

//               <div
//                 className={`
//                   max-w-[80%] px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed 
//                   animate-fadeIn relative
//                   ${
//                     m.sender === 'user'
//                       ? 'bg-sky-600 text-white rounded-br-none'
//                       : 'bg-white border text-gray-800 rounded-bl-none'
//                   }
//                 `}
//               >
//                 {/* <ReactMarkdown>{m.text}</ReactMarkdown> */}
//                 {m.text}

//                 {/* Timestamp */}
//                 <div className="text-[10px] opacity-60 mt-1">
//                   {m.time}
//                 </div>
//               </div>

//               {m.sender === 'user' && (
//                 <div className="w-10 h-10 bg-gray-300 text-gray-700 rounded-full flex items-center justify-center">
//                   🧑
//                 </div>
//               )}

//             </div>
//           ))}

//           {/* Typing Indicator */}
//           {loading && (
//             <div className="flex gap-2">
//               <div className="w-10 h-10 bg-sky-600 text-white rounded-full flex items-center justify-center">
//                 🤖
//               </div>
//               <div className="bg-white px-4 py-3 border rounded-2xl shadow max-w-[60%]">
//                 <div className="typing-dots flex space-x-1">
//                   <span className="dot bg-gray-600"></span>
//                   <span className="dot bg-gray-600"></span>
//                   <span className="dot bg-gray-600"></span>
//                 </div>
//               </div>
//             </div>
//           )}

//           <div ref={scrollRef}></div>
//         </div>

//         {/* INPUT BAR */}
//         <div className="p-4 bg-white border-t shadow-sm flex gap-3">
//           <input
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             placeholder="Describe symptoms, ask for diagnosis…"
//             className="flex-1 px-4 py-3 border rounded-xl bg-gray-50 
//               focus:ring-2 focus:ring-sky-500 outline-none"
//           />
//           <button
//             onClick={sendMessage}
//             disabled={loading}
//             className="px-6 py-3 bg-sky-600 text-white rounded-xl hover:bg-sky-700 transition"
//           >
//             {loading ? '...' : 'Send'}
//           </button>
//         </div>
//       </div>

//       {/* ANIMATIONS */}
//       <style jsx>{`
//         .dot {
//           width: 7px;
//           height: 7px;
//           border-radius: 50%;
//           animation: blink 1.4s infinite both;
//         }
//         .dot:nth-child(2) { animation-delay: 0.2s; }
//         .dot:nth-child(3) { animation-delay: 0.4s; }

//         @keyframes blink {
//           0% { opacity: 0.2; }
//           20% { opacity: 1; }
//           100% { opacity: 0.2; }
//         }
//         @keyframes fadeIn {
//           from { opacity: 0; transform: translateY(4px); }
//           to { opacity: 1; transform: translateY(0); }
//         }
//         .animate-fadeIn { animation: fadeIn 0.2s ease-out; }
//       `}</style>
//     </div>
//   );
// }


'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Bot, 
  User, 
  Menu, 
  X, 
  Brain, 
  HeartPulse, 
  Wind, 
  Stethoscope, 
  AlertCircle, 
  HashIcon
} from 'lucide-react';
import { askAssistant } from '@/app/lib/api';

// --- Types ---
type Sender = 'user' | 'bot';
type Msg = {
  id: string;
  sender: Sender;
  text: string;
  time: string;
};

type Domain = 'Neurology' | 'Cardiology' | 'Pulmonology' | 'General';

// --- Configuration ---
const DOMAINS: { id: Domain; icon: any; color: string }[] = [
  { id: 'Neurology', icon: Brain, color: 'text-indigo-500' },
  { id: 'Cardiology', icon: HeartPulse, color: 'text-rose-500' },
  { id: 'Pulmonology', icon: Wind, color: 'text-teal-500' },
  { id: 'General', icon: HashIcon, color: 'text-purple-500'},
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<Domain>('Neurology');
  const [loading, setLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Mobile state
  const scrollRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMsg: Msg = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, newMsg]);
    setInput('');
    setLoading(true);

    try {
      // Simulate API call format. 
      // NOTE: Ensure your askAssistant handles the string correctly.
      const res = await askAssistant(selectedDomain, newMsg.text);
      
      const botMsg: Msg = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: res.reply, // Ensure your API returns 'reply'
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errorMsg: Msg = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: `**System Error:** ${(err as Error).message}. Please try again.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

//   const activeDomainConfig = DOMAINS.find(d => d.id === selectedDomain);
  const activeDomainConfig = DOMAINS.find(d => d.id === selectedDomain) || DOMAINS[0];

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden font-sans text-gray-900">
      
      {/* --- Mobile Sidebar Overlay --- */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(false)}
            className="fixed inset-0 bg-black/50 z-20 md:hidden"
          />
        )}
      </AnimatePresence>

      {/* --- Sidebar --- */}
      <aside className={`
        fixed inset-y-0 left-0 z-30 w-72 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out
        md:relative md:translate-x-0
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6 h-full flex flex-col">
          <div className="flex items-center gap-2 mb-8 text-sky-700 font-bold text-xl">
            <Stethoscope className="w-8 h-8" />
            <span>MediChat AI</span>
          </div>

          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Select Specialist</h3>
          
          <div className="space-y-2 flex-1">
            {DOMAINS.map((domain) => {
              const Icon = domain.icon;
              const isActive = selectedDomain === domain.id;
              return (
                <button
                  key={domain.id}
                  onClick={() => {
                    setSelectedDomain(domain.id);
                    setIsSidebarOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200
                    ${isActive 
                      ? 'bg-sky-50 text-sky-700 shadow-sm border border-sky-100 ring-1 ring-sky-200' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                >
                  <Icon size={20} className={isActive ? domain.color : 'text-gray-400'} />
                  <span className="font-medium">{domain.id}</span>
                  {isActive && <motion.div layoutId="active-dot" className="ml-auto w-2 h-2 bg-sky-500 rounded-full" />}
                </button>
              );
            })}
          </div>

          {/* Sidebar Footer */}
          <div className="mt-auto p-4 bg-gray-50 rounded-xl border border-gray-100">
            <div className="flex gap-3 items-center">
              <div className="w-8 h-8 bg-sky-100 rounded-full flex items-center justify-center">
                <User size={16} className="text-sky-600" />
              </div>
              <div className="text-sm">
                <p className="font-semibold text-gray-900">Dr. Guest</p>
                <p className="text-gray-500 text-xs">Medical ID: #8821</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* --- Main Chat Area --- */}
      <main className="flex-1 flex flex-col h-full relative">
        
        {/* Header */}
        <header className="bg-white border-b border-gray-200 p-4 flex items-center justify-between shadow-sm z-10">
          <div className="flex items-center gap-3">
            <button onClick={() => setIsSidebarOpen(true)} className="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
              <Menu size={24} />
            </button>
            <div>
              <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                {activeDomainConfig?.id} Assistant
                <span className="flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
              </h2>
              <p className="text-xs text-gray-500">AI-powered diagnostic support</p>
            </div>
          </div>
        </header>

        {/* Chat Stream */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400 opacity-60">
              <activeDomainConfig.icon size={64} className="mb-4 text-gray-300" />
              <p>Start a consultation with the {selectedDomain} specialist.</p>
            </div>
          )}

          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} />
          ))}

          {loading && <TypingIndicator />}
          
          <div ref={scrollRef} className="h-4" />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="max-w-4xl mx-auto flex items-end gap-3 p-2 bg-gray-50 border border-gray-200 rounded-2xl shadow-sm focus-within:ring-2 focus-within:ring-sky-100 focus-within:border-sky-300 transition-all">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Provide patient's age and describe symptoms for the ${selectedDomain} agent...`}
              className="flex-1 bg-transparent border-none focus:ring-0 p-3 max-h-32 resize-none text-gray-800 placeholder-gray-400"
              rows={1}
              style={{ minHeight: '48px' }}
            />
            <button 
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="p-3 bg-sky-600 text-white rounded-xl hover:bg-sky-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm mb-1"
            >
              <Send size={18} />
            </button>
          </div>
          <p className="text-center text-xs text-gray-400 mt-2 flex items-center justify-center gap-1">
            <AlertCircle size={12} />
            AI-generated content. Review with clinical protocols.
          </p>
        </div>
      </main>
    </div>
  );
}

// --- Sub Components ---

function MessageBubble({ msg }: { msg: Msg }) {
  const isUser = msg.sender === 'user';
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div className={`
        flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-sm
        ${isUser ? 'bg-sky-600 text-white' : 'bg-white border border-gray-200 text-sky-600'}
      `}>
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>

      {/* Bubble */}
      <div className={`
        max-w-[85%] md:max-w-[70%] rounded-2xl p-4 shadow-sm text-sm leading-relaxed
        ${isUser 
          ? 'bg-sky-600 text-white rounded-tr-none' 
          : 'bg-white border border-gray-100 text-gray-800 rounded-tl-none'
        }
      `}>
        {isUser ? (
          <p className="whitespace-pre-wrap">{msg.text}</p>
        ) : (
          <div className="markdown-body">
            {/* ReactMarkdown renders bolding, lists, etc. properly */}
            <ReactMarkdown 
              components={{
                ul: ({...props}: any) => <ul className="list-disc ml-4 space-y-1 my-2" {...props} />,
                ol: ({...props}: any) => <ol className="list-decimal ml-4 space-y-1 my-2" {...props} />,
                li: ({...props}: any) => <li className="pl-1" {...props} />,
                strong: ({...props}: any) => <span className="font-bold text-sky-700" {...props} />,
                p: ({...props}: any) => <p className="mb-2 last:mb-0" {...props} />,
              }}
            >
              {msg.text}
            </ReactMarkdown>
          </div>
        )}
        <p className={`text-[10px] mt-2 text-right ${isUser ? 'text-sky-200' : 'text-gray-400'}`}>
          {msg.time}
        </p>
      </div>
    </motion.div>
  );
}

function TypingIndicator() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex gap-4"
    >
      <div className="w-10 h-10 bg-white border border-gray-200 text-sky-600 rounded-full flex items-center justify-center shadow-sm">
        <Bot size={18} />
      </div>
      <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-none p-4 shadow-sm flex items-center gap-1">
        <span className="text-xs text-gray-500 mr-2">Analyzing</span>
        <motion.div 
          className="w-1.5 h-1.5 bg-sky-500 rounded-full"
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
        />
        <motion.div 
          className="w-1.5 h-1.5 bg-sky-500 rounded-full"
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
        />
        <motion.div 
          className="w-1.5 h-1.5 bg-sky-500 rounded-full"
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
        />
      </div>
    </motion.div>
  );
}