"use client";

import { useState } from "react";

export default function UIUXPanel() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE;
  const [source, setSource] = useState("web");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");

  // simple accept/reject tracking for issues
  const [decisions, setDecisions] = useState({}); // {issueId: "accepted"|"rejected"}

  async function analyze(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRes(null);
    try {
      const r = await fetch(`${API_BASE}/uiux/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, url }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      setRes(j);
      setDecisions({});
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  function setDecision(id, val) {
    setDecisions((d) => ({ ...d, [id]: val }));
  }

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <section style={card}>
        <h2 style={{ marginTop: 0 }}>Intake</h2>
        <form onSubmit={analyze} style={{ display: "grid", gap: 12, maxWidth: 640 }}>
          <label>
            <div style={label}>Source</div>
            <select value={source} onChange={(e) => setSource(e.target.value)} style={input}>
              <option value="web">Website URL</option>
              <option value="figma">Figma URL</option>
            </select>
          </label>
          <label>
            <div style={label}>URL</div>
            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder={source === "figma" ? "https://www.figma.com/file/..." : "https://example.com"}
              style={input}
              type="url"
              required
            />
          </label>
          <div>
            <button type="submit" disabled={loading} style={btn}>
              {loading ? "Analyzing…" : "Analyze"}
            </button>
          </div>
        </form>
        {error && <p style={{ color: "red", marginTop: 8 }}>Error: {error}</p>}
      </section>

      {res && (
        <>
          <section style={card}>
            <h2 style={{ marginTop: 0 }}>Summary</h2>
            <p>
              <strong>Target:</strong> {res.target} ({res.source}) •{" "}
              <strong>Components:</strong> {res.summary.components_found} •{" "}
              <strong>Issues:</strong> {res.summary.issues_found}
            </p>
          </section>

          <section style={card}>
            <h2 style={{ marginTop: 0 }}>Components</h2>
            <table style={table}>
              <thead>
                <tr>
                  <th style={th}>Name</th>
                  <th style={th}>Type</th>
                  <th style={th}>Notes</th>
                </tr>
              </thead>
              <tbody>
                {res.components.map((c, idx) => (
                  <tr key={idx}>
                    <td style={td}>{c.name}</td>
                    <td style={td}>{c.type}</td>
                    <td style={td}>{c.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section style={card}>
            <h2 style={{ marginTop: 0 }}>Heuristic Issues</h2>
            <table style={table}>
              <thead>
                <tr>
                  <th style={th}>Severity</th>
                  <th style={th}>Title</th>
                  <th style={th}>Suggestion</th>
                  <th style={th}>Decision</th>
                </tr>
              </thead>
              <tbody>
                {res.issues.map((i) => (
                  <tr key={i.id}>
                    <td style={{ ...td, textTransform: "capitalize" }}>{i.severity}</td>
                    <td style={td}>{i.title}</td>
                    <td style={td}>{i.suggestion}</td>
                    <td style={td}>
                      <div style={{ display: "flex", gap: 8 }}>
                        <button
                          type="button"
                          onClick={() => setDecision(i.id, "accepted")}
                          style={{
                            ...chip,
                            background: decisions[i.id] === "accepted" ? "#16a34a" : "#e5e7eb",
                            color: decisions[i.id] === "accepted" ? "white" : "black",
                          }}
                        >
                          Accept
                        </button>
                        <button
                          type="button"
                          onClick={() => setDecision(i.id, "rejected")}
                          style={{
                            ...chip,
                            background: decisions[i.id] === "rejected" ? "#dc2626" : "#e5e7eb",
                            color: decisions[i.id] === "rejected" ? "white" : "black",
                          }}
                        >
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div style={{ marginTop: 12, fontSize: 13, color: "#6b7280" }}>
              Decisions: {Object.keys(decisions).length ? JSON.stringify(decisions) : "—"}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

const card = { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16 };
const label = { fontSize: 14, marginBottom: 4 };
const input = { width: "100%", border: "1px solid #d1d5db", borderRadius: 6, padding: "8px 10px" };
const btn = { padding: "8px 14px" };
const table = { width: "100%", borderCollapse: "collapse" };
const th = { textAlign: "left", padding: 8, borderBottom: "1px solid #e5e7eb" };
const td = { padding: 8, borderBottom: "1px solid #f3f4f6", verticalAlign: "top" };
const chip = { padding: "6px 10px", borderRadius: 999, border: "1px solid #d1d5db" };
