// app/[domain]/[sub]/page.tsx

import DiagnosisForm from './components/diagnosisForm'; // Import the new client component

interface PageProps {
  // Define the structure of the props received by the page component
  params: {
    domain: string;
    sub: string;
  };
}

// This is the Server Component. It is synchronous by default.
export default async function SubDiagnosisPage({ params }: PageProps) {
  
  // Accessing params here is synchronous and correct in a Server Component.
  const { domain, sub } = await params;

  // Pass the unwrapped strings down as simple props to the Client Component
  return (
    <DiagnosisForm domain={domain} sub={sub} />
    // <DiagnosisForm domain={params.domain} sub={params.sub} />
  );
}