from django.shortcuts import render, HttpResponse
from voting.models import Voting
from django.utils import translation


def homepage(request):
    votingsList  = list(Voting.objects.all())
    votings = {}
    for voting in votingsList:
        votings[voting.id] = {
                'id': voting.id,
                'name': voting.name,
            }
    return render(request, 'homepage/homepage.html', {"votings":votings.values()})