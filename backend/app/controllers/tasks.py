from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.task import Task
from app.models.user import User
from app.views.task import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskSummary, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


def get_owned_task(task_id: int, db: Session, user_id: int) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Task:
    task = Task(**payload.model_dump(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskResponse])
def list_tasks(status_filter: TaskStatus | None = Query(default=None, alias="status"), priority: TaskPriority | None = None, search: str | None = Query(default=None, min_length=1, max_length=200), skip: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100), sort_by: Literal["created_at", "due_date"] = "created_at", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Task]:
    query = select(Task).where(Task.user_id == current_user.id)
    if status_filter: query = query.where(Task.status == status_filter)
    if priority: query = query.where(Task.priority == priority)
    if search: query = query.where(Task.title.ilike(f"%{search}%"))
    order_column = Task.created_at if sort_by == "created_at" else Task.due_date
    return list(db.scalars(query.order_by(order_column.desc()).offset(skip).limit(limit)))


@router.get("/summary", response_model=TaskSummary)
def task_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> TaskSummary:
    counts = dict(db.execute(select(Task.status, func.count(Task.id)).where(Task.user_id == current_user.id).group_by(Task.status)).all())
    overdue = db.scalar(select(func.count(Task.id)).where(Task.user_id == current_user.id, Task.due_date < datetime.now(UTC), Task.status != TaskStatus.DONE)) or 0
    return TaskSummary(todo=counts.get("todo", 0), in_progress=counts.get("in_progress", 0), done=counts.get("done", 0), overdue=overdue)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Task:
    return get_owned_task(task_id, db, current_user.id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Task:
    task = get_owned_task(task_id, db, current_user.id)
    for field, value in payload.model_dump(exclude_unset=True).items(): setattr(task, field, value)
    db.commit(); db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Response:
    db.delete(get_owned_task(task_id, db, current_user.id)); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
