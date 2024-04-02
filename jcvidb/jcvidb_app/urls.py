from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('categories/<int:id>', views.category_list_view, name='category_list_view'),
    path('details/<int:id>', views.details, name='details'),
    path('update/<int:id>', views.update_posted_data, name='update_posted_data'),
    path('search/', views.search, name='search'),
    path('registration/', views.create_User, name='registration'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('post_data/', views.prot_post, name='post'),
    path('approve_post/', views.appprove_post, name='approve_post'),
    path('approve_data/<int:id>',views.approve_data, name='update_prot'),
    path('file_upload/<int:context_id>', views.file_upload, name='file_upload'),
    path('download/<str:file_name>/', views.download_file, name='download_file'),
    path('preview_csv/', views.preview_csv, name='preview_csv'),
    path('profile/', views.profile_view, name='profile_view'),
    path('delete_data/<int:id>', views.delete_data, name='delete_data'),
    path('file_update/<int:context_id>', views.file_update, name='file_update'),
]