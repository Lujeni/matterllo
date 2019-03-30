from django.views.generic import TemplateView

class ReadmeView(TemplateView):
    template_name = "core/readme.html"

    def get_context_data(self, **kwargs):
      context = super(ReadmeView, self).get_context_data(**kwargs)
      return context