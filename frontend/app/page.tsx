export default function RootPage() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>TodoApp - Redirecting...</title>
        <meta httpEquiv="refresh" content="0;url=/en" />
      </head>
      <body>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          fontFamily: 'system-ui, -apple-system, sans-serif'
        }}>
          <div style={{ textAlign: 'center' }}>
            <h1>TodoApp</h1>
            <p>Redirecting to English version...</p>
            <p style={{ marginTop: '20px' }}>
              <a href="/en" style={{ color: '#3b82f6', textDecoration: 'underline' }}>
                Click here if not redirected automatically
              </a>
            </p>
          </div>
        </div>
      </body>
    </html>
  );
}
