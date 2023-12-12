from Fitness_center import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from Fitness_center.views import register_user

urlpatterns = [
    path('task/', views.ClientList.as_view()),
    path('task/<int:pk>/', views.ClientDetail.as_view()),
    path('category/', views.TrainingTypeList.as_view()),
    path('category/<int:pk>/', views.TrainingTypeDetail.as_view()),
    path('category/', views.SubscriptionList.as_view()),
    path('category/<int:pk>/', views.SubscriptionDetail.as_view()),
    path('drf-auth/', include('rest_framework.urls')),
    path('register/', register_user, name='register_user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

