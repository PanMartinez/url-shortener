from django.urls import path

from shortener import views

app_name = "shortener"

urlpatterns = [
    path("shrt/", views.ShortURLCreateView.as_view(), name="create"),
    path("shrt/<str:code>/", views.ShortURLExpandView.as_view(), name="expand"),
]
