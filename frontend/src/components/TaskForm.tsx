import { useEffect, useState } from 'react'
import type { Task, TaskPayload } from '../types/task'

interface Props { task?: Task | null; onSave: (payload: TaskPayload) => Promise<void>; onCancel: () => void }
const empty: TaskPayload = { title: '', description: '', status: 'todo', priority: 'medium', due_date: null }

export function TaskForm({ task, onSave, onCancel }: Props) {
  const [form, setForm] = useState<TaskPayload>(empty)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  useEffect(() => setForm(task ? { title: task.title, description: task.description ?? '', status: task.status, priority: task.priority, due_date: task.due_date ? task.due_date.slice(0, 16) : null } : empty), [task])
  const submit = async (event: React.FormEvent) => { event.preventDefault(); setSaving(true); setError(''); try { await onSave({ ...form, description: form.description || null, due_date: form.due_date ? new Date(form.due_date).toISOString() : null }); } catch (err) { setError(err instanceof Error ? err.message : 'Could not save task.') } finally { setSaving(false) } }
  return <form className="task-form" onSubmit={submit}><div className="form-heading"><h2>{task ? 'Edit task' : 'New task'}</h2><button type="button" className="icon-button" onClick={onCancel} aria-label="Close form">×</button></div>{error && <p className="error">{error}</p>}<label>Title<input required maxLength={200} value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} placeholder="What needs doing?" /></label><label>Description<textarea value={form.description ?? ''} onChange={e => setForm({ ...form, description: e.target.value })} rows={3} /></label><div className="form-row"><label>Status<select value={form.status} onChange={e => setForm({ ...form, status: e.target.value as TaskPayload['status'] })}><option value="todo">To do</option><option value="in_progress">In progress</option><option value="done">Done</option></select></label><label>Priority<select value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value as TaskPayload['priority'] })}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></label></div><label>Due date<input type="datetime-local" value={form.due_date ?? ''} onChange={e => setForm({ ...form, due_date: e.target.value || null })} /></label><div className="form-actions"><button type="button" className="secondary" onClick={onCancel}>Cancel</button><button disabled={saving}>{saving ? 'Saving…' : task ? 'Save changes' : 'Create task'}</button></div></form>
}
