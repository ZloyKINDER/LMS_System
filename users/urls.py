from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListView, SubscriptionViewSet, PaymentCreateView, PaymentStatusView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/status/', PaymentStatusView.as_view(), name='payment-status'),
]