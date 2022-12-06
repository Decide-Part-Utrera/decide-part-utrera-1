import json
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from django.contrib.auth.models import User

from base import mods

from django.shortcuts import get_object_or_404
from voting.models import *
from census.models import *
from authentication.serializers import *
import random



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


class VisualizerGetAllCensus(TemplateView):

    def get(self, request):

        data  = list(Census.objects.all())
        responseData = {}
        for censo in data:
            responseData[censo.id] = { 
                'voting' : censo.voting_id,
                'voter': censo.voter_id
            }

        return JsonResponse(responseData)




class VisualizerGetAllUsers(TemplateView):

    def get(self, request):

        data  = list(User.objects.all())
        responseData = {}
        for user in data:
            responseData[user.username] = { 
                'username' : user.username,
                'email': user.email
            }

        return JsonResponse(responseData)
