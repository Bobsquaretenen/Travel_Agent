from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('travel/', views.tour_list, name='tour_list'),
    path('information/', views.info_view, name='information'),
    path('contacts/', views.contact_view, name='contacts'),
    path('login/', views.login_view, name='login'),
    path('logup/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my-tours/', views.my_tours_view, name='my_tours'),
    path('add-card/', views.add_card_view, name='add_card'),
    path('buy/<int:tour_id>/', views.buy_tour_view, name='buy_tour'),
    path('complete/<int:usertour_id>/', views.complete_tour_view, name='complete_tour'),
    path('test-403/', views.exception_403, name='test_403'),
]