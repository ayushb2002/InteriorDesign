from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gallery", views.gallery, name="gallery"),
    path("contact", views.contact, name="contact"),
    path("login_view", views.login_view, name="login_view"),
    path("register_view", views.register_view, name="register_view"),
    path("pricing", views.pricing, name="pricing"),
    path("register_user", views.register_user, name="register_user"),
    path("login_user", views.login_user, name="login_user"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("shop", views.shop, name="shop"),
    path("sendMail", views.sendMail, name="sendMail"),
    path("buyItems/<int:item_id>", views.buyItems, name="buyItems"),
    path("delOrder/<int:oid>", views.delOrder, name="delOrder"),
    path("cart", views.cart, name="cart"),
    path("payment", views.payment, name="payment"),
    path("paid", views.paid, name="paid"),
    path("visit", views.visit, name="visit"),
    path("bookVisit", views.bookVisit, name="bookVisit")
]