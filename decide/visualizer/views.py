import json, csv, requests, ast
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.generic.base import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from voting.models import Voting

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

#Generate a CSV File 
class Votes_csv(View):
   def get(self,request,*args,**kwargs):
        vid = kwargs.get('voting_id', 0)
        try:
            voting = mods.get('voting', params={'id':vid})
        except:
            raise Http404
        res = HttpResponse(content_type="text/csv")
        res['Content-Disposition'] = 'attachment; filename=' + str(voting[0]['name']) + '-SimpleVoting.csv'

        csv_file = csv.writer(res)
        csv_file.writerow(["Opcion", "Puntuacion", "Votos"])
        
        for vote in (voting[0]['postproc']):
            csv_file.writerow([vote["option"], vote["postproc"], vote["votes"]])
        return res

