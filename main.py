from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI()


class Task(BaseModel):
    id: UUID
    title: str
    description: str
    status: str = "pending"

tasks = []

@app.post('/create_task/', response_model= Task)
async def createTask(task:Task):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get('/task_detail/{task_id}/', response_model= Task)
async def getTaskDetail(task_id:UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found!')

@app.put('/update_task/{task_id}/', response_model= Task)
async def updateTask(task_id: UUID, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found!")

@app.delete('/delete_task/{task_id}/')
async def deleteTask(task_id: UUID):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found!")

@app.get('/fetch_tasks/', response_model= List[Task])
async def fetchTasks(status: Optional[str] = Query(None)):
    if status:
        return [task for task in tasks if task.status == status]
    return tasks


