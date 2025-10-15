export default function ModuleCard({ title }) {
  const href = `/${title}`;
  return (
    <a href={href} style={{
      display: "block",
      border: "1px solid #e5e7eb",
      borderRadius: 8,
      padding: 16,
      width: 220,
      textDecoration: "none",
      color: "inherit"
    }}>
      <div style={{ fontSize: 20, fontWeight: 600, textTransform: "capitalize" }}>{title.replace("-", " ")}</div>
      <div style={{ marginTop: 8, color: "#374151" }}>Quick actions and status</div>
    </a>
  );
}
