import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("priority", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="medium", max_length=10)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed")], default="pending", max_length=15)),
                ("due_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["due_date", "-created_at"]},
        ),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["user", "status"], name="tasks_task_user_id_c0fce1_idx")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["user", "due_date"], name="tasks_task_user_id_075050_idx")),
    ]
