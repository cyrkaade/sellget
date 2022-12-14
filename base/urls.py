from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create-room/', views.createRoom, name="create-room"),
    path('room/buy/<str:pk>/', views.buying, name='buy'),
    path('update/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('register/', views.registerPage, name="register"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('script/', views.script, name='script')
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)