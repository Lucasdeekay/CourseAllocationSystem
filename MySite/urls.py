from django.urls import path

from MySite import views
from MySite.views import HomeView, LoginView, RegisterView, DashboardView, DashboardAdminView

app_name = "MySite"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("logout", views.log_out, name="logout"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("dashboard/admin", DashboardAdminView.as_view(), name="dash_admin"),
    path("dashboard/admin/choose_lecturer", views.choose_lecturer, name="choose_lecturer"),
    path("dashboard/admin/allocate-<int:course_id>-<str:staff_id>", views.allocate, name="allocate"),
    path("dashboard/admin/deallocate-<int:course_id>-<str:staff_id>", views.deallocate, name="deallocate"),
]
