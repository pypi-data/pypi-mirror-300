"""
URL configuration for the mastodon application.

This module defines the URL patterns for the mastodon app, including:
- A redirect from the root URL to the "statuses/" URL.
- A URL pattern for the "statuses/" view.

Routes:
- "" : Redirects to "statuses/".
- "statuses/" : Maps to the `views.statuses` view.

Imports:
- `re_path` from `django.urls` for defining URL patterns.
- `RedirectView` from `django.views.generic` for handling URL redirects.
- `views` from `illallangi.django.mastodon` for the application-specific view functions.
"""

from django.urls import include, re_path

from illallangi.django.mastodon import views

app_name = "mastodon"

urlpatterns = [
    re_path(
        "^$",
        views.home_html,
        name="home_html",
    ),
    re_path(
        "^favicon.svg$",
        views.favicon,
        name="favicon",
    ),
    re_path(
        "^favicon.ico$",
        views.favicon,
    ),
    re_path(
        "^statuses/",
        include("illallangi.django.mastodon.urls.status"),
    ),
]
