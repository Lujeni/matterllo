from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# apiKey = settings.TRELLO_APIKEY

@method_decorator(login_required, name='dispatch')
class TokenView(TemplateView):
    template_name = "core/token.html"

      
    def get_context_data(self, **kwargs):
      token = self.request.GET.get('token')
      context = super(TokenView, self).get_context_data(**kwargs)
      context["apiKey"] = token
      return context