import "../styles/globals.css";

export const metadata = { title: "TestBuddy", description: "Agentic AI-Powered Testing Platform" };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
