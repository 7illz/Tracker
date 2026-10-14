import type { Task } from '../types/task'

interface Props { tasks: Task[]; onEdit: (task: Task) => void; onDelete: (task: Task) => void }
const label = (value: string) => value.replace('_', ' ')

export function TaskList({ tasks, onEdit, onDelete }: Props) {
  if (!tasks.length) return <div className="empty"><h2>No tasks found</h2><p>Create a task or adjust your filters.</p></div>
  return <div className="task-list">{tasks.map(task => <article className="task-card" key={task.id}><div className="task-main"><div className="task-title"><h3>{task.title}</h3><span className={`badge ${task.status}`}>{label(task.status)}</span></div>{task.description && <p>{task.description}</p>}<div className="task-meta"><span className={`priority ${task.priority}`}>{task.priority}</span>{task.due_date && <span>Due {new Date(task.due_date).toLocaleString()}</span>}</div></div><div className="task-actions"><button className="secondary" onClick={() => onEdit(task)}>Edit</button><button className="danger" onClick={() => onDelete(task)}>Delete</button></div></article>)}</div>
}
