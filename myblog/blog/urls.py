from .views import (PostList,PostDetail,search,
                    login,register,createpost,
                    update_post,DeletePostView)
from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('search/',search, name = 'search'),
    path('accounts/login/',login,name ='login'),
    path('accounts/signup/', register,name ='register'),
    path('make/post/',createpost,name = 'create_post'),
    path('update/<slug:slug>/',update_post,name='update_post'),
    path('delete/<int:pk>/post/',DeletePostView.as_view(), name='delete'),


]