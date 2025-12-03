// import Link from 'next/link';


// export default function Navbar() {
// return (
//         <nav className="w-full bg-white shadow py-3">
//             <div className="container mx-auto flex justify-between items-center px-4">
//                 <Link href="/" className="text-2xl font-bold text-sky-600">BRAINS</Link>
//                 <div className="flex items-center gap-6">
//                     <Link href="/diagnose" className="text-sm hover:text-sky-600">Diagnose</Link>
//                     <Link href="/chat" className="text-sm hover:text-sky-600">Assistant</Link>
//                     <Link href="/results" className="text-sm hover:text-sky-600">Reports</Link>
//                 </div>
//             </div>
//         </nav>
//     );
// }

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BrainCircuit, 
  Menu, 
  X, 
  Activity, 
  MessageSquareText, 
  FileText,
  ChevronRight
} from 'lucide-react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  // Detect scroll to add shadow/border styling
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  const navLinks = [
    { name: 'Assistant', href: '/chat', icon: MessageSquareText },
    { name: 'Reports', href: '/results', icon: FileText },
  ];

  return (
    <>
      <nav 
        className={`sticky top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled 
            ? 'bg-white/80 backdrop-blur-md border-b border-gray-200 py-3 shadow-sm' 
            : 'bg-transparent py-5'
        }`}
      >
        <div className="container mx-auto px-6 max-w-7xl flex justify-between items-center">
          
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="bg-sky-600 text-white p-2 rounded-xl group-hover:bg-sky-700 transition-colors">
              <BrainCircuit size={24} />
            </div>
            <span className="text-xl font-bold text-slate-800 tracking-tight">
              BRAINS<span className="text-sky-600">.ai</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link 
                  key={link.href} 
                  href={link.href}
                  className={`text-sm font-medium transition-colors relative group ${
                    isActive ? 'text-sky-600' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {link.name}
                  {/* Active Indicator Dot */}
                  {isActive && (
                    <motion.div 
                      layoutId="nav-dot"
                      className="absolute -bottom-2 left-0 right-0 h-1 bg-sky-600 rounded-full" 
                    />
                  )}
                </Link>
              );
            })}

            {/* CTA Button */}
            <Link 
              href="/diagnose" 
              className="flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white text-sm font-medium rounded-full hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/20 hover:shadow-slate-900/30 hover:-translate-y-0.5"
            >
              <Activity size={16} />
              Start Diagnosis
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button 
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-x-0 top-[70px] z-40 bg-white border-b border-gray-100 shadow-xl md:hidden"
          >
            <div className="flex flex-col p-6 space-y-4">
              {navLinks.map((link) => (
                <Link 
                  key={link.href} 
                  href={link.href}
                  className={`flex items-center gap-3 p-3 rounded-xl transition-colors ${
                    pathname === link.href 
                      ? 'bg-sky-50 text-sky-700 font-semibold' 
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <link.icon size={20} />
                  {link.name}
                  {pathname === link.href && <ChevronRight size={16} className="ml-auto" />}
                </Link>
              ))}
              <div className="h-px bg-gray-100 my-2" />
              <Link 
                href="/diagnose"
                className="flex items-center justify-center gap-2 w-full p-3 bg-sky-600 text-white font-semibold rounded-xl active:scale-95 transition-transform"
              >
                <Activity size={20} />
                Start Diagnosis
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}