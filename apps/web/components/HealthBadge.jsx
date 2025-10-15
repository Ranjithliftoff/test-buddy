"use client";
import { useEffect, useState } from "react";

export default function HealthBadge() {
  const [status, setStatus] = useState("checking");
  const base = process.env.NEXT_PUBLIC_API_BASE;

  async function check() {
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
    check();
    const id = setInterval(check, 10000); // re-check every 10s
    return () => clearInterval(id);
  }, []);

  const color =
    status === "ok" ? "bg-green-500" : status === "down" ? "bg-red-500" : "bg-gray-400";
  const text =
    status === "ok" ? "Backend: OK" : status === "down" ? "Backend: DOWN" : "Checking…";

  return (
    <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
      <span className={`inline-block h-2.5 w-2.5 rounded-full ${color}`} />
      <span className="font-medium">{text}</span>
      <span className="text-gray-500">({base})</span>
    </div>
  );
}
