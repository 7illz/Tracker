import type { TaskSummary as Summary } from '../types/task'

export function TaskSummary({ summary }: { summary: Summary }) {
  const cards = [['To do', summary.todo, 'blue'], ['In progress', summary.in_progress, 'amber'], ['Done', summary.done, 'green'], ['Overdue', summary.overdue, 'red']]
  return <section className="summary-grid">{cards.map(([label, count, color]) => <article className={`summary-card ${color}`} key={String(label)}><span>{label}</span><strong>{count}</strong></article>)}</section>
}
