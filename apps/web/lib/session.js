export function saveSession(session){
  if(typeof window === 'undefined') return
  localStorage.setItem('tb_session', JSON.stringify(session))
}

export function loadSession(){
  if(typeof window === 'undefined') return null
  try{ return JSON.parse(localStorage.getItem('tb_session')) }catch{ return null }
}
