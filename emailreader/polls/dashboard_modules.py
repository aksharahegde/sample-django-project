"""
Django Jet Dashboard Modules for Polls App
This file contains custom dashboard modules to showcase Django Jet's dashboard capabilities.
"""

from django.template.loader import render_to_string
from django.utils.html import format_html
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta, date
import json

from jet.dashboard import modules
from jet.dashboard.modules import DashboardModule
from jet.dashboard.dashboard_modules import google_analytics, yandex_metrika

from .models import (
    User, Question, Choice, Answer, Quiz, Poll, PollOption, PollVote, 
    Category, Tag, Analytics
)


class UserStatsModule(DashboardModule):
    """Module showing user statistics"""
    title = 'User Statistics'
    template = 'admin/dashboard_modules/user_stats.html'
    
    def init_with_context(self, context):
        """Initialize module with user statistics"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Basic counts
        total_users = User.objects.count()
        new_users_30d = User.objects.filter(created_at__gte=last_30_days).count()
        verified_users = User.objects.filter(is_verified=True).count()
        premium_users = User.objects.filter(is_premium=True).count()
        
        # User roles distribution
        role_stats = User.objects.values('role').annotate(count=Count('id')).order_by('-count')
        
        # Gender distribution
        gender_stats = User.objects.values('gender').annotate(count=Count('id')).order_by('-count')
        
        # Average score
        avg_score = User.objects.aggregate(avg_score=Avg('score'))['avg_score'] or 0
        
        self.children = [
            {
                'total_users': total_users,
                'new_users_30d': new_users_30d,
                'verified_users': verified_users,
                'premium_users': premium_users,
                'role_stats': list(role_stats),
                'gender_stats': list(gender_stats),
                'avg_score': round(avg_score, 2),
            }
        ]


class QuestionStatsModule(DashboardModule):
    """Module showing question statistics"""
    title = 'Question Statistics'
    template = 'admin/dashboard_modules/question_stats.html'
    
    def init_with_context(self, context):
        """Initialize module with question statistics"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Basic counts
        total_questions = Question.objects.count()
        published_questions = Question.objects.filter(status='published').count()
        draft_questions = Question.objects.filter(status='draft').count()
        featured_questions = Question.objects.filter(is_featured=True).count()
        
        # New questions in last 30 days
        new_questions_30d = Question.objects.filter(created_at__gte=last_30_days).count()
        
        # Difficulty distribution
        difficulty_stats = Question.objects.values('difficulty').annotate(count=Count('id')).order_by('-count')
        
        # Category distribution
        category_stats = Question.objects.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Average view count
        avg_views = Question.objects.aggregate(avg_views=Avg('view_count'))['avg_views'] or 0
        
        # Most popular questions
        popular_questions = Question.objects.filter(status='published').order_by('-view_count')[:5]
        
        self.children = [
            {
                'total_questions': total_questions,
                'published_questions': published_questions,
                'draft_questions': draft_questions,
                'featured_questions': featured_questions,
                'new_questions_30d': new_questions_30d,
                'difficulty_stats': list(difficulty_stats),
                'category_stats': list(category_stats),
                'avg_views': round(avg_views, 2),
                'popular_questions': list(popular_questions),
            }
        ]


class QuizPerformanceModule(DashboardModule):
    """Module showing quiz performance analytics"""
    title = 'Quiz Performance'
    template = 'admin/dashboard_modules/quiz_performance.html'
    
    def init_with_context(self, context):
        """Initialize module with quiz performance data"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Basic quiz statistics
        total_quizzes = Quiz.objects.count()
        completed_quizzes = Quiz.objects.filter(status='completed').count()
        correct_answers = Quiz.objects.filter(is_correct=True).count()
        
        # Performance metrics
        completion_rate = (completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0
        accuracy_rate = (correct_answers / completed_quizzes * 100) if completed_quizzes > 0 else 0
        
        # Recent activity (last 30 days)
        recent_quizzes = Quiz.objects.filter(started_at__gte=last_30_days).count()
        
        # Status distribution
        status_stats = Quiz.objects.values('status').annotate(count=Count('id')).order_by('-count')
        
        # Average score
        avg_score = Quiz.objects.aggregate(avg_score=Avg('score_earned'))['avg_score'] or 0
        
        # Top performers
        top_performers = User.objects.annotate(
            total_score=Sum('quiz_attempts__score_earned'),
            quiz_count=Count('quiz_attempts')
        ).filter(quiz_count__gt=0).order_by('-total_score')[:5]
        
        # Most difficult questions
        difficult_questions = Question.objects.annotate(
            total_attempts=Count('quiz'),
            correct_attempts=Count('quiz', filter=Q(quiz__is_correct=True))
        ).filter(total_attempts__gt=0).annotate(
            success_rate=Avg('quiz__is_correct')
        ).order_by('success_rate')[:5]
        
        self.children = [
            {
                'total_quizzes': total_quizzes,
                'completed_quizzes': completed_quizzes,
                'correct_answers': correct_answers,
                'completion_rate': round(completion_rate, 2),
                'accuracy_rate': round(accuracy_rate, 2),
                'recent_quizzes': recent_quizzes,
                'status_stats': list(status_stats),
                'avg_score': round(avg_score, 2),
                'top_performers': list(top_performers),
                'difficult_questions': list(difficult_questions),
            }
        ]


class PollActivityModule(DashboardModule):
    """Module showing poll activity and results"""
    title = 'Poll Activity'
    template = 'admin/dashboard_modules/poll_activity.html'
    
    def init_with_context(self, context):
        """Initialize module with poll activity data"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Basic poll statistics
        total_polls = Poll.objects.count()
        active_polls = Poll.objects.filter(status='active').count()
        closed_polls = Poll.objects.filter(status='closed').count()
        total_votes = PollVote.objects.count()
        
        # Recent activity
        new_polls_30d = Poll.objects.filter(created_at__gte=last_30_days).count()
        recent_votes = PollVote.objects.filter(voted_at__gte=last_30_days).count()
        
        # Status distribution
        status_stats = Poll.objects.values('status').annotate(count=Count('id')).order_by('-count')
        
        # Most popular polls
        popular_polls = Poll.objects.annotate(
            vote_count=Count('votes')
        ).order_by('-vote_count')[:5]
        
        # Category distribution
        category_stats = Poll.objects.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Anonymous vs registered votes
        anonymous_votes = PollVote.objects.filter(user__isnull=True).count()
        registered_votes = PollVote.objects.filter(user__isnull=False).count()
        
        self.children = [
            {
                'total_polls': total_polls,
                'active_polls': active_polls,
                'closed_polls': closed_polls,
                'total_votes': total_votes,
                'new_polls_30d': new_polls_30d,
                'recent_votes': recent_votes,
                'status_stats': list(status_stats),
                'popular_polls': list(popular_polls),
                'category_stats': list(category_stats),
                'anonymous_votes': anonymous_votes,
                'registered_votes': registered_votes,
            }
        ]


class RecentActivityModule(DashboardModule):
    """Module showing recent activity across the platform"""
    title = 'Recent Activity'
    template = 'admin/dashboard_modules/recent_activity.html'
    
    def init_with_context(self, context):
        """Initialize module with recent activity data"""
        now = timezone.now()
        last_7_days = now - timedelta(days=7)
        
        # Recent users
        recent_users = User.objects.filter(created_at__gte=last_7_days).order_by('-created_at')[:5]
        
        # Recent questions
        recent_questions = Question.objects.filter(created_at__gte=last_7_days).order_by('-created_at')[:5]
        
        # Recent polls
        recent_polls = Poll.objects.filter(created_at__gte=last_7_days).order_by('-created_at')[:5]
        
        # Recent quiz attempts
        recent_quizzes = Quiz.objects.filter(started_at__gte=last_7_days).order_by('-started_at')[:5]
        
        # Recent votes
        recent_votes = PollVote.objects.filter(voted_at__gte=last_7_days).order_by('-voted_at')[:5]
        
        self.children = [
            {
                'recent_users': list(recent_users),
                'recent_questions': list(recent_questions),
                'recent_polls': list(recent_polls),
                'recent_quizzes': list(recent_quizzes),
                'recent_votes': list(recent_votes),
            }
        ]


class CategoryAnalyticsModule(DashboardModule):
    """Module showing category analytics and distribution"""
    title = 'Category Analytics'
    template = 'admin/dashboard_modules/category_analytics.html'
    
    def init_with_context(self, context):
        """Initialize module with category analytics"""
        # Category statistics
        categories = Category.objects.annotate(
            question_count=Count('question'),
            poll_count=Count('poll'),
            total_items=Count('question') + Count('poll')
        ).order_by('-total_items')
        
        # Tag usage statistics
        popular_tags = Tag.objects.annotate(
            question_count=Count('question'),
            poll_count=Count('poll'),
            total_usage=Count('question') + Count('poll')
        ).filter(total_usage__gt=0).order_by('-total_usage')[:10]
        
        # Most active categories
        active_categories = Category.objects.filter(is_active=True).annotate(
            recent_questions=Count('question', filter=Q(question__created_at__gte=timezone.now() - timedelta(days=30))),
            recent_polls=Count('poll', filter=Q(poll__created_at__gte=timezone.now() - timedelta(days=30)))
        ).order_by('-recent_questions', '-recent_polls')
        
        self.children = [
            {
                'categories': list(categories),
                'popular_tags': list(popular_tags),
                'active_categories': list(active_categories),
            }
        ]


class PerformanceMetricsModule(DashboardModule):
    """Module showing performance metrics and KPIs"""
    title = 'Performance Metrics'
    template = 'admin/dashboard_modules/performance_metrics.html'
    
    def init_with_context(self, context):
        """Initialize module with performance metrics"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Calculate various KPIs
        total_users = User.objects.count()
        total_questions = Question.objects.count()
        total_polls = Poll.objects.count()
        total_quizzes = Quiz.objects.count()
        total_votes = PollVote.objects.count()
        
        # Growth metrics
        new_users_growth = User.objects.filter(created_at__gte=last_30_days).count()
        new_questions_growth = Question.objects.filter(created_at__gte=last_30_days).count()
        new_polls_growth = Poll.objects.filter(created_at__gte=last_30_days).count()
        
        # Engagement metrics
        avg_views_per_question = Question.objects.aggregate(avg=Avg('view_count'))['avg'] or 0
        avg_votes_per_poll = Poll.objects.aggregate(avg=Avg('total_votes'))['avg'] or 0
        avg_score_per_user = User.objects.aggregate(avg=Avg('score'))['avg'] or 0
        
        # Completion rates
        quiz_completion_rate = Quiz.objects.filter(status='completed').count() / max(Quiz.objects.count(), 1) * 100
        
        # User engagement
        active_users = User.objects.filter(quiz_attempts__started_at__gte=last_30_days).distinct().count()
        user_engagement_rate = (active_users / max(total_users, 1)) * 100
        
        self.children = [
            {
                'total_users': total_users,
                'total_questions': total_questions,
                'total_polls': total_polls,
                'total_quizzes': total_quizzes,
                'total_votes': total_votes,
                'new_users_growth': new_users_growth,
                'new_questions_growth': new_questions_growth,
                'new_polls_growth': new_polls_growth,
                'avg_views_per_question': round(avg_views_per_question, 2),
                'avg_votes_per_poll': round(avg_votes_per_poll, 2),
                'avg_score_per_user': round(avg_score_per_user, 2),
                'quiz_completion_rate': round(quiz_completion_rate, 2),
                'user_engagement_rate': round(user_engagement_rate, 2),
            }
        ]


# Custom chart module for visualizations
class ChartModule(DashboardModule):
    """Custom chart module for data visualization"""
    title = 'Data Visualizations'
    template = 'admin/dashboard_modules/charts.html'
    
    def init_with_context(self, context):
        """Initialize module with chart data"""
        # Prepare data for various charts
        
        # User registration over time (last 30 days)
        user_registration_data = []
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            count = User.objects.filter(created_at__date=date).count()
            user_registration_data.append({'date': date.strftime('%Y-%m-%d'), 'count': count})
        user_registration_data.reverse()
        
        # Question difficulty distribution
        difficulty_data = list(Question.objects.values('difficulty').annotate(count=Count('id')))
        
        # Quiz accuracy by category
        category_accuracy = []
        categories = Category.objects.all()[:5]
        for category in categories:
            quizzes = Quiz.objects.filter(question__category=category)
            if quizzes.exists():
                accuracy = quizzes.filter(is_correct=True).count() / quizzes.count() * 100
                category_accuracy.append({'category': category.name, 'accuracy': round(accuracy, 2)})
        
        # Poll voting activity (last 7 days)
        voting_activity = []
        for i in range(7):
            date = timezone.now().date() - timedelta(days=i)
            count = PollVote.objects.filter(voted_at__date=date).count()
            voting_activity.append({'date': date.strftime('%Y-%m-%d'), 'votes': count})
        voting_activity.reverse()
        
        self.children = [
            {
                'user_registration_data': json.dumps(user_registration_data),
                'difficulty_data': json.dumps(difficulty_data),
                'category_accuracy': json.dumps(category_accuracy),
                'voting_activity': json.dumps(voting_activity),
            }
        ]
