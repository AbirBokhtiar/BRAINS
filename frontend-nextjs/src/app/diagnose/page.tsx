// 'use client';
// import Card from '@/app/components/Card';
// import { useRouter } from 'next/navigation';


// const domains = [
// { name: 'cardiology', label: 'Cardiological Diagnosis' },
// { name: 'neurology', label: 'Neurological Diagnosis' },
// { name: 'pulmonology', label: 'Pulmonological Diagnosis' },
// ];


// export default function DiagnoseIndex() {
// const router = useRouter();
// return (
//     <div className="grid md:grid-cols-3 gap-6">
//     {domains.map((d) => (
//     <Card key={d.name} title={d.label} description="AI specialist diagnostic pipeline" onClick={() => router.push(`/diagnose/${d.name}`)} />
//     ))}
//     </div>
// );
// }

'use client';

import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  HeartPulse, 
  Brain, 
  Wind, 
  ArrowRight, 
  ActivitySquare 
} from 'lucide-react';

// Enhanced data structure for better UI rendering
const domains = [
  { 
    id: 'cardiology', 
    label: 'Cardiology Agent', 
    description: 'Analyzes arrhythmias, ECG patterns, and cardiovascular risk factors using AHA protocols.',
    icon: HeartPulse,
    color: 'text-rose-600',
    bg: 'bg-rose-50',
    border: 'group-hover:border-rose-200',
    shadow: 'group-hover:shadow-rose-100'
  },
  { 
    id: 'neurology', 
    label: 'Neurology Agent', 
    description: 'Evaluates cognitive decline, stroke symptoms, and neuropathic patterns.',
    icon: Brain,
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
    border: 'group-hover:border-indigo-200',
    shadow: 'group-hover:shadow-indigo-100'
  },
  { 
    id: 'pulmonology', 
    label: 'Pulmonology Agent', 
    description: 'Respiratory assessment focusing on COPD indicators, breath sounds, and oxygenation levels.',
    icon: Wind,
    color: 'text-teal-600',
    bg: 'bg-teal-50',
    border: 'group-hover:border-teal-200',
    shadow: 'group-hover:shadow-teal-100'
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

export default function DiagnoseIndex() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        
        {/* Page Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center p-3 bg-white rounded-2xl shadow-sm mb-4 border border-gray-100">
            <ActivitySquare className="w-8 h-8 text-sky-600" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4 tracking-tight">
            Select Diagnostic Protocol
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Choose a specialist AI agent to begin the analysis pipeline. Each agent is optimized for specific clinical domains.
          </p>
        </div>

        {/* Card Grid */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid md:grid-cols-3 gap-8"
        >
          {domains.map((d) => (
            <motion.div
              key={d.id}
              variants={itemVariants}
              whileHover={{ y: -5 }}
              className={`
                group relative bg-white rounded-3xl p-8 cursor-pointer 
                border border-gray-200 transition-all duration-300 shadow-sm hover:shadow-xl
                ${d.border} ${d.shadow}
              `}
              onClick={() => router.push(`/diagnose/${d.id}`)}
            >
              {/* Icon */}
              <div className={`w-14 h-14 rounded-2xl ${d.bg} ${d.color} flex items-center justify-center mb-6 transition-transform group-hover:scale-110`}>
                <d.icon size={28} />
              </div>

              {/* Text Content */}
              <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-sky-700 transition-colors">
                {d.label}
              </h3>
              <p className="text-slate-500 text-sm leading-relaxed mb-8">
                {d.description}
              </p>

              {/* Action Footer */}
              <div className="flex items-center text-sm font-semibold text-slate-900 group-hover:text-sky-600 transition-colors">
                Initialize Agent
                <ArrowRight className="ml-2 w-4 h-4 transition-transform group-hover:translate-x-1" />
              </div>
            </motion.div>
          ))}
        </motion.div>

      </div>
    </div>
  );
}