from . import validators
import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from voting.models import *
import json

from census.models import Census
from django.forms.models import inlineformset_factory
from rest_framework.views import APIView
import json
from voting.models import *
from mixnet.mixcrypt import *
from base import mods


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def get(self, request, *args, **kwargs):
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)



def create_BinaryQuestion(self):
    option_yes = False
    option_no = False

    try:
        options = QuestionOption.objects.all().filter(question=self)
        for o in options:
            if o.option == 'Sí':
                option_yes = True
            elif o.option == 'No':
                option_no = True

            if option_yes and option_no:
                break
    except:
        pass

    if not option_yes:
        option_yes = QuestionOption(option='Sí', number=1, question=self)
        option_yes.save()
    if not option_no:
        option_no = QuestionOption(option='No', number=2, question=self)
        option_no.save()
        
        
def create_ScoreQuestion(self):
    try:
        options = QuestionOption.objects.all().filter(question=self)
        list_options = [str(o.option) for o in options]

        for i in range(0, 6):
            if str(i) in list_options:
                continue
            else:
                option = QuestionOption(option=str(i), number=(i+1), question=self)
                option.save()

    except:
        pass


class GiveMeAB(APIView):

    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def encrypt_msg(self, msg, v, bits = settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def post(self, request, *args, **kwargs):
        for data in ['id_v', 'question_opt']:
            if not data in request.data:
                return Response({'Falta algo miarma'}, status=status.HTTP_400_BAD_REQUEST)
        
        votacion = Voting.objects.get(id=request.data.get('id_v'))
        question = votacion.question
        dicc = str(request.data.get('question_opt')).replace('\'', '\"')
        diccionario = json.loads(dicc)
        opt = QuestionOption(question=question, option=diccionario['option'], number=diccionario['number'])
        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL, defaults={'me': True, 'name': 'test auth'})
        
        ''' ====== Encriptado del voto ======'''
        a, b = self.encrypt_msg(opt.number, votacion)
        ''' ================================='''
        return Response({
            'a': a,
            'b': b
        })