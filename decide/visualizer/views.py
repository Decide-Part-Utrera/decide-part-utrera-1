import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404




from django.http import JsonResponse
from django.http.response import HttpResponse

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context


class VisualizerDetails(TemplateView):

    def get(self, request, voting_id):
        try:
            r = mods.get('voting', params={'id': voting_id})
            voting = r[0]
            responseData= {
                'id': voting["id"],
                'name': voting["name"],
                'description': voting["desc"],
                'fecha_inicio': voting["start_date"],
                'fecha_fin': voting["end_date"],
                'question_desc': voting["question"]["desc"],
                'question_options': voting["question"]["options"],
                'postproc': voting["postproc"],
            }
        except:
            responseData = {}

        return JsonResponse(responseData)
