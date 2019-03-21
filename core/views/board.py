# -*- coding: utf-8 -*-
from os import getenv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from trello import TrelloClient

from core.models import Board, Webhook


# trello_client = TrelloClient(api_key=settings.TRELLO_APIKEY, token=settings.TRELLO_TOKEN)


@method_decorator(login_required, name='dispatch')
class BoardView(ListView):
    """ List boards from Trello and create each board into database.
        Create the trello Hook also.
        Then returns the board template.
    """
    model = Board
    template_name = "core/board.html"

    def get(self, request):
        try:
            token = request.GET.get('token')
            user = request.user
            if token is None:
                boards= None
                return super(BoardView, self).get(request)
            else:
                trello_client = TrelloClient(api_key=settings.TRELLO_APIKEY, token=token)
                boards = trello_client.list_boards()
                if boards:
                    result = [h.delete() for h in trello_client.list_hooks()]
                    print("delete trello hook :: result={}".format(result))

                for board in boards:
                    print ("BOARD_ID:", board.id)
                    slug_board = slugify(board.name, allow_unicode=False)
                    b, created = Board.objects.get_or_create(name=slug_board, user=user, trelloBoard_id = board.id, trello_token = token)
                    host = getenv("MATTERLLO_HOST") or request.get_host()
                    url = "{}://{}/callback/{}/".format(request.scheme, host, b.id)
                    result = trello_client.create_hook(url, board.id)
                    print("create trello hook :: callback={} :: board={} :: result={}".format(url, slug_board, result))
                return super(BoardView, self).get(request)
        except Exception as e:
            print("unable to display board :: {}".format(e))
            return super(BoardView, self).get(request)

    def get_context_data(self, **kwargs):
        """ Fishy way to ensure trello_client is configured.
        """
        try:
            context = super(BoardView, self).get_context_data(**kwargs)
            token = self.request.GET.get('token')
            if token is None:
                context['board_list'] = None
            trello_client = TrelloClient(api_key=settings.TRELLO_APIKEY, token=token)
            trello_client.list_boards()
            user = self.request.user
            listboard = Board.objects.filter(trello_token=token)
            context['board_list'] = listboard
            context['trello_error'] = None
        except Exception as e:
            context['trello_error'] = "{} :: api_key={} :: token={}".format(e,
                    settings.TRELLO_APIKEY, settings.TRELLO_TOKEN)
        finally:
            return context


class BoardDetailView(DetailView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super(BoardDetailView, self).get_context_data(**kwargs)
        context['webhook_list'] = Webhook.objects.filter(board=self.kwargs['pk'])
        return context
