from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Task


@override_settings(SECURE_SSL_REDIRECT=False)
class TaskFlowTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="long-test-pass-123")
        self.bob = User.objects.create_user(username="bob", password="long-test-pass-123")
        self.task = Task.objects.create(user=self.alice, title="Alice task", due_date=timezone.localdate() + timedelta(days=2))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(reverse("register"), {"username": "new", "email": "new@example.com", "password1": "Safe-pass-987654", "password2": "Safe-pass-987654"})
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="new").exists())

    def test_task_crud_is_scoped_to_owner(self):
        self.client.force_login(self.bob)
        self.assertEqual(self.client.get(reverse("task_detail", args=[self.task.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("task_update", args=[self.task.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("task_delete", args=[self.task.pk])).status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_owner_can_create_update_complete_and_delete(self):
        self.client.force_login(self.alice)
        data = {"title": "New task", "description": "Details", "priority": "high", "status": "pending", "due_date": (timezone.localdate() + timedelta(days=3)).isoformat()}
        response = self.client.post(reverse("task_create"), data)
        task = Task.objects.get(title="New task", user=self.alice)
        self.assertRedirects(response, reverse("task_detail", args=[task.pk]))
        data["title"] = "Updated task"
        self.client.post(reverse("task_update", args=[task.pk]), data)
        self.client.post(reverse("task_complete", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated task")
        self.assertEqual(task.status, Task.Status.COMPLETED)
        self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_dashboard_counts_only_users_tasks_and_overdue_logic(self):
        Task.objects.create(user=self.alice, title="Late", due_date=timezone.localdate() - timedelta(days=1))
        Task.objects.create(user=self.bob, title="Other user's", due_date=timezone.localdate() - timedelta(days=4))
        self.client.force_login(self.alice)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.context["stats"]["total"], 2)
        self.assertEqual(response.context["stats"]["overdue"], 1)
