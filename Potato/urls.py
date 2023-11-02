from django.urls import path
from . import views

app_name = 'Potato'
urlpatterns = [
    path("", views.index, name="index"),
    path("predict", views.predict, name="predict"),
    path("agribot",views.agribot, name="agribot"),
    # path("chatbot", views.chatbot, name="chatbot"),
    # path("chat", views.chat, name="chat"),
    # path("register", views.register, name="register"),
    # path("login", views.login_page, name="login"),
    # path("logout", views.logout_now, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    # path("myCode", views.SendEmail, name="myCode"),
    # path("update_password", views.UpdatePassword, name="update_password"),
]