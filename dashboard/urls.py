from django.urls import path
from . import views as dashboard_views
import users.views as users_view
# import railways.views as railways_view

urlpatterns = [
    # Dashboard view
    path("", dashboard_views.dashboard, name="dashboard"),
    # User authentication views
    path("login/", users_view.login_view, name="login"),
    path("register/", users_view.register_view, name="register"),
    path("logout/", users_view.logout_view, name="logout"),
    # Railway ticket booking views
    # path("book/", railways_view.book_ticket, name="book_ticket"),
    # path("ticket/<int:ticket_id>/", railways_view.view_ticket, name="view_ticket"),
    # path(
    #     "ticket/<int:ticket_id>/cancel/",
    #     railways_view.cancel_ticket,
    #     name="cancel_ticket",
    # ),
    # path("my_tickets/", railways_view.my_tickets, name="my_tickets"),
]
