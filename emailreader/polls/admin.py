from django.contrib import admin

from polls.models import Question, User, Choice, Answer, Quiz


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'updated_at')
    search_fields = ('username', 'email')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    search_fields = ('question_text',)
    list_filter = ('pub_date',)
    ordering = ('-pub_date',)

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes')
    search_fields = ('question__question_text', 'choice_text')
    list_filter = ('votes',)
    ordering = ('-votes',)

admin.site.register(Choice, ChoiceAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    search_fields = ('question__question_text', 'answer_text')
    list_filter = ('is_correct',)
    ordering = ('-is_correct',)

admin.site.register(Answer, AnswerAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'user', 'is_correct', 'created_at', 'updated_at')
    search_fields = ('question__question_text', 'answer__answer_text', 'user__username', 'user__email')
    list_filter = ('is_correct', 'created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Quiz, QuizAdmin)