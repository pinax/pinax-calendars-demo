from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView

from account.mixins import LoginRequiredMixin

from .models import Event


class GoHomeMixin(object):

    def get_success_url(self):
        return reverse("home")


class OwnerMixin(object):

    def get_queryset(self):
        return self.model._default_manager.filter(created_by=self.request.user)


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
