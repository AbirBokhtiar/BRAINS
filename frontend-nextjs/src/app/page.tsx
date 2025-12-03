// 'use client';

// import { useState } from "react";

// export default function Home() {
//   const [mmse, setMmse] = useState(22);
//   const [age, setAge] = useState(67);
//   const [cdr, setCdr] = useState(1.0);
//   const [etiv, setEtiv] = useState(1450);
//   const [nwbv, setNwbv] = useState(0.68);
//   const [apoe, setApoe] = useState("e3/e4");
//   const [sex, setSex] = useState("M");
//   const [result, setResult] = useState<any>(null);
//   const [loading, setLoading] = useState(false);

//   async function submit() {
//     setLoading(true);
//     const payload = { age, mmse, cdr, etiv, nwbv, apoe, sex};
//     try {
//       const res = await fetch("/api/proxy/diagnose", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(payload),
//       });

//       const contentType = res.headers.get("content-type") || "";
//       if (!res.ok) {
//         const body = contentType.includes("application/json") ? await res.json() : await res.text();
//         setResult({ error: `Server returned ${res.status}`, body });
//       } else if (contentType.includes("application/json")) {
//         const data = await res.json();
//         setResult(data);
//       } else {
//         const text = await res.text();
//         setResult({ error: "Non-JSON response from server", status: res.status, body: text });
//       }
//     } catch (e: any) {
//       setResult({ error: e.message });
//     } finally { setLoading(false); }
//   }

//   return (
//     <main style={{ padding: 24 }}>
//       <h1>BRAINS — Demo</h1>
//       <div style={{ marginTop: 16 }}>
//         <label>Age: <input value={age} onChange={(e)=>setAge(Number(e.target.value))} /></label>
//       </div>
//       <div>
//         <label>MMSE: <input value={mmse} onChange={(e)=>setMmse(Number(e.target.value))} /></label>
//       </div>
//       <div>
//         <label>CDR: <input value={cdr} onChange={(e)=>setCdr(Number(e.target.value))} /></label>
//       </div>
//       <div>
//         <label>ETIV: <input value={etiv} onChange={(e)=>setEtiv(Number(e.target.value))} /></label>
//       </div>
//       <div>
//         <label>NWBV: <input value={nwbv} onChange={(e)=>setNwbv(Number(e.target.value))} /></label>
//       </div>
//       <div>
//         <label>APOE: <input value={apoe} onChange={(e)=>setApoe(e.target.value)} /></label>
//       </div>
//       <div>
//         <label>SEX: <input value={sex} onChange={(e)=>setSex(e.target.value)} /></label>
//       </div>
//       <div style={{ marginTop: 12 }}>
//         <button onClick={submit} disabled={loading}>{loading ? "Running..." : "Get Diagnosis"}</button>
//       </div>
//       <div style={{ marginTop: 18 }}>
//         <pre>{JSON.stringify(result, null, 2)}</pre>
//       </div>
//     </main>
//   );
// }

// import Link from 'next/link';


// export default function Home() {
// return (
//   <div className="text-center py-20">
//     <h1 className="text-5xl font-bold mb-6 text-sky-700">AI-Powered Healthcare Diagnostics</h1>
//     <p className="text-lg text-gray-600 mb-10 max-w-2xl mx-auto">
//       Multi-agent medical diagnostic platform — specialist pipelines for cardiology, neurology, and pulmonology.
//     </p>
//     <Link href="/diagnose" className="px-8 py-4 bg-sky-600 text-white rounded-xl shadow hover:bg-sky-700">
//       Start Diagnosis
//     </Link>
//   </div>
// );
// }



'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { 
  ArrowRight, 
  Brain, 
  HeartPulse, 
  Wind, 
  Sparkles 
} from 'lucide-react';

export default function Home() {
  return (
    <div className="relative min-h-screen bg-gray-50 overflow-hidden flex flex-col justify-center items-center selection:bg-sky-100">
      
      {/* Background Decor Elements (Blobs) */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-sky-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob" />
      <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000" />
      <div className="absolute -bottom-32 left-20 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000" />

      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        
        {/* Intro Badge */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-sky-100 shadow-sm mb-8"
        >
          <Sparkles size={16} className="text-sky-500" />
          <span className="text-sm font-semibold text-gray-600 tracking-wide uppercase">
            Next-Gen Medical AI
          </span>
        </motion.div>

        {/* Main Heading */}
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-6"
        >
          Intelligent <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 to-indigo-600">Diagnostics</span>
          <br /> for Modern Healthcare
        </motion.h1>

        {/* Subtext */}
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed"
        >
          Harness the power of multi-agent architecture. Our specialized AI pipelines analyze clinical data with precision for enhanced decision support.
        </motion.p>

        {/* Call to Action Button */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Link 
            href="/diagnose" 
            className="group relative inline-flex items-center justify-center gap-3 px-8 py-4 bg-sky-600 text-white text-lg font-semibold rounded-2xl shadow-lg shadow-sky-500/30 hover:bg-sky-700 hover:scale-105 transition-all duration-300"
          >
            Start New Diagnosis
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <p className="mt-4 text-sm text-gray-400">Secure • HIPAA Compliant Design • Instant Analysis</p>
        </motion.div>

        {/* Feature Cards (The "Agents") */}
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 text-left"
        >
          <FeatureCard 
            icon={<HeartPulse className="w-8 h-8 text-rose-500" />}
            title="Cardiology Agent"
            desc="Analyzes heart rhythm, ECG data, and cardiovascular risk factors."
          />
          <FeatureCard 
            icon={<Brain className="w-8 h-8 text-indigo-500" />}
            title="Neurology Agent"
            desc="Evaluates neurological symptoms, stroke risks, and cognitive patterns."
          />
          <FeatureCard 
            icon={<Wind className="w-8 h-8 text-teal-500" />}
            title="Pulmonology Agent"
            desc="Respiratory assessment including lung function and breath sound analysis."
          />
        </motion.div>

      </div>
    </div>
  );
}

// Sub-component for the feature cards
function FeatureCard({ icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      <div className="mb-4 bg-gray-50 w-14 h-14 rounded-xl flex items-center justify-center">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 leading-relaxed">{desc}</p>
    </div>
  );
}