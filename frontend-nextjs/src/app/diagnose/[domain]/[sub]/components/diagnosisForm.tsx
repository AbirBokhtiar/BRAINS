// // app/[domain]/[sub]/DiagnosisForm.tsx

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { postDiagnosis } from '@/app/lib/api';
import { PatientPayload } from '@/app/types';

interface Props {
  domain: string;
  sub: string;
}

export default function DiagnosisForm({ domain, sub }: Props) {
    const router = useRouter();
    
    // 1. Add State for Age
    const [age, setAge] = useState<string>(''); 
    const [symptoms, setSymptoms] = useState('');
    const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
    const [image, setImage] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);

    const toBase64 = (file: File) => new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = reject;
    });

    // Domain-aware symptom suggestions (can be extended)
    const symptomOptionsByDomain: Record<string, string[]> = {
        neurology: [
            'memory loss',
            'confusion',
            'headache',
            'weakness',
            'seizures',
        ],
        cardiology: [
            'chest pain',
            'shortness of breath',
            'palpitations',
            'fatigue',
            'edema',
        ],
        pulmonology: [
            'cough',
            'wheeze',
            'sputum production',
            'dyspnea',
            'chronic cough',
        ],
        general: [
            'fever',
            'fatigue',
            'nausea',
            'dizziness',
            'weight loss',
        ],
    };

    const options = symptomOptionsByDomain[domain.toLowerCase()] ?? symptomOptionsByDomain['general'];

    const toggleSymptom = (s: string) => {
        setSelectedSymptoms(prev => {
            if (prev.includes(s)) return prev.filter(x => x !== s);
            return [...prev, s];
        });
    };

    const handleSubmit = async () => {
        // 2. Basic Validation - require age and at least one symptom (selected or typed)
        if (!age || (selectedSymptoms.length === 0 && !symptoms.trim())) {
            alert("Please provide Age and at least one symptom (select from options or type). ");
            return;
        }

        setLoading(true);
        
        try {
            // 3. Construct Payload with Age
            // Combine selected symptom options with custom symptom text
            const freeList = symptoms
                .split(/[,\n]/)
                .map(s => s.trim())
                .filter(Boolean);
            const combinedSymptoms = Array.from(new Set([...selectedSymptoms, ...freeList]));

            const payload: PatientPayload = {
                age: parseInt(age, 10), // Ensure it is a number
                symptoms: combinedSymptoms,
            };
            
            if (image) payload.imageBase64 = await toBase64(image);

            const data = await postDiagnosis(domain, sub, payload);
            localStorage.setItem('diagnosis_result', JSON.stringify(data));
            // router.push('/results');
            router.push('../../../results');
        } catch (err) {
            alert((err as Error).message);
        } finally { 
            setLoading(false); 
        }
    };

    return (
        
        // <div className="space-y-6 max-w-xl mx-auto">
        <div
            className="
                p-6 rounded-2xl space-y-6
                max-w-xl mx-auto
                bg-white/20 
                backdrop-blur-xl 
                border border-white/40
                shadow-[0_8px_32px_rgba(0,0,0,0.12)]
            "
            >
            <div className="bg-gradient-to-br from-sky-50 via-white to-blue-100">
            {/* <h1 className="text-3xl font-bold mb-4 capitalize">{domain} / {sub.replace(/_/g, ' ')}</h1> */}
            <div className="mb-8 bg-white/10 backdrop-blur-lg p-4 rounded-xl border border-white/30 shadow-sm">
                <h1 className="text-3xl font-bold text-sky-700 capitalize">
                    {domain} / {sub.replace(/_/g, ' ')}
                </h1>
                <p className="text-gray-600 mt-1 text-sm">AI-assisted diagnosis form</p>
            </div>
            </div>
            
            {/* 4. Add Age Input Field */}
            <div className="flex flex-col gap-2">
                <label className="font-semibold text-gray-700">Patient Age</label>
                <input 
                    type="number" 
                    className="w-full p-3 border rounded-xl"
                    placeholder="e.g. 74"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                />
            </div>

            {/* Symptom suggestion chips (click to select) */}
            <div className="flex flex-col gap-2">
                <label className="font-semibold text-gray-700">Quick symptom options</label>
                <div className="flex flex-wrap gap-2">
                    {options.map((opt) => {
                        const active = selectedSymptoms.includes(opt);
                        return (
                            <button
                                key={opt}
                                type="button"
                                onClick={() => toggleSymptom(opt)}
                                className={`px-3 py-1 rounded-full border ${active ? 'bg-sky-600 text-white border-sky-600' : 'bg-white text-gray-800'}`}
                            >
                                {opt}
                            </button>
                        );
                    })}
                </div>
            </div>

            <div className="flex flex-col gap-2">
                <label className="font-semibold text-gray-700">Symptoms & History</label>
                <textarea 
                    className="w-full p-4 border rounded-xl" 
                    rows={10} 
                    placeholder="Enter patient symptoms (e.g. memory loss, confusion)..." 
                    value={symptoms} 
                    onChange={(e) => setSymptoms(e.target.value)} 
                />
            </div>

            <div className="flex flex-col gap-2">
                <label className="font-semibold text-gray-700">Medical Imaging (Optional)</label>
                <input 
                    className='w-full p-2 border rounded-xl bg-white' 
                    type="file" 
                    accept="image/*" 
                    onChange={(e) => setImage(e.target.files?.[0] ?? null)} 
                />
            </div>

            <button 
                className="w-full px-6 py-3 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl transition-colors" 
                onClick={handleSubmit}
                disabled={loading}
            >
                {loading ? 'Processing Diagnosis...' : 'Run Diagnosis'}
            </button>
        </div>
    );
}