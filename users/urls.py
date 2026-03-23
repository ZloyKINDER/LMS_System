from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListView, SubscriptionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # Изменено с r'' на r'users'
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]