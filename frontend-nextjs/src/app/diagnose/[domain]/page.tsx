// app/[domain]/page.tsx

import DomainView from './components/domainView'; // Import the new client component

interface PageProps {
    params: {
        domain: string;
    };
}

// This is the Server Component entry point.
export default async function DomainPage({ params }: PageProps) {
    
    // Accessing params here is synchronous and safe.
    const { domain } = await params;

    // Render the Client Component with the extracted string prop.
    return (
        <DomainView domain={domain} />
    );
}