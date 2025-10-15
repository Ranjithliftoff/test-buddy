"use client";

import { useEffect, useState } from "react";

export default function FunctionalPanel() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE;
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  const [mode, setMode] = useState("web");
  const [url, setUrl] = useState("");
  const [plan, setPlan] = useState(null);
  const [posting, setPosting] = useState(false);

  async function loadTests() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/functional/test`, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function submitPlan(e) {
    e.preventDefault();
    setPosting(true);
    setPlan(null);
    try {
      const res = await fetch(`${API_BASE}/functional/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, url })
      });
      const json = await res.json();
      setPlan(json);
    } catch (e) {
      alert("Failed to request plan: " + e);
    } finally {
      setPosting(false);
    }
  }

  useEffect(() => { loadTests(); }, []);

  return (
    <div style={{ display: "grid", gap: 16 }}>
      {/* Section: Sample run from BE */}
      <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ margin: 0 }}>Latest sample results (from API)</h2>
          <button onClick={loadTests} style={{ padding: "6px 10px" }}>Refresh</button>
        </div>

        {loading && <p style={{ marginTop: 8 }}>Loading…</p>}
        {error && <p style={{ color: "red" }}>Error: {error}</p>}
        {data && (
          <>
            <p style={{ marginTop: 8 }}>
              <strong>Summary:</strong> {data.summary.passed} passed / {data.summary.failed} failed (total {data.summary.total})
            </p>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={th}>ID</th>
                  <th style={th}>Name</th>
                  <th style={th}>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.tests.map((t) => (
                  <tr key={t.id}>
                    <td style={td}>{t.id}</td>
                    <td style={td}>{t.name}</td>
                    <td style={{ ...td, color: t.status === "passed" ? "green" : "red" }}>
                      {t.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </section>

      {/* Section: Draft a plan from intake */}
      <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Draft plan from intake</h2>
        <form onSubmit={submitPlan} style={{ display: "grid", gap: 12, maxWidth: 600 }}>
          <label>
            <div style={{ fontSize: 14 }}>Mode</div>
            <select value={mode} onChange={(e) => setMode(e.target.value)} style={input}>
              <option value="web">web</option>
              <option value="figma">figma</option>
              <option value="doc">doc</option>
              <option value="sheet">sheet</option>
            </select>
          </label>

          <label>
            <div style={{ fontSize: 14 }}>URL (optional)</div>
            <input
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={input}
            />
          </label>

          <div>
            <button type="submit" disabled={posting} style={{ padding: "8px 14px" }}>
              {posting ? "Requesting…" : "Generate Draft Plan"}
            </button>
          </div>
        </form>

        {plan && (
          <div style={{ marginTop: 16 }}>
            <h3 style={{ margin: 0 }}>{plan.plan?.title || "Plan"}</h3>
            <ul>
              {(plan.plan?.bullets || []).map((b, i) => (
                <li key={i}>{b}</li>
              ))}
            </ul>
            <div style={{ fontSize: 12, color: "#6b7280" }}>
              Intake: mode=<code>{plan.intake?.mode}</code> url={<code>{plan.intake?.url || "—"}</code>}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

const th = { textAlign: "left", padding: "8px", borderBottom: "1px solid #e5e7eb" };
const td = { padding: "8px", borderBottom: "1px solid #f3f4f6" };
const input = { width: "100%", border: "1px solid #d1d5db", borderRadius: 6, padding: "8px 10px" };
