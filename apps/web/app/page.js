"use client";

import Header from "../components/Header";
import ModuleCard from "../components/ModuleCard";
import { useEffect, useState } from "react";

export default function Page() {
  const modules = ["ui-ux", "functional", "api-testing", "smoke", "regression", "chatbot"];
  const [status, setStatus] = useState("checking");
  const base = process.env.NEXT_PUBLIC_API_BASE;

  // Check backend connection
  async function checkHealth() {
    try {
      const res = await fetch(`${base}/health`, { cache: "no-store" });
      const json = await res.json().catch(() => ({}));
      if (res.ok && (json.ok === true || json.status === "ok")) setStatus("ok");
      else setStatus("down");
    } catch {
      setStatus("down");
    }
  }

  useEffect(() => {
    checkHealth();
    const id = setInterval(checkHealth, 10000); // re-check every 10 seconds
    return () => clearInterval(id);
  }, []);

  const color =
    status === "ok" ? "green" : status === "down" ? "red" : "gray";
  const text =
    status === "ok"
      ? "Backend: OK"
      : status === "down"
      ? "Backend: DOWN"
      : "Checking...";

  return (
    <main style={{ padding: 20 }}>
      <Header />
      <h1>Dashboard</h1>

      {/* Backend status indicator */}
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          border: "1px solid #ddd",
          borderRadius: 20,
          padding: "6px 12px",
          fontSize: 14,
          marginBottom: 16,
        }}
      >
        <span
          style={{
            display: "inline-block",
            width: 10,
            height: 10,
            borderRadius: "50%",
            backgroundColor: color,
          }}
        ></span>
        <span>{text}</span>
        <span style={{ color: "#888", marginLeft: 4 }}>({base})</span>
      </div>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {modules.map((m) => (
          <ModuleCard key={m} title={m} />
        ))}
      </div>
    </main>
  );
}
