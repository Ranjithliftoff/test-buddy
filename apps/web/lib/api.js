const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export async function fetchJSON(path, opts={}){
  const res = await fetch(base + path, opts)
  if(!res.ok) throw new Error('API error: ' + res.status)
  return res.json()
}
