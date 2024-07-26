from uuid import uuid4
from httpx import ASGITransport, AsyncClient
import pytest
from main import app, tasks, Task


# This decorator is used to mark the test function as an asynchronous test function. It tells pytest to run the function in an event loop.
@pytest.mark.asyncio
async def test_create_task():
    task_id = str(uuid4())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/create_task/", json={"id": task_id,"title": "New Task", "description": "A new task description"})
    # assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_json = response.json()
    assert response_json["title"] == "New Task", f"Expected title to be 'New Task', but got '{response_json['title']}'"
    assert response_json["description"] == "A new task description", f"Expected description to be 'A new task description', but got {response_json['description']}"


@pytest.mark.asyncio
async def test_task_detail():
    task_id = str(uuid4())
    new_task = Task(id=task_id, title="Sample Task", description="Sample Description")
    tasks.append(new_task)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f'/task_detail/{task_id}/')
    assert response.json()['id'] == task_id, f"Expected task ID to be {task_id}, but got {response.json()['id']}"

@pytest.mark.asyncio
async def test_update_task():
    task_id = str(uuid4())
    new_task = Task(id=task_id, title="Sample Task", description="Sample Description")
    tasks.append(new_task)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put(f"/update_task/{task_id}/", json={"id": task_id, "title": "Updated Task", "description": "Updated description"})
    response_json = response.json()
    assert response_json["title"] == "Updated Task", f"Expected title to be 'Updated Task', but got {response_json['title']}. Response: {response_json}"
    assert response_json["description"] == "Updated description", f"Expected description to be 'Updated description', but got {response_json['description']}. Response: {response_json}"


@pytest.mark.asyncio
async def test_delete_task():
    task_id = str(uuid4())
    new_task = Task(id=task_id, title="Sample Task", description="Sample Description")
    tasks.append(new_task)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(f"/delete_task/{task_id}/")
    assert response.json()["message"] == "Task deleted successfully", f"Expected message to be 'Task deleted successfully', but got {response.json()['message']}. Response: {response.json()}"

@pytest.mark.asyncio
async def test_filter_tasks():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/fetch_tasks/?status=approved")
    # assert all(task["status"] == "pending" for task in response.json()), f"Expected all tasks to have status 'pending'."
    assert all(task["status"] == "approved" for task in response.json()), f"Expected all tasks to have status 'approved'"

