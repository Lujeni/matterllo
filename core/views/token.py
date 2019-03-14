from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# apiKey = settings.TRELLO_APIKEY

@method_decorator(login_required, name='dispatch')
class TokenView(TemplateView):
    # model = Bridge
    def get(self, request, *args, **kwargs):
      token = request.GET.get('token')
      print request.method
      response = HttpResponse(token)
      return response
      
    def get_context_data(self, **kwargs):
      # print(settings.TRELLO_APIKEY)
      context = super(OauthView, self).get_context_data(**kwargs)
      context["apiKey"] = apiKey
      return context