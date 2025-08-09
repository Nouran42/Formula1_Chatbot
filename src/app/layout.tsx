// src/app/layout.tsx
import './globals.css'  // optional, your global styles

export const metadata = {
  title: 'F1 GPT Chatbot',
  description: 'Formula 1 chatbot powered by GPT',
};


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", backgroundColor: '#0a0a0a', color: '#fff' }}>
        {children}
      </body>
    </html>
  );
}