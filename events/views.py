import datetime

from collections import defaultdict

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from account.mixins import LoginRequiredMixin

from .models import Event


class EventsHelper(object):

    @classmethod
    def day_url(cls, year, month, day, has_event, **kwargs):
        if has_event:
            return reverse("daily", args=[year, month, day])

    @classmethod
    def month_url(cls, year, month, **kwargs):
        return reverse("monthly", args=[year, month])

    @classmethod
    def events_by_day(cls, year, month, **kwargs):
        events = Event.objects.filter(date__year=year, date__month=month).order_by("date")
        days = defaultdict(list)
        for event in events:
            days[event.date.day].append(event)
        return days


class GoHomeMixin(object):

    def get_success_url(self):
        return reverse("home")


class OwnerMixin(object):

    def get_queryset(self):
        return self.model._default_manager.filter(created_by=self.request.user)


class HomeView(TemplateView):

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        if month and year:
            the_date = datetime.date(year=int(year), month=int(month), day=1)
        else:
            the_date = timezone.now().date()
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            "the_date": the_date,
            "events": EventsHelper
        })
        return context


class DayView(TemplateView):

    template_name = "daily.html"

    def get_context_data(self, **kwargs):
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        day = self.kwargs.get("day")
        the_date = datetime.date(year=int(year), month=int(month), day=int(day))
        context = super(DayView, self).get_context_data(**kwargs)
        context.update({
            "the_date": the_date,
            "events": Event.objects.filter(date=the_date)
        })
        return context


class EventCreateView(LoginRequiredMixin, OwnerMixin, GoHomeMixin, CreateView):
    model = Event
    fields = ["title", "date"]

    def form_valid(self, form):
        event = form.save(commit=False)
        event.created_by = self.request.user
        event.save()
        return redirect(self.get_success_url())


class EventUpdateView(LoginRequiredMixin, OwnerMixin, GoHomeMixin, UpdateView):
    model = Event
    fields = ["title", "date"]


class EventDeleteView(LoginRequiredMixin, OwnerMixin, GoHomeMixin, DeleteView):
    model = Event
