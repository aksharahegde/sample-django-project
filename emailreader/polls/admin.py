from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg, Sum
from django.contrib.admin import DateFieldListFilter
from jet.admin import CompactInline
from jet.filters import DateRangeFilter, RelatedFieldAjaxListFilter

from polls.models import (
    Category, Tag, User, Question, Choice, Answer, Quiz,
    Poll, PollOption, PollVote, Analytics
)


# =============================================================================
# INLINE ADMIN CLASSES
# =============================================================================

class ChoiceInline(CompactInline):
    """Compact inline for choices with Django Jet styling"""
    model = Choice
    extra = 0
    fields = ('choice_text', 'is_correct', 'votes', 'order')
    ordering = ('order',)


class PollOptionInline(CompactInline):
    """Compact inline for poll options"""
    model = PollOption
    extra = 0
    fields = ('option_text', 'votes', 'order', 'description')
    ordering = ('order',)


# =============================================================================
# MAIN ADMIN CLASSES
# =============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin with Django Jet features"""
    list_display = ('name', 'color_display', 'is_active', 'question_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'color')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def color_display(self, obj):
        """Display color as a colored square"""
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></span> {}',
            obj.color, obj.color
        )
    color_display.short_description = 'Color'
    color_display.admin_order_field = 'color'
    
    def question_count(self, obj):
        """Show number of questions in this category"""
        count = obj.question_set.count()
        if count > 0:
            url = reverse('admin:polls_question_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} questions</a>', url, count)
        return '0 questions'
    question_count.short_description = 'Questions'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin with usage statistics"""
    list_display = ('name', 'slug', 'usage_count', 'question_count', 'poll_count')
    list_filter = ('usage_count',)
    search_fields = ('name', 'slug', 'description')
    list_editable = ('usage_count',)
    ordering = ('name',)
    
    def question_count(self, obj):
        """Show number of questions using this tag"""
        count = obj.question_set.count()
        if count > 0:
            url = reverse('admin:polls_question_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} questions</a>', url, count)
        return '0 questions'
    question_count.short_description = 'Questions'
    
    def poll_count(self, obj):
        """Show number of polls using this tag"""
        count = obj.poll_set.count()
        if count > 0:
            url = reverse('admin:polls_poll_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} polls</a>', url, count)
        return '0 polls'
    poll_count.short_description = 'Polls'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Enhanced user admin with comprehensive Django Jet features"""
    list_display = (
        'username', 'full_name', 'email', 'role', 'is_verified', 'is_premium',
        'score', 'quiz_count', 'created_at'
    )
    list_filter = (
        'role', 'is_verified', 'is_premium', 'gender',
        ('created_at', DateRangeFilter),
        ('last_login', DateRangeFilter),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('role', 'is_verified', 'is_premium')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Profile', {
            'fields': ('gender', 'age', 'bio', 'avatar')
        }),
        ('Status & Permissions', {
            'fields': ('role', 'is_verified', 'is_premium')
        }),
        ('Statistics', {
            'fields': ('score', 'last_login'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def quiz_count(self, obj):
        """Show number of quiz attempts"""
        count = obj.quiz_attempts.count()
        if count > 0:
            url = reverse('admin:polls_quiz_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} attempts</a>', url, count)
        return '0 attempts'
    quiz_count.short_description = 'Quiz Attempts'
    
    def get_queryset(self, request):
        """Optimize queryset with annotations"""
        return super().get_queryset(request).annotate(
            total_quizzes=Count('quiz_attempts')
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Comprehensive question admin with Django Jet features"""
    list_display = (
        'title', 'category', 'difficulty', 'status', 'author', 'points',
        'view_count', 'like_count', 'choice_count', 'is_featured', 'pub_date'
    )
    list_filter = (
        'category', 'difficulty', 'status', 'is_featured',
        ('pub_date', DateRangeFilter),
        ('created_at', DateRangeFilter),
        ('author', RelatedFieldAjaxListFilter),
    )
    search_fields = ('title', 'question_text', 'slug', 'author__username')
    list_editable = ('status', 'is_featured', 'points')
    ordering = ('-pub_date',)
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Question Content', {
            'fields': ('title', 'slug', 'question_text', 'explanation', 'image')
        }),
        ('Categorization', {
            'fields': ('category', 'tags', 'difficulty')
        }),
        ('Settings', {
            'fields': ('status', 'author', 'points', 'time_limit', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('pub_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ChoiceInline]
    
    def choice_count(self, obj):
        """Show number of choices"""
        count = obj.choices.count()
        if count > 0:
            url = reverse('admin:polls_choice_changelist') + f'?question__id__exact={obj.id}'
            return format_html('<a href="{}">{} choices</a>', url, count)
        return '0 choices'
    choice_count.short_description = 'Choices'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Choice admin with enhanced features"""
    list_display = (
        'choice_text_short', 'question', 'is_correct', 'votes', 'order'
    )
    list_filter = (
        'is_correct', 'votes',
        ('question', RelatedFieldAjaxListFilter),
        ('question__category', RelatedFieldAjaxListFilter),
    )
    search_fields = ('choice_text', 'question__title', 'explanation')
    list_editable = ('is_correct', 'votes', 'order')
    ordering = ('question', 'order')
    
    fieldsets = (
        ('Choice Content', {
            'fields': ('question', 'choice_text', 'explanation')
        }),
        ('Settings', {
            'fields': ('is_correct', 'votes', 'order')
        }),
    )
    
    def choice_text_short(self, obj):
        """Display truncated choice text"""
        text = obj.choice_text
        return text[:50] + '...' if len(text) > 50 else text
    choice_text_short.short_description = 'Choice Text'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer admin for quiz responses"""
    list_display = (
        'answer_text_short', 'question', 'is_correct', 'confidence_level', 'source_short'
    )
    list_filter = (
        'is_correct', 'confidence_level',
        ('question', RelatedFieldAjaxListFilter),
    )
    search_fields = ('answer_text', 'question__title', 'source')
    list_editable = ('is_correct', 'confidence_level')
    ordering = ('-is_correct', '-confidence_level')
    
    def answer_text_short(self, obj):
        """Display truncated answer text"""
        text = obj.answer_text
        return text[:50] + '...' if len(text) > 50 else text
    answer_text_short.short_description = 'Answer Text'
    
    def source_short(self, obj):
        """Display truncated source URL"""
        if obj.source:
            url = obj.source
            return url[:30] + '...' if len(url) > 30 else url
        return '-'
    source_short.short_description = 'Source'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Comprehensive quiz admin with analytics"""
    list_display = (
        'user', 'question', 'status', 'is_correct', 'score_earned',
        'time_spent', 'started_at', 'completed_at'
    )
    list_filter = (
        'status', 'is_correct',
        ('started_at', DateRangeFilter),
        ('completed_at', DateRangeFilter),
        ('user', RelatedFieldAjaxListFilter),
        ('question__category', RelatedFieldAjaxListFilter),
    )
    search_fields = (
        'user__username', 'question__title', 'feedback', 'ip_address'
    )
    list_editable = ('status',)
    ordering = ('-started_at',)
    
    fieldsets = (
        ('Quiz Details', {
            'fields': ('question', 'selected_choice', 'user', 'status')
        }),
        ('Results', {
            'fields': ('is_correct', 'score_earned', 'time_spent', 'feedback')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Poll admin with comprehensive features"""
    list_display = (
        'title', 'category', 'status', 'author', 'total_votes',
        'option_count', 'is_featured', 'start_date', 'end_date'
    )
    list_filter = (
        'status', 'is_featured', 'allow_multiple_choices', 'is_anonymous',
        'category',
        ('start_date', DateRangeFilter),
        ('end_date', DateRangeFilter),
        ('author', RelatedFieldAjaxListFilter),
    )
    search_fields = ('title', 'description', 'author__username')
    list_editable = ('status', 'is_featured')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Poll Content', {
            'fields': ('title', 'description', 'category', 'tags')
        }),
        ('Settings', {
            'fields': (
                'status', 'author', 'allow_multiple_choices', 'is_anonymous',
                'max_votes_per_user', 'is_featured'
            )
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('total_votes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'total_votes')
    inlines = [PollOptionInline]
    
    def option_count(self, obj):
        """Show number of options"""
        count = obj.options.count()
        if count > 0:
            url = reverse('admin:polls_polloption_changelist') + f'?poll__id__exact={obj.id}'
            return format_html('<a href="{}">{} options</a>', url, count)
        return '0 options'
    option_count.short_description = 'Options'


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    """Poll option admin"""
    list_display = ('option_text_short', 'poll', 'votes', 'order')
    list_filter = (
        'votes', 'order',
        ('poll', RelatedFieldAjaxListFilter),
        ('poll__category', RelatedFieldAjaxListFilter),
    )
    search_fields = ('option_text', 'poll__title', 'description')
    list_editable = ('votes', 'order')
    ordering = ('poll', 'order')
    
    def option_text_short(self, obj):
        """Display truncated option text"""
        text = obj.option_text
        return text[:50] + '...' if len(text) > 50 else text
    option_text_short.short_description = 'Option Text'


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    """Poll vote admin with tracking features"""
    list_display = (
        'voter_display', 'poll', 'option', 'voted_at'
    )
    list_filter = (
        ('voted_at', DateRangeFilter),
        ('poll', RelatedFieldAjaxListFilter),
        ('option', RelatedFieldAjaxListFilter),
    )
    search_fields = (
        'user__username', 'poll__title', 'option__option_text',
        'ip_address', 'user_agent'
    )
    ordering = ('-voted_at',)
    
    fieldsets = (
        ('Vote Details', {
            'fields': ('poll', 'option', 'user', 'voted_at')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('voted_at',)
    
    def voter_display(self, obj):
        """Display voter information"""
        if obj.user:
            url = reverse('admin:polls_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        else:
            return f"Anonymous ({obj.ip_address})"
    voter_display.short_description = 'Voter'


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    """Analytics admin for dashboard data"""
    list_display = ('date', 'metric_name', 'metric_value', 'category')
    list_filter = (
        'metric_name', 'category',
        ('date', DateRangeFilter),
    )
    search_fields = ('metric_name', 'category')
    list_editable = ('metric_value',)
    ordering = ('-date', 'metric_name')
    
    fieldsets = (
        ('Metric Data', {
            'fields': ('date', 'metric_name', 'metric_value', 'category')
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)


# =============================================================================
# ADMIN SITE CONFIGURATION
# =============================================================================

# Configure admin site
admin.site.site_header = "Django Jet Admin Demo"
admin.site.site_title = "Jet Admin"
admin.site.index_title = "Polls & Analytics Dashboard"

# Customize admin site URLs
admin.site.site_url = "/"

# Set up admin site ordering
admin.site._registry[Category].admin_ordering = 1
admin.site._registry[Tag].admin_ordering = 2
admin.site._registry[User].admin_ordering = 3
admin.site._registry[Question].admin_ordering = 4
admin.site._registry[Choice].admin_ordering = 5
admin.site._registry[Answer].admin_ordering = 6
admin.site._registry[Quiz].admin_ordering = 7
admin.site._registry[Poll].admin_ordering = 8
admin.site._registry[PollOption].admin_ordering = 9
admin.site._registry[PollVote].admin_ordering = 10
admin.site._registry[Analytics].admin_ordering = 11