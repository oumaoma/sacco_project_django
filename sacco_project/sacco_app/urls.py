from django.urls import path
from .views import DepositView, WithdrawView, StatementView, dashboard, login_view, logout_view

urlpatterns = [
    path('deposit/<int:farmer_id>/<int:amount>/', DepositView.as_view(), name='deposit'),
    path('withdraw/<int:farmer_id>/<int:amount>/', WithdrawView.as_view(), name='withdraw'),
    path('statement/<int:farmer_id>/<int:N>/', StatementView.as_view(), name='statement'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
