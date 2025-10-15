import Header from '../components/Header'
import ModuleCard from '../components/ModuleCard'

export default function Page() {
  const modules = [
    'ui-ux','functional','api-testing','smoke','regression','chatbot'
  ]

  return (
    <main>
      <Header />
      <h1>Dashboard</h1>
      <div style={{display: 'flex', gap: 12}}>
        {modules.map(m => <ModuleCard key={m} title={m} />)}
      </div>
    </main>
  )
}
