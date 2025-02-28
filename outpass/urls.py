from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('signin/', views.sign_in, name="signin"),
    path('logout/',views.logout_view,name='logout'),
    path('apply/',views.apply_view,name="apply"),
    path("faculty_dashboard/", views.faculty_dashboard, name="faculty"),
    path("approve_outpass/<int:outpass_id>/", views.approve_outpass, name="approve_outpass"),
    path("reject_outpass/<int:outpass_id>/", views.reject_outpass, name="reject_outpass"),
]
