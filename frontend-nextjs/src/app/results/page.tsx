// 'use client';

// import { useEffect, useState } from 'react';
// import { DiagnosisResult } from '@/app/types';

// function safeText(value: any) {
//   if (value === null || value === undefined) return "";
//   if (typeof value === "string") return value;
//   return JSON.stringify(value, null, 2);
// }

// // function formatRetrievedContext(item: any) {
// //   return `
// //   **Case**: ${item.id ?? ""}  
// //   Domain: ${item.domain ?? ""}  
// //   Disease: ${item.disease ?? ""}  
// //   Age: ${item.age ?? "N/A"}  
// //   Symptoms: ${Array.isArray(item.symptoms) ? item.symptoms.join(", ") : "N/A"}  
// //   Diagnosis: ${item.diagnosis ?? ""}  
// //   `.trim();
// // }


// export default function ResultsPage() {
//   const [result, setResult] = useState<DiagnosisResult | null>(null);

//   useEffect(() => {
//     const raw = localStorage.getItem('diagnosis_result');
//     if (raw) setResult(JSON.parse(raw));
//   }, []);

//   if (!result) return <p>No results found.</p>;

//   return (
//     <div className="max-w-2xl mx-auto bg-white p-8 rounded-2xl shadow">
//       <h1 className="text-3xl font-bold mb-4">Diagnosis Report</h1>

//       <p className="text-lg mb-2">
//         <strong>Condition:</strong> {safeText(result.condition ?? result.diagnosis)}
//       </p>

//       {result.confidence !== undefined && (
//         <p className="text-lg mb-2">
//           <strong>Confidence:</strong> {result.confidence}%
//         </p>
//       )}

//       <p className="text-lg mb-2">
//         <strong>Recommendation:</strong> {safeText(result.recommendation ?? result.rationale)}
//       </p>

//       {/* <div className="mt-4">
//         <h3 className="font-semibold">Retrieved Context</h3>
//         <ul className="list-disc list-inside text-sm text-gray-700">
//           {(result.retrieved ?? []).map((r: any, i: number) => (
//             <li key={i} className="mb-2 whitespace-pre-line">
//               {formatRetrievedContext(r)}
//             </li>
//           ))}
//         </ul>
//       </div> */}
//       <div className="mt-6">
//         <h3 className="text-xl font-semibold mb-3">Retrieved Context</h3>

//         <div className="space-y-4">
//           {(result.retrieved ?? []).map((item: any, i: number) => (
//             <div
//               key={i}
//               className="border rounded-lg p-4 shadow-sm bg-gray-50"
//             >
//               {item.id && (
//                 <p className="text-sm text-gray-700">
//                   <strong>Case ID:</strong> {item.id}
//                 </p>
//               )}

//               <p className="text-sm text-gray-700">
//                 <strong>Domain:</strong> {item.domain ?? "N/A"}
//               </p>

//               <p className="text-sm text-gray-700">
//                 <strong>Disease:</strong> {item.disease ?? "N/A"}
//               </p>

//               {item.age && (
//                 <p className="text-sm text-gray-700">
//                   <strong>Age:</strong> {item.age}
//                 </p>
//               )}

//               {item.symptoms && (
//                 <p className="text-sm text-gray-700">
//                   <strong>Symptoms:</strong> {item.symptoms.join(", ")}
//                 </p>
//               )}

//               <p className="text-sm text-gray-700">
//                 <strong>Diagnosis:</strong> {item.diagnosis}
//               </p>
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// }

'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  AlertCircle, 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  FileText, 
  Info, 
  Stethoscope, 
  BrainCircuit, 
  LucideDownload
} from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { DiagnosisResult } from '@/app/types';

// Utility for cleaner tailwind classes
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function safeText(value: any) {
  if (value === null || value === undefined) return "Not specified";
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}

// Color logic for confidence score
const getConfidenceColor = (score: number) => {
  if (score >= 80) return "text-emerald-600 bg-emerald-50 border-emerald-200";
  if (score >= 50) return "text-amber-600 bg-amber-50 border-amber-200";
  return "text-red-600 bg-red-50 border-red-200";
};

const getProgressBarColor = (score: number) => {
  if (score >= 80) return "bg-emerald-500";
  if (score >= 50) return "bg-amber-500";
  return "bg-red-500";
};

export default function ResultsPage() {
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showContext, setShowContext] = useState(false);

  useEffect(() => {
    // Simulate a small delay for a smoother "app-like" feel
    const timer = setTimeout(() => {
      const raw = localStorage.getItem('diagnosis_result');
      if (raw) setResult(JSON.parse(raw));
      setLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
        <p className="text-gray-500 font-medium animate-pulse">Analyzing medical data...</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
        <div className="text-center max-w-md">
          <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800">No Diagnosis Found</h2>
          <p className="text-gray-500 mt-2">There is no result data stored. Please return to the intake form.</p>
        </div>
      </div>
    );
  }

  const confidenceScore = result.confidence ?? 0;
  const condition = safeText(result.condition ?? result.diagnosis);
  const recommendation = safeText(result.recommendation ?? result.rationale);

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-3xl mx-auto"
      >
        {/* Header Badge */}
        <div className="flex items-center justify-center mb-8">
          <span className="bg-indigo-100 text-indigo-700 px-4 py-1.5 rounded-full text-sm font-semibold flex items-center gap-2 shadow-sm">
            <BrainCircuit size={16} />
            AI Diagnostic Report
          </span>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
          
          {/* Top Section: Condition & Confidence */}
          <div className="p-8 border-b border-gray-100 bg-gradient-to-br from-white to-gray-50">
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
              
              <div className="flex-1">
                <h2 className="text-sm uppercase tracking-wider text-gray-500 font-bold mb-2 flex items-center gap-2">
                  <Activity size={16} /> Detected Condition
                </h2>
                <h1 className="text-4xl font-extrabold text-gray-900 leading-tight">
                  {condition}
                </h1>
              </div>

              {/* Confidence Meter */}
              <div className={cn("rounded-2xl p-4 border min-w-[160px] text-center", getConfidenceColor(confidenceScore))}>
                <p className="text-xs font-bold uppercase tracking-wider opacity-80 mb-1">Confidence</p>
                <p className="text-3xl font-black">{confidenceScore}</p>
                {/* <p className="text-3xl font-black">75%</p> */}
                <div className="w-full bg-black/10 h-2 rounded-full mt-2 overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${confidenceScore}%` }}
                    // animate={{ width: '75%' }}
                    transition={{ delay: 0.4, duration: 1 }}
                    className={cn("h-full", getProgressBarColor(confidenceScore))}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Recommendation Section */}
          <div className="p-8 bg-white">
            <div className="flex gap-4">
              <div className="mt-1 flex-shrink-0">
                <div className="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center">
                  <Stethoscope size={20} />
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Recommendation & Rationale</h3>
                <p className="text-gray-600 leading-relaxed text-lg">
                  {recommendation}
                </p>
              </div>
            </div>
          </div>

          {/* Expandable Context Section */}
          <div className="bg-gray-50 border-t border-gray-200">
            <button
              onClick={() => setShowContext(!showContext)}
              className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-100 transition-colors focus:outline-none"
            >
              <div className="flex items-center gap-3">
                <div className="bg-white p-2 rounded-lg shadow-sm border border-gray-200">
                  <FileText size={18} className="text-gray-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Reference Evidence</h3>
                  <p className="text-sm text-gray-500">Based on {(result.retrieved ?? []).length} similar historical cases</p>
                </div>
              </div>
              {showContext ? <ChevronUp className="text-gray-400" /> : <ChevronDown className="text-gray-400" />}
            </button>

            <AnimatePresence>
              {showContext && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-6 pt-0 space-y-4">
                    {(result.retrieved ?? []).map((item: any, i: number) => (
                      <ContextCard key={i} item={item} index={i} />
                    ))}
                    {(result.retrieved ?? []).length === 0 && (
                      <p className="text-center text-gray-500 italic py-4">No specific context retrieved.</p>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="mt-6 flex justify-center gap-4">
          <button 
            onClick={() => window.print()}
            className="text-sm font-medium border px-4 py-2 text-red-500 hover:text-blue-900 transition-colors flex items-center gap-2"
          >
            <LucideDownload size={14} /> Download / Print Report
          </button>
        </div>

      </motion.div>
    </div>
  );
}

// Sub-component for individual context cards to keep main file clean
// function ContextCard({ item, index }: { item: any, index: number }) {
//   return (
//     <motion.div
//       initial={{ opacity: 0, x: -10 }}
//       animate={{ opacity: 1, x: 0 }}
//       transition={{ delay: index * 0.1 }}
//       className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
//     >
//       <div className="flex items-center justify-between mb-3 border-b border-gray-100 pb-2">
//         <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
//           Case ID: {item.id ?? "Unknown"}
//         </span>
//         {item.domain && (
//           <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
//             {item.domain}
//           </span>
//         )}
//       </div>
      
//       <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//         <div>
//           <p className="text-xs text-gray-500 mb-1">Disease / Condition</p>
//           <p className="font-medium text-gray-800">{item.disease ?? "N/A"}</p>
//         </div>
//         <div>
//           <p className="text-xs text-gray-500 mb-1">Diagnosis</p>
//           <p className="font-medium text-gray-800">{item.diagnosis ?? "N/A"}</p>
//         </div>
//       </div>

//       <div className="mt-4 bg-gray-50 p-3 rounded-lg">
//         <div className="flex gap-2 items-start">
//           <Info size={14} className="text-gray-400 mt-1 flex-shrink-0" />
//           <div className="text-sm text-gray-700">
//             <span className="font-semibold block text-xs text-gray-500 uppercase mb-1">Symptoms ({item.age ? `Age: ${item.age}` : 'Age: N/A'})</span>
//             {Array.isArray(item.symptoms) ? item.symptoms.join(", ") : "No symptoms listed"}
//           </div>
//         </div>
//       </div>
//     </motion.div>
//   );
// }

function ContextCard({ item, index }: { item: any, index: number }) {
  const domainColors: Record<string, string> = {
    neurology: "bg-purple-100 text-purple-700",
    cardiology: "bg-red-100 text-red-700",
    pulmonology: "bg-blue-100 text-blue-700",
    general: "bg-green-100 text-green-700",
  };

  const badgeColor =
    domainColors[item.domain?.toLowerCase()] || "bg-gray-100 text-gray-600";

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className="
        p-5 rounded-xl shadow-md hover:shadow-lg transition-all border border-gray-200
        bg-gradient-to-br from-white via-gray-50 to-gray-100
      "
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-2 border-b border-gray-200">
        <span className="text-xs font-semibold text-gray-500 tracking-wider">
          Case ID: {item.id ?? "Unknown"}
        </span>

        {item.domain && (
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${badgeColor}`}>
            {item.domain}
          </span>
        )}
      </div>

      {/* Disease + Diagnosis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-500 mb-1">Disease / Condition</p>
          <p className="font-semibold text-gray-900">{item.disease ?? "N/A"}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Diagnosis</p>
          <p className="font-semibold text-gray-900">{item.diagnosis ?? "N/A"}</p>
        </div>
      </div>

      {/* Symptoms */}
      <div className="mt-4 bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
        <div className="flex gap-2 items-start">
          <Info size={14} className="text-blue-400 mt-1" />

          <div className="text-sm text-gray-700">
            <span className="font-semibold block text-xs text-gray-500 uppercase mb-1">
              Symptoms ({item.age ? `Age: ${item.age}` : "Age: N/A"})
            </span>

            {Array.isArray(item.symptoms)
              ? item.symptoms.join(", ")
              : "No symptoms listed"}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
