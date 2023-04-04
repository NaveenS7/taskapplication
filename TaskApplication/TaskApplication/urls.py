"""TaskApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todos import views
from api import views as api_view
from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken

from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("api/users",api_view.UsersView,basename="users")
router.register("api/tasks",api_view.TaskView,basename="tasks")
router.register("api/todos",api_view.TaskdetailsView,basename="todos")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("tasks/add",views.TaskCreateView.as_view(),name="task-add"),
    path("",views.IndexView.as_view(),name="home"),
    path("tasks/all",views.TaskListView.as_view(),name="task-list"),
    path("tasks/<int:pk>",views.TaskDetailView.as_view(),name="task-detail"),
    path("tasks/remove/<int:pk>",views.TaskDeleteView.as_view(),name="task-delete"),
    path("tasks/change/<int:pk>",views.TaskEditView.as_view(),name="task-edit"),
    path("register/",views.RegistrationView.as_view(),name="register"),
    path("signin",views.SignInView.as_view(),name="signin"),
    path("signout",views.SignOutView.as_view(),name="signout"),
    path("task/home",views.TaskHome.as_view(),name="task-home"),
    path("api/token/",ObtainAuthToken.as_view())


]+router.urls
