import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')


    def test_lofensivo_dont_pass(self):
        self.login()
        question = Question(desc='Tonto, esta descripcion contiene alguna palabra ofensiva? Pis, ceporro')
        with self.assertRaises(ValidationError):
            question.clean()

    def test_lofensivo_pass_by_words(self):
        self.login()
        question = Question(desc='Esta descripcion no contiene lenguaje ofensivo')
        question.clean()
        self.assertEqual(question.desc, 'Esta descripcion no contiene lenguaje ofensivo')

    def test_lofensivo_pass_by_percentage(self):
        self.login()
        question = Question(desc='Esta descripcion contiene solo una palabra ofensiva, tonto, pero se necesita que el 20 por ciento sean palabras ofensivas')
        question.clean()
        self.assertEqual(question.desc, 'Esta descripcion contiene solo una palabra ofensiva, tonto, pero se necesita que el 20 por ciento sean palabras ofensivas')


    #Test de binary question con opciones por defecto
    def test_BinaryQuestion(self):
        q = Question(desc='Test BinaryQuestion', type='BQ')
        q.save()

        self.assertEquals(len(q.options.all()), 2)
        self.assertEquals(q.type, 'BQ')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)

    #Test de binary question con opciones
    def test_BinaryQuestion_Options(self):
        q = Question(desc='Test BinaryQuestion with options', type='BQ')
        q.save()
        qo1 = QuestionOption(question = q, option = 'Prueba1')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Prueba2')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Prueba3')
        qo3.save()

        self.assertEquals(len(q.options.all()), 2)
        self.assertEquals(q.type, 'BQ')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)
        
        
  #Test de Score question con opciones por defecto
    def test_ScoreQuestion(self):
        q = Question(desc='Test ScoreQuestion', type='SQ')
        q.save()

        self.assertEquals(len(q.options.all()), 6)
        self.assertEquals(q.type, 'SQ')
        self.assertEquals(q.options.all()[0].option, '0')
        self.assertEquals(q.options.all()[1].option, '1')
        self.assertEquals(q.options.all()[2].option, '2')
        self.assertEquals(q.options.all()[3].option, '3')
        self.assertEquals(q.options.all()[4].option, '4')
        self.assertEquals(q.options.all()[5].option, '5')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)
        self.assertEquals(q.options.all()[2].number, 3)
        self.assertEquals(q.options.all()[3].number, 4)
        self.assertEquals(q.options.all()[4].number, 5)
        self.assertEquals(q.options.all()[5].number, 6)
        

    #Test de Score question con opciones
    def test_ScoreQuestion_Options(self):
        q = Question(desc='Test ScoreQuestion with options', type='SQ')
        q.save()
        qo1 = QuestionOption(question = q, option = 'Prueba1')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Prueba2')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Prueba3')
        qo3.save()

        self.assertEquals(len(q.options.all()), 6)
        self.assertEquals(q.type, 'SQ')
        self.assertEquals(q.options.all()[0].option, '0')
        self.assertEquals(q.options.all()[1].option, '1')
        self.assertEquals(q.options.all()[2].option, '2')
        self.assertEquals(q.options.all()[3].option, '3')
        self.assertEquals(q.options.all()[4].option, '4')
        self.assertEquals(q.options.all()[5].option, '5')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)
        self.assertEquals(q.options.all()[2].number, 3)
        self.assertEquals(q.options.all()[3].number, 4)
        self.assertEquals(q.options.all()[4].number, 5)
        self.assertEquals(q.options.all()[5].number, 6)