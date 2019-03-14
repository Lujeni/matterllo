from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

apiKey = settings.TRELLO_APIKEY

@method_decorator(login_required, name='dispatch')
class OauthView(TemplateView):
    # model = Bridge
    template_name = "core/oauth.html"
    def get_context_data(self, **kwargs):
      print(self.request.get_host())
      returnURL = 'http://localhost:8000'+'/accessToken'
      context = super(OauthView, self).get_context_data(**kwargs)
      context["apiKey"] = apiKey
      # returnURL = "https://juliandong.com"
      context["returnURL"] = returnURL
      return context