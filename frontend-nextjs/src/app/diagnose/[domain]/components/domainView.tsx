// // app/[domain]/DomainView.tsx

// 'use client';

// import Card from '@/app/components/Card';
// import { useRouter } from 'next/navigation';

// // Define the available subdomains (this can be moved outside if static)
// const subs: Record<string, string[]> = {
//     neurology: ['alzheimers', 'brain_tumor', 'stroke'],
//     cardiology: ['heart_failure', 'arrhythmia'],
//     pulmonology: ['pneumonia', 'asthma'],
// };

// interface Props {
//     domain: string;
// }

// export default function DomainView({ domain }: Props) {
//     const router = useRouter();

//     // Determine the base path for navigation (assuming your route structure is /diagnose/[domain]/[sub])
//     const basePath = `/diagnose/${domain}`;

//     // Handle case where domain is not found
//     if (!subs[domain]) {
//         return <div>Domain not found.</div>; 
//     }

//     return (
//         <div>
//             <h1 className="text-3xl font-bold mb-6 capitalize">{domain} Diagnosis</h1>
//             <div className="grid md:grid-cols-3 gap-6">
//                 {subs[domain].map((s) => (
//                     <Card 
//                         key={s} 
//                         title={s.replace(/_/g, ' ')} 
//                         description="AI model diagnostic pipeline" 
//                         onClick={() => router.push(`${basePath}/${s}`)} 
//                     />
//                 ))}
//             </div>
//         </div>
//     );
// }

'use client';

import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  ChevronLeft, 
  Activity, 
  Brain, 
  Wind, 
  Stethoscope, 
  Microscope,
  ArrowRight
} from 'lucide-react';

// --- Configuration ---

// 1. Domain Styling Configuration (Colors & Icons)
const DOMAIN_CONFIG: Record<string, { color: string; bg: string; icon: any; label: string }> = {
  neurology: { 
    color: 'text-indigo-600', 
    bg: 'bg-indigo-50 border-indigo-100', 
    icon: Brain,
    label: 'Neurology'
  },
  cardiology: { 
    color: 'text-rose-600', 
    bg: 'bg-rose-50 border-rose-100', 
    icon: Activity,
    label: 'Cardiology'
  },
  pulmonology: { 
    color: 'text-teal-600', 
    bg: 'bg-teal-50 border-teal-100', 
    icon: Wind,
    label: 'Pulmonology'
  },
};

// 2. Sub-domain Data (The list of diseases)
const SUBS: Record<string, string[]> = {
  neurology: ['alzheimers', 'brain_tumor', 'stroke'],
  cardiology: ['heart_failure', 'arrhythmia'],
  pulmonology: ['copd', 'pneumonia', 'asthma'],
};

// 3. Detailed Descriptions for UI richness
const SUB_DETAILS: Record<string, string> = {
  alzheimers: 'Cognitive pattern analysis for early stage dementia detection.',
  brain_tumor: 'MRI-based mass detection and segmentation pipeline.',
  stroke: 'Acute ischemic and hemorrhagic stroke classification.',
  heart_failure: 'Ejection fraction analysis and risk stratification.',
  arrhythmia: 'ECG rhythm analysis for Atrial Fibrillation detection.',
  pneumonia: 'X-Ray opacity detection for bacterial/viral pneumonia.',
  asthma: 'Spirometry data analysis for chronic airway inflammation.',
};

// Utility to format text (e.g. "brain_tumor" -> "Brain Tumor")
const formatTitle = (str: string) => {
  return str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

interface Props {
  domain: string;
}

export default function DomainView({ domain }: Props) {
  const router = useRouter();
  const normalizedDomain = domain.toLowerCase();

  // Get config or fallback to generic
  const config = DOMAIN_CONFIG[normalizedDomain] || { 
    color: 'text-gray-600', 
    bg: 'bg-gray-50 border-gray-200', 
    icon: Stethoscope,
    label: domain 
  };

  const Icon = config.icon;
  const subItems = SUBS[normalizedDomain];

  // Error State
  if (!subItems) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500">
        <p className="text-xl font-semibold">Domain Not Found</p>
        <button onClick={() => router.back()} className="text-sky-600 hover:underline mt-2">Go Back</button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        
        {/* Navigation & Header */}
        <div className="mb-12">
          <button 
            onClick={() => router.back()}
            className="flex items-center text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors mb-6 group"
          >
            <ChevronLeft size={16} className="mr-1 group-hover:-translate-x-1 transition-transform" />
            Back to Specialists
          </button>

          <div className="flex items-center gap-4">
            <div className={`p-4 rounded-2xl ${config.bg} ${config.color}`}>
              <Icon size={32} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{config.label} Diagnosis</h1>
              <p className="text-gray-500 mt-1">Select a specific condition to initialize the diagnostic model.</p>
            </div>
          </div>
        </div>

        {/* Grid List */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {subItems.map((item, index) => (
            <DomainCard 
              key={item}
              id={item}
              domainId={normalizedDomain}
              title={formatTitle(item)}
              description={SUB_DETAILS[item] || "Standard AI diagnostic pipeline"}
              index={index}
              onClick={() => router.push(`/diagnose/${normalizedDomain}/${item}`)}
            />
          ))}
        </div>

      </div>
    </div>
  );
}

// Sub-component for individual cards
function DomainCard({ id, domainId, title, description, index, onClick }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      onClick={onClick}
      className="group cursor-pointer bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-lg hover:border-sky-100 transition-all duration-300 relative overflow-hidden"
    >
      {/* Decorative background gradient on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-white to-sky-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      <div className="relative z-10">
        <div className="flex justify-between items-start mb-4">
          <div className="p-3 bg-gray-50 rounded-xl group-hover:bg-white group-hover:shadow-sm transition-all">
            <Microscope size={24} className="text-gray-600 group-hover:text-sky-600" />
          </div>
          <div className="text-gray-300 group-hover:text-sky-500 transition-colors">
            <ArrowRight size={20} className="-translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
          </div>
        </div>
        
        <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-sky-700 transition-colors">
          {title}
        </h3>
        <p className="text-sm text-gray-500 leading-relaxed">
          {description}
        </p>
      </div>
    </motion.div>
  );
}