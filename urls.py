from django.urls import path
import chatIntegration.views as views
urlpatterns = [
    path('', views.welcome),
    path('list', views.index),
    path('update/<field>/<chat_id>/<update>', views.update),
    path('delete/<chat_id>', views.delete),
    path('show/<chat_id>' , views.show)
]