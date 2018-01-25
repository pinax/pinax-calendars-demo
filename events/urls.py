from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import (
    DayView,
    EventCreateView,
    EventDeleteView,
    EventUpdateView,
    HomeView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("<int:year>/<int:month>/", HomeView.as_view(), name="monthly"),
    path("<int:year>/<int:month>/<int:day>/", DayView.as_view(), name="daily"),

    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),

    path("events/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
