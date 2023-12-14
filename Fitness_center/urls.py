from Fitness_center import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Fitness_center.views import register_user

urlpatterns = [
    path('Client/', views.ClientList.as_view(), name='client-list'),
    path('Client/<int:pk>/', views.ClientDetail.as_view(), name='client-detail'),
    path('TrainingType/', views.TrainingTypeList.as_view(), name='trainingtype-list'),
    path('TrainingType/<int:pk>/', views.TrainingTypeDetail.as_view(), name='trainingtype-detail'),
    path('Subscription/', views.SubscriptionList.as_view(), name='subscription-list'),
    path('Subscription/<int:pk>/', views.SubscriptionDetail.as_view(), name='subscription-detail'),
    path('drf-auth/', include('rest_framework.urls', namespace='drf-auth')),
    path('register/', register_user, name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

