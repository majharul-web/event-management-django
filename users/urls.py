from django.urls import path
from users.views import sign_up, sign_in, sign_out,activate_account, admin_dashboard,assign_role,create_group,group_list,user_list, ProfileView,EditProfileView

# users app url
urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_account, name='activate-account'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/user-list/', user_list, name='user-list'),
    path('admin/assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]