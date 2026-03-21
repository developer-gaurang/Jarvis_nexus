<div align="center">

<img src="Project_Preview.png" alt="Jarvis Nexus Core" width="350"/>

# 🌌 **J.A.R.V.I.S  NEXUS** 

### ⟦ Next-Generation Cognitive Cloud Assistant ⟧

[![System Status](https://img.shields.io/badge/System_Status-ONLINE-00ff00?style=for-the-badge&logo=power-bi&logoColor=black)](https://github.com/developer-gaurang/Jarvis_nexus)
[![Core Processing](https://img.shields.io/badge/Core_Processing-Gemini_&_Groq-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](#)
[![Neural Render](https://img.shields.io/badge/Neural_Render-React_Three_Fiber-000000?style=for-the-badge&logo=react&logoColor=00e5ff)](#)
[![Data Pipeline](https://img.shields.io/badge/Data_Pipeline-FastAPI_v0.100+-282828?style=for-the-badge&logo=fastapi&logoColor=white)](#)

*“Bridging the gap between human intuition and hyper-threaded computational logic.”*

---

</div>

<br>

<div align="center">
  <p>
    <strong>JARVIS Nexus</strong> is not just a chatbot—it’s an immersive, cybernetic 3D artificial intelligence platform. Powered by state-of-the-art LLMs, WebSockets, and WebGL rendering, this ecosystem is built to interpret, visualize, and execute commands at near-zero latency.
  </p>
</div>

<br>

## ⚡ ⟨ 01. CORE PROTOCOLS & CAPABILITIES ⟩

- **✧ Multilingual NLP Engine:** Real-time polyglot translation, deep intent recognition, and empathetic reasoning via Google Gemini (2.5 Flash) and parallel Groq tensor operations.
- **✧ Synchronous Data Stream:** Bidirectional WebSocket data-links ensuring uninterrupted zero-latency communication between the UI matrix and the backend brain.
- **✧ Holographic 3D CLI Matrix:** A fully reactive cinematic user interface crafted with `@react-three/fiber` and `@react-three/drei`. The UI visually dilates and reacts dynamically to audio telemetry.
- **✧ Modular "Skill" Subroutines:** The Nexus Architecture is highly uncoupled. Distinct neural skills (e.g., Image Generation, System Diagnostics, Speech Engines) can be hot-swapped or modified on the fly without system downtime.
- **✧ Aesthetic Cyberpunk Shell:** A dark-mode, neon-accented, glassmorphic layout powered by Tailwind CSS. Toggle the visual "Dev Mask" for an authentic terminal-command line appearance.
- **✧ Hyper-Secure Sandboxing (.env):** All API operations remain strictly isolated in the backend. 🛡️ *Sensitive API tokens are cryptographically firewalled inside local environments, ensuring no credential leaks.*

---

## 💻 ⟨ 02. SYSTEM ARCHITECTURE ⟩

The backend and frontend communicate like brain synapses. Below is the exact data topography of the project architecture:

```mermaid
graph TD
    classDef react fill:#0d1117,stroke:#00e5ff,stroke-width:2px;
    classDef python fill:#0d1117,stroke:#00ff00,stroke-width:2px;
    classDef ai fill:#0d1117,stroke:#b200ff,stroke-width:2px;

    subgraph 🌐 Holographic Frontend
        A[React 3D UI / Vite]:::react
        A1(Microphone Input / TTS):::react
        A2(Three.js Render Engine):::react
        A --- A1
        A --- A2
    end

    subgraph 🧠 FastAPI Core Backend
        B[FastAPI Application]:::python
        C{Intent Router / Skill Manager}:::python
        D[Local Hardware Monitor / Audio]:::python
    end

    subgraph ☁️ External Quantum Cognitive Services
        E[Google Gemini LLM / Groq API]:::ai
        F[Pollinations.ai / Neural Image Gen]:::ai
    end

    %% Bidirectional Streams
    A <==>|Bi-directional WebSockets (JSON Payload)| B
    
    %% Backend Logic
    B --> C
    C -.->|Native Skills| D
    C ==>|Semantic Analysis Fallback| E
    C -.->|Image Requests| F
    
    %% Callbacks
    D -.-> B
    E ==>|AI Output Stream| B
    F -.->|Base64 / URL Payload| B
```

---

## 🔧 ⟨ 03. TECHNOLOGICAL STACK ⟩

<details open>
<summary><b>Click to expand System Specs...</b></summary>

| **Sector** | **Component** | **Purpose** |
|:---|:---|:---|
| **Render Engine** | React 19 / Three.js / R3F | Drives the real-time 3D models, user interactions, and spatial UI layout. |
| **Stylization** | Tailwind CSS / Framer Motion | Provides the neon-cyber layout, dynamic glassmorphism, and smooth micro-transitions. |
| **Logic & Networking**| FastAPI / Uvicorn (Python) | High-concurrency async servers handling continuous data streaming. |
| **Communication** | WebSockets Protocol | Sustains a persistent connection linking React components directly to Python's main logic loops. |
| **Generative APIs** | Gemini Pro / Groq / SoundDevice | The neural core governing text completion, conversational intelligence, and amplitude sensing. |

</details>

---

## 📷 ⟨ 04. VISUAL TELEMETRY ⟩

> *AWAITING SYSTEM BOOT... (Place visual snapshot of J.A.R.V.I.S running as `Project_Preview.png` in root).*

![Project Preview](Project_Preview.png)

---

## 🚀 ⟨ 05. CORE SYSTEM BOOT SEQUENCE ⟩

To initialize the Jarvis Nexus ecosystem on local hardware, initiate the following cryptographic sequence:

### [1. SYSTEM CLONE]
Acquire the source code from remote servers:
```zsh
git clone https://github.com/developer-gaurang/Jarvis_nexus.git
cd Jarvis_nexus
```

### [2. IGNITE THE BRAIN (BACKEND)]
```zsh
cd backend
pip install -r requirements.txt
```

**⚠️ CRITICAL SECURITY OVERRIDE:** 
Create a `.env` file mapping your cognitive providers. *(.gitignore guarantees this file never leaves your local system.)*
```ini
# backend/.env 
GROQ_API_KEY=your_groq_api_token
GEMINI_API_KEY=your_gemini_api_token
NANO_BANANA_API_KEY=your_nano_banana_api_key
```

Execute the primary server process:
```zsh
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### [3. ENGAGE HOLOGRAPHIC UI (FRONTEND)]
Initialize a secondary terminal to boot the Vite SPA:
```zsh
cd frontend
npm install
npm run dev
```

### [4. ESTABLISH NEXUS LINK]
Navigate any modern Chromium/WebKit browser to: -> `http://localhost:5173/`
> *Observe the log outputs confirming: `[WS] Connected`. The system is now fully synced and operational.*

---

<div align="center">
  <p><strong>Developed by: <a href="https://github.com/developer-gaurang" style="color:#00ff00; text-decoration:none;">Gaurang Verma</a></strong></p>
  <i>Running on pure logic, imagination, and zero downtime.</i>
</div>
