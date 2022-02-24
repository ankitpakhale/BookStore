from django.urls import path
from .views import index, register, login, logout,profile_edit,catwisebook,authorwise,  forgot, Confirm
urlpatterns = [
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    
    path('forgot/', forgot, name='FORGOT'),

    path('conf/',Confirm,name='conf'),
    
    path('logout/', logout,name='logout'),
    path('catwise/<str:cat_name>/',catwisebook,name='catwise'),
    path('authwise/<str:name>/',authorwise,name='authwise'),
    path('profile_edit/',profile_edit,name='profile_edit'),
]
