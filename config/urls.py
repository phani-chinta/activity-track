from django.contrib import admin
from django.urls import include, path
from tasks.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("accounts/", include("accounts.urls")),
    path("", include("tasks.urls")),
]
