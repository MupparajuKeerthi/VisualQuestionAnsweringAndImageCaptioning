"""
URL configuration for visualQuestionAnsweringProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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


from django.conf.urls.static import static
from django.conf import settings


from userapp import views as user_views
from adminapp import views as admin_views




urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_views.index,name="index"),
    path("about/", user_views.about,name="about"),
    path("user-login/", user_views.user_login,name="user_login"),
    path("user-register/", user_views.user_register,name="user_register"),
    path("user-otp/",user_views.user_otp,name="user_otp"),
    path("admin-login/", user_views.admin_login,name="admin_login"),
    path("contact/", user_views.contact,name="contact"),
    path('user-dashboard/',user_views.user_dashboard,name="user_dashboard"),
    path('user-detection/',user_views.user_detection,name="user_detection"),
    path('user-feedback/',user_views.user_feedback,name="user_feedback"),
    path('user-profile/',user_views.user_profile,name="user_profile"),
    path("user/logout/",user_views.user_logout,name="user_logout"),
    path('user/upload', user_views.image_upload, name='image_upload'),
    path('user/search', user_views.image_search, name='image_search'),
    path("results/",user_views.user_result,name="user_result"),
    path("user-results/resultss/",user_views.result_result,name="result_result"),
    path("caption/",user_views.user_caption,name="user_caption"),

    path('admin-dashboard/', admin_views.index, name='admin_dashboard'),
    path('user/change-status/<int:user_id>/', admin_views.change_status, name='change_status'),
    path('all-users/', admin_views.all_users, name='all_users'),
    path('upload-dataset/', admin_views.upload_dataset, name='upload_dataset'),
    path('Train-Test-model/', admin_views.trainTestmodel, name='trainTestmodel'),
    path('MB-model/', admin_views.nb, name='mb'),
    path('Graph-analysis/', admin_views.graph, name='graph'),
    path('pending-users/', admin_views.pending_users, name='pending_users'),
    path('accept-user/<int:user_id>/', admin_views.accept_user, name='accept_user'),
    path('reject-user/<int:user_id>/', admin_views.reject_user, name='reject_user'),
    path('delete-user/<int:user_id>/', admin_views.delete_user, name='delete_user'),
    path('view-feedbacks/', admin_views.view_feedbacks, name='view_feedbacks'),
    path('remove-feedback/<int:feedback_id>/', admin_views.remove_feedback, name='remove_feedback'),
    path('feedback-graph/',admin_views.feedbacks_graph,name="feedback_graph"),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
