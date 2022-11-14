from django.contrib import admin
from django.utils import timezone
from django.db.models.base import Model

from .models import QuestionOption
from .models import Question
from .models import Voting
from .models import BinaryVoting, BinaryQuestion, BinaryQuestionOption
from .models import MultipleVoting, MultipleQuestion, MultipleQuestionOption

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)
        
def start_vote(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

def stop_vote(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]
    

class BinaryQuestionOptionInline(admin.TabularInline):
    model = BinaryQuestionOption
    
class BinaryQuestionAdmin(admin.ModelAdmin):
    inlines = [BinaryQuestionOptionInline]
    
class BinaryVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]
    
class MultipleQuestionOptionInline(admin.TabularInline):
    model = MultipleQuestionOption

class MultipleQuestionAdmin(admin.ModelAdmin):
    inlines = [MultipleQuestionOptionInline]

class MultipleVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    #date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(BinaryVoting, BinaryVotingAdmin)
admin.site.register(BinaryQuestion, BinaryQuestionAdmin)
admin.site.register(MultipleVoting, MultipleVotingAdmin)
admin.site.register(MultipleQuestion, MultipleQuestionAdmin)
