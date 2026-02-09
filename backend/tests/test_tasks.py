"""
Task CRUD Tests

Tests for task creation, reading, updating, deleting, filtering, and sorting.
All endpoints are scoped to authenticated users.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_token, create_test_user


async def _create_task(
    client: AsyncClient,
    token: str,
    title: str = "Test Task",
    priority: str = "urgent_important",
    description: str | None = None,
    due_datetime: str | None = None,
) -> dict:
    """Helper to create a task and return the response data."""
    payload: dict = {"title": title, "priority": priority}
    if description is not None:
        payload["description"] = description
    if due_datetime is not None:
        payload["due_datetime"] = due_datetime
    response = await client.post(
        "/api/v1/tasks",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()["data"]


class TestCreateTask:
    """Tests for POST /api/v1/tasks."""

    @pytest.mark.asyncio
    async def test_create_task_valid(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Create task with valid data returns 201."""
        _, token = await create_test_user(db_session)

        response = await client.post(
            "/api/v1/tasks",
            json={
                "title": "My Task",
                "priority": "urgent_important",
                "description": "A test task",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "My Task"
        assert data["data"]["priority"] == "urgent_important"
        assert data["data"]["is_completed"] is False

    @pytest.mark.asyncio
    async def test_create_task_missing_title(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Create task without title returns 422."""
        _, token = await create_test_user(db_session)

        response = await client.post(
            "/api/v1/tasks",
            json={"priority": "urgent_important"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_invalid_priority(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Create task with invalid priority returns 422."""
        _, token = await create_test_user(db_session)

        response = await client.post(
            "/api/v1/tasks",
            json={"title": "Bad Priority", "priority": "invalid_value"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_without_auth(self, client: AsyncClient) -> None:
        """Create task without token returns 401."""
        response = await client.post(
            "/api/v1/tasks",
            json={"title": "No Auth", "priority": "urgent_important"},
        )
        assert response.status_code == 401


class TestListTasks:
    """Tests for GET /api/v1/tasks."""

    @pytest.mark.asyncio
    async def test_list_own_tasks(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """List tasks returns only authenticated user's tasks."""
        _, token1 = await create_test_user(db_session, email="user1@example.com")
        _, token2 = await create_test_user(db_session, email="user2@example.com")

        # Create tasks for both users
        await _create_task(client, token1, title="User1 Task")
        await _create_task(client, token2, title="User2 Task")

        # User1 should only see their task
        response = await client.get(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {token1}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total_count"] == 1
        assert data["data"]["tasks"][0]["title"] == "User1 Task"

    @pytest.mark.asyncio
    async def test_list_tasks_filter_priority(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Filter tasks by priority returns correct subset."""
        _, token = await create_test_user(db_session)

        await _create_task(client, token, title="Urgent", priority="urgent_important")
        await _create_task(client, token, title="Not Urgent", priority="not_urgent_not_important")

        response = await client.get(
            "/api/v1/tasks?priority=urgent_important",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Urgent"

    @pytest.mark.asyncio
    async def test_list_tasks_filter_completed(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Filter by is_completed returns correct subset."""
        _, token = await create_test_user(db_session)

        task_data = await _create_task(client, token, title="Complete Me")
        # Mark as completed
        await client.patch(
            f"/api/v1/tasks/{task_data['id']}",
            json={"is_completed": True},
            headers={"Authorization": f"Bearer {token}"},
        )
        await _create_task(client, token, title="Still Pending")

        response = await client.get(
            "/api/v1/tasks?is_completed=true",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Complete Me"

    @pytest.mark.asyncio
    async def test_list_tasks_sort_by_title(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Sort tasks by title ascending."""
        _, token = await create_test_user(db_session)

        await _create_task(client, token, title="Charlie")
        await _create_task(client, token, title="Alpha")
        await _create_task(client, token, title="Bravo")

        response = await client.get(
            "/api/v1/tasks?sort_by=title&sort_order=asc",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        titles = [t["title"] for t in tasks]
        assert titles == ["Alpha", "Bravo", "Charlie"]

    @pytest.mark.asyncio
    async def test_list_tasks_without_auth(self, client: AsyncClient) -> None:
        """List tasks without token returns 401."""
        response = await client.get("/api/v1/tasks")
        assert response.status_code == 401


class TestGetTask:
    """Tests for GET /api/v1/tasks/{task_id}."""

    @pytest.mark.asyncio
    async def test_get_own_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Get task by ID returns task owned by user."""
        _, token = await create_test_user(db_session)
        task_data = await _create_task(client, token, title="Fetch Me")

        response = await client.get(
            f"/api/v1/tasks/{task_data['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Fetch Me"

    @pytest.mark.asyncio
    async def test_get_other_users_task_returns_404(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Get another user's task returns 404."""
        _, token1 = await create_test_user(db_session, email="owner@example.com")
        _, token2 = await create_test_user(db_session, email="other@example.com")

        task_data = await _create_task(client, token1, title="Private Task")

        response = await client.get(
            f"/api/v1/tasks/{task_data['id']}",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_nonexistent_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Get nonexistent task returns 404."""
        _, token = await create_test_user(db_session)

        response = await client.get(
            "/api/v1/tasks/nonexistent-id",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


class TestUpdateTask:
    """Tests for PATCH /api/v1/tasks/{task_id}."""

    @pytest.mark.asyncio
    async def test_update_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Update task fields returns updated task."""
        _, token = await create_test_user(db_session)
        task_data = await _create_task(client, token, title="Old Title")

        response = await client.patch(
            f"/api/v1/tasks/{task_data['id']}",
            json={"title": "New Title", "is_completed": True},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        updated = response.json()["data"]
        assert updated["title"] == "New Title"
        assert updated["is_completed"] is True

    @pytest.mark.asyncio
    async def test_update_other_users_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Update another user's task returns 404."""
        _, token1 = await create_test_user(db_session, email="owner2@example.com")
        _, token2 = await create_test_user(db_session, email="other2@example.com")

        task_data = await _create_task(client, token1, title="Not Yours")

        response = await client.patch(
            f"/api/v1/tasks/{task_data['id']}",
            json={"title": "Hijacked"},
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /api/v1/tasks/{task_id}."""

    @pytest.mark.asyncio
    async def test_delete_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Delete task returns success and task is gone."""
        _, token = await create_test_user(db_session)
        task_data = await _create_task(client, token, title="Delete Me")

        # Delete
        response = await client.delete(
            f"/api/v1/tasks/{task_data['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

        # Verify gone
        response = await client.get(
            f"/api/v1/tasks/{task_data['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_without_auth(self, client: AsyncClient) -> None:
        """Delete task without token returns 401."""
        response = await client.delete("/api/v1/tasks/some-id")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_other_users_task(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Delete another user's task returns 404."""
        _, token1 = await create_test_user(db_session, email="owner3@example.com")
        _, token2 = await create_test_user(db_session, email="other3@example.com")

        task_data = await _create_task(client, token1, title="Protected")

        response = await client.delete(
            f"/api/v1/tasks/{task_data['id']}",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert response.status_code == 404
