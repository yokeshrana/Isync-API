from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^add$',views.Addnow, name="add"),
    url(r'^update$',views.update, name="update"),
    url(r'^delete$',views.delete, name="delete"),
    url(r'^show$',views.show ,name="show"),
    url(r'^show/(?P<pk>\w+)/$', views.showindividual, name="showpk"),
    url(r'^login$', views.login, name='apilogin'),
    url(r'^register$', views.register, name='apiregister'),
]
