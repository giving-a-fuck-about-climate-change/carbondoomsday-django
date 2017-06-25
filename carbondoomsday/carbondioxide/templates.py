"""Template views."""

from django.views.generic import TemplateView


class CO2TrackerView(TemplateView):
    """The CO2 tracker home page."""
    template_name = 'co2-tracker.html'
