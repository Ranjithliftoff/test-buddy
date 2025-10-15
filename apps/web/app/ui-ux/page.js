"use client";

import UIUXPanel from "../../components/UIUXPanel";

export default function UIUXPage() {
  return (
    <main style={{ padding: 20, maxWidth: 1000, margin: "0 auto" }}>
      <a href="/" style={{ fontSize: 14, color: "#2563eb" }}>← Back to Dashboard</a>
      <h1 style={{ marginTop: 12 }}>UI/UX — Quick actions</h1>
      <UIUXPanel />
    </main>
  );
}
