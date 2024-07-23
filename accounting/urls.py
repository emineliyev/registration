from django.urls import path
from .views import (
    user_login, logout_view, profile_update, ContractListView, UploadContractView, DeleteContractView, change_password
)


app_name = 'accounting'

urlpatterns = [
    path('', user_login, name='login'),
    path('logout_view/', logout_view, name='logout_view'),
    path('profile/', profile_update, name='profile_update'),
    path('change-password/', change_password, name='change_password'),
    path('contract_list/', ContractListView.as_view(), name='contract_list'),
    path('upload_contract/', UploadContractView.as_view(), name='upload_contract'),
    path('delete_confirm_contract/<int:pk>/', DeleteContractView.as_view(), name='delete_confirm_contract'),
]

handler404 = 'accounting.views.page_not_found'