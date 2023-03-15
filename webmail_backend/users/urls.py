from django.urls import path,include
from .views import RegisterView,LoginView,UserView,LogoutView,MailViewApi,MailUpdateView,StarredView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('mails',MailViewApi.as_view()),
    path('mails/<int:pk>',MailUpdateView.as_view()),
    path('starred',StarredView.as_view())
]