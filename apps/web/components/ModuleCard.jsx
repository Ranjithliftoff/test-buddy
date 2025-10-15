export default function ModuleCard({title}){
  return (<div style={{border: '1px solid #ccc', padding: 8, width: 160}}>
    <h3 style={{textTransform: 'capitalize'}}>{title}</h3>
    <p>Quick actions and status</p>
  </div>)
}
