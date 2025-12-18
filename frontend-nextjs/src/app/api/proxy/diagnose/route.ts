// import { NextResponse } from 'next/server';

// const ML_URL = process.env.ML_SERVICE_URL || 'http://localhost:4000';

// export async function POST(request: Request) {
//   try {
//     const body = await request.json();
//     const res = await fetch(`${ML_URL}/api/ml/diagnose`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(body),
//     });

//     const text = await res.text();
//     const contentType = res.headers.get('content-type') || '';

//     return new Response(text, {
//       status: res.status,
//       headers: { 'Content-Type': contentType || 'text/plain' },
//     });
//   } catch (err: any) {
//     return NextResponse.json(
//       { error: err?.message || 'Proxy error' },
//       { status: 500 }
//     );
//   }
// }

import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const body = await req.json();
  // forward to Nest backend
  const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/agents/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
