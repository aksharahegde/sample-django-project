"""
Django Jet Dashboard Configuration for Polls App
This file configures the dashboard layout and modules.
"""

from jet.dashboard import Dashboard, AppDashboardModule
from jet.dashboard.modules import DashboardModule, LinkList
from jet.dashboard.dashboard_modules import google_analytics, yandex_metrika

from .dashboard_modules import (
    UserStatsModule, QuestionStatsModule, QuizPerformanceModule,
    PollActivityModule, RecentActivityModule, CategoryAnalyticsModule,
    PerformanceMetricsModule, ChartModule
)


class CustomIndexDashboard(Dashboard):
    """Custom dashboard for the main admin index page"""

    columns = 3

    def init_with_context(self, context):
        """Initialize the dashboard with modules"""

        # Top row - Key metrics
        self.children.append(PerformanceMetricsModule())
        self.children.append(UserStatsModule())
        self.children.append(QuestionStatsModule())

        # Second row - Analytics
        self.children.append(QuizPerformanceModule())
        self.children.append(PollActivityModule())
        self.children.append(CategoryAnalyticsModule())

        # Third row - Charts and recent activity
        self.children.append(ChartModule())
        self.children.append(RecentActivityModule())

        # Quick links module
        self.children.append(LinkList(
            title='Quick Links',
            children=[
                {
                    'title': 'Create New Question',
                    'url': '/admin/polls/question/add/',
                    'external': False,
                },
                {
                    'title': 'Create New Poll',
                    'url': '/admin/polls/poll/add/',
                    'external': False,
                },
                {
                    'title': 'Add New User',
                    'url': '/admin/polls/user/add/',
                    'external': False,
                },
                {
                    'title': 'View All Questions',
                    'url': '/admin/polls/question/',
                    'external': False,
                },
                {
                    'title': 'View All Polls',
                    'url': '/admin/polls/poll/',
                    'external': False,
                },
                {
                    'title': 'View Analytics',
                    'url': '/admin/polls/analytics/',
                    'external': False,
                },
            ]
        ))


class CustomAppDashboard(Dashboard):
    """Custom dashboard for the polls app"""

    columns = 2

    def init_with_context(self, context):
        """Initialize the app dashboard with modules"""

        # App-specific modules
        self.children.append(UserStatsModule())
        self.children.append(QuestionStatsModule())
        self.children.append(QuizPerformanceModule())
        self.children.append(PollActivityModule())
        self.children.append(ChartModule())
        self.children.append(RecentActivityModule())

        # App navigation links
        self.children.append(LinkList(
            title='Polls App Navigation',
            children=[
                {
                    'title': 'Questions Management',
                    'url': '/admin/polls/question/',
                    'external': False,
                },
                {
                    'title': 'Polls Management',
                    'url': '/admin/polls/poll/',
                    'external': False,
                },
                {
                    'title': 'Users Management',
                    'url': '/admin/polls/user/',
                    'external': False,
                },
                {
                    'title': 'Quiz Results',
                    'url': '/admin/polls/quiz/',
                    'external': False,
                },
                {
                    'title': 'Categories',
                    'url': '/admin/polls/category/',
                    'external': False,
                },
                {
                    'title': 'Tags',
                    'url': '/admin/polls/tag/',
                    'external': False,
                },
            ]
        ))


# # Register the dashboards
# Dashboard.register(CustomIndexDashboard)
# Dashboard.register(CustomAppDashboard)
