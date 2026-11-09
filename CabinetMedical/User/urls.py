from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('login/',auth_view.LoginView.as_view(
        template_name="User/login.html",
        redirect_authenticated_user=True,),
         name="log"),
    path('logout/',auth_view.LogoutView.as_view(),
         name="logout"),
    path('Accueil/',views.Accueil,name="Accueil")
    #  path('SignUp/',views.SignUp,
    #           name="Register")
]
