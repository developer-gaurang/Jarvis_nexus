import React, { useState, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { applyDevMask } from './utils/maskHelper';
import JarvisCore from './components/JarvisCore';

export default function App() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [devMaskOn, setDevMaskOn] = useState(false);
  const [chats, setChats] = useState([]);
  const [inputText, setInputText] = useState('');
  const ws = useRef(null);
  const chatContainerRef = useRef(null); // scroll ke liye ref
  
  // 🔊 Web Speech API Ref
  const voiceRef = useRef(null);

  // Initialize Output Voice Streamer
  useEffect(() => {
    const setVoice = () => {
      const voices = window.speechSynthesis.getVoices();
      // Look for a deep, professional British/American Male or fallback
      voiceRef.current = voices.find(v => (v.name.includes('Male') && v.lang.includes('en')) || v.name.includes('David') || v.name.includes('Zira') || v.lang === 'en-GB') || voices[0];
    };
    setVoice();
    window.speechSynthesis.onvoiceschanged = setVoice;
  }, []);

  const outputSpeech = (text) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel(); // Clears queue for immediate sync
    
    // Strip markdown chars (like ** or *) for better speech
    let cleanText = text.replace(/[*_#]/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    
    // Wire TTS State directly to 3D Reactive Component Animation
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    if (voiceRef.current) utterance.voice = voiceRef.current;
    utterance.pitch = 0.9;  // Slightly deeper
    utterance.rate = 1.1;   // Brisk, assistant pacing
    
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws/jarvis');
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setChats((prev) => [...prev, data]);
      
      // Auto-play voice precisely synchronized with text render
      if (data.role === 'JARVIS' && data.content) {
        outputSpeech(data.content);
      }
    };
    return () => { if (ws.current) ws.current.close(); };
  }, []);

  // Naya message aane par auto-scroll down karna
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chats]);

  const handleSend = (e) => {
    if (e.key === 'Enter' && inputText.trim() !== '') {
      // User ka message UI pe dikhao
      setChats((prev) => [...prev, { role: 'User', content: inputText }]);
      // Backend ko command bhejo
      ws.current.send(JSON.stringify({ command: inputText }));
      setInputText('');
    }
  };

  return (
    <div className={`h-screen w-full transition-colors duration-500 flex flex-col overflow-hidden ${devMaskOn ? 'bg-black text-green-500 font-mono' : 'bg-[#030712] text-cyan-400 font-sans'}`}>

      {/* ⭕ Central 3D Canvas Background (No Stars, No Jelly) */}
      <div className="absolute top-0 left-0 w-full h-full z-0 pointer-events-auto flex items-center justify-center">
        <Canvas camera={{ position: [0, 0, 4] }}>
          <ambientLight intensity={1} />
          <directionalLight position={[2, 5, 2]} intensity={2} />
          <JarvisCore isSpeaking={isSpeaking} />
          <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
        </Canvas>
      </div>

      {/* 🛡️ UI Overlay Layout */}
      <div className="relative z-10 flex flex-col h-full pointer-events-none">

        {/* Top Header */}
        <div className="flex justify-between items-center p-6 pointer-events-auto border-b border-white/5 bg-black/20 backdrop-blur-sm">
          <div>
            <h1 className="text-3xl font-bold tracking-[0.2em] uppercase">
              {devMaskOn ? applyDevMask('NEXUS') : 'J.A.R.V.I.S'}
            </h1>
          </div>
          <button
            onClick={() => setDevMaskOn(!devMaskOn)}
            className="px-4 py-2 border border-current rounded hover:bg-current hover:text-black transition-all font-bold uppercase tracking-widest shadow-[0_0_10px_currentColor]"
          >
            {devMaskOn ? 'Disable Mask' : 'Activate Dev Mask'}
          </button>
        </div>

        {/* Chat History Panel (Central Area) */}
        <div
          ref={chatContainerRef} // auto-scroll ke liye refer kiya
          className="flex-1 overflow-y-auto p-6 pointer-events-auto custom-scrollbar w-full max-w-4xl mx-auto mt-4 mb-4 flex flex-col"
          style={{ maxHeight: '65vh' }}
        >
          {chats.length === 0 && (
            <div className="text-center opacity-30 mt-10 tracking-widest text-sm animate-pulse">
              {devMaskOn ? 'AWAITING_ROOT_COMMAND...' : 'AWAITING COMMAND, SIR...'}
            </div>
          )}
          {chats.map((chat, idx) => (
            <div key={idx} className={`mb-6 flex flex-col ${chat.role === 'User' ? 'items-end' : 'items-start'}`}>
              <span className="text-xs opacity-50 uppercase tracking-widest mb-1">
                {chat.role}
              </span>
              <div className={`p-4 rounded-lg backdrop-blur-md border ${chat.role === 'User' ? 'bg-cyan-900/10 border-cyan-500/20 text-white' : 'bg-black/30 border-white/5 text-cyan-400'} ${devMaskOn ? 'border-green-500/30 text-green-400' : ''}`}>
                <p className="text-md leading-relaxed tracking-wide">
                  {devMaskOn ? applyDevMask(chat.content) : chat.content}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Input Box Area */}
        <div className="w-full max-w-4xl mx-auto p-6 pt-0 pointer-events-auto mt-auto mb-4">
          <div className="relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleSend}
              placeholder={devMaskOn ? "> ENTER_BINARY_COMMAND" : "Interface with J.A.R.V.I.S (Type and press Enter)..."}
              className="w-full bg-black/60 backdrop-blur-lg border border-white/10 rounded-lg py-4 px-6 outline-none focus:border-current focus:shadow-[0_0_15px_currentColor] transition-all text-lg shadow-xl"
            />
          </div>
        </div>

      </div>
    </div>
  );
}