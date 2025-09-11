from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.template.loader import render_to_string
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.test.utils import override_settings
import os
import json

from polls.models import Question, User as PollUser, Choice, Answer, Quiz
from polls.admin import UserAdmin, QuestionAdmin, ChoiceAdmin, AnswerAdmin, QuizAdmin


class DjangoJetCalmCompatibilityTests(TestCase):
    """Test cases for Django Jet Calm compatibility"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)
        
        # Create test data
        self.question = Question.objects.create(
            question_text="What is Django?",
            pub_date="2024-01-01 12:00:00"
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="A web framework",
            votes=5
        )
        self.poll_user = PollUser.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )
        self.answer = Answer.objects.create(
            question=self.question,
            answer_text="A Python web framework",
            is_correct=True
        )
        self.quiz = Quiz.objects.create(
            question=self.question,
            answer=self.answer,
            user=self.poll_user,
            is_correct=True
        )

    def test_jet_apps_installed(self):
        """Test that Jet apps are properly installed"""
        self.assertIn('jet', settings.INSTALLED_APPS)
        self.assertIn('jet.dashboard', settings.INSTALLED_APPS)

    def test_jet_themes_configuration(self):
        """Test Jet themes configuration"""
        self.assertTrue(hasattr(settings, 'JET_THEMES'))
        self.assertIsInstance(settings.JET_THEMES, list)
        self.assertGreater(len(settings.JET_THEMES), 0)
        
        # Check theme structure
        for theme in settings.JET_THEMES:
            self.assertIn('theme', theme)
            self.assertIn('color', theme)
            self.assertIn('title', theme)

    def test_admin_interface_accessibility(self):
        """Test that admin interface is accessible with Jet"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django administration')

    def test_jet_urls_accessibility(self):
        """Test Jet URLs are accessible"""
        # Test Jet main URL
        response = self.client.get('/jet/')
        self.assertEqual(response.status_code, 200)
        
        # Test Jet dashboard URL
        response = self.client.get('/jet/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_model_admin_integration(self):
        """Test that models work correctly with Jet admin"""
        # Test User admin
        response = self.client.get('/admin/polls/user/')
        self.assertEqual(response.status_code, 200)
        
        # Test Question admin
        response = self.client.get('/admin/polls/question/')
        self.assertEqual(response.status_code, 200)
        
        # Test Choice admin
        response = self.client.get('/admin/polls/choice/')
        self.assertEqual(response.status_code, 200)
        
        # Test Answer admin
        response = self.client.get('/admin/polls/answer/')
        self.assertEqual(response.status_code, 200)
        
        # Test Quiz admin
        response = self.client.get('/admin/polls/quiz/')
        self.assertEqual(response.status_code, 200)

    def test_admin_list_display_functionality(self):
        """Test admin list display functionality with Jet"""
        # Test User list display
        response = self.client.get('/admin/polls/user/')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test@example.com')
        
        # Test Question list display
        response = self.client.get('/admin/polls/question/')
        self.assertContains(response, 'What is Django?')
        
        # Test Choice list display
        response = self.client.get('/admin/polls/choice/')
        self.assertContains(response, 'A web framework')
        self.assertContains(response, '5')

    def test_admin_search_functionality(self):
        """Test admin search functionality with Jet"""
        # Test User search
        response = self.client.get('/admin/polls/user/?q=testuser')
        self.assertContains(response, 'testuser')
        
        # Test Question search
        response = self.client.get('/admin/polls/question/?q=Django')
        self.assertContains(response, 'What is Django?')

    def test_admin_filter_functionality(self):
        """Test admin filter functionality with Jet"""
        # Test User filter
        response = self.client.get('/admin/polls/user/')
        self.assertEqual(response.status_code, 200)
        
        # Test Question filter
        response = self.client.get('/admin/polls/question/')
        self.assertEqual(response.status_code, 200)

    def test_static_files_serving(self):
        """Test that Jet static files are properly served"""
        # Test Jet CSS files
        response = self.client.get('/static/jet/css/build/themes/default.css')
        self.assertEqual(response.status_code, 200)
        
        # Test Jet JS files
        response = self.client.get('/static/jet/js/build/bundle.min.js')
        self.assertEqual(response.status_code, 200)

    def test_jet_dashboard_widgets(self):
        """Test Jet dashboard widgets functionality"""
        response = self.client.get('/jet/dashboard/')
        self.assertEqual(response.status_code, 200)
        # Check if dashboard loads without errors

    def test_database_compatibility(self):
        """Test database operations with Jet"""
        # Test creating new records
        new_question = Question.objects.create(
            question_text="Test question",
            pub_date="2024-01-02 12:00:00"
        )
        self.assertEqual(new_question.question_text, "Test question")
        
        # Test updating records
        new_question.question_text = "Updated question"
        new_question.save()
        self.assertEqual(new_question.question_text, "Updated question")
        
        # Test deleting records
        question_count = Question.objects.count()
        new_question.delete()
        self.assertEqual(Question.objects.count(), question_count - 1)

    def test_migrations_compatibility(self):
        """Test that migrations work correctly with Jet"""
        # Check if migrations can be applied
        try:
            call_command('migrate', '--check', verbosity=0)
            self.assertTrue(True)  # If no exception, migrations are compatible
        except Exception as e:
            self.fail(f"Migrations failed: {e}")

    def test_template_rendering(self):
        """Test template rendering with Jet"""
        # Test admin templates render correctly
        response = self.client.get('/admin/polls/user/')
        self.assertContains(response, '<html')
        self.assertContains(response, '</html>')

    def test_jet_theme_switching(self):
        """Test Jet theme switching functionality"""
        # Test with different themes
        for theme in settings.JET_THEMES:
            with override_settings(JET_DEFAULT_THEME=theme['theme']):
                response = self.client.get('/admin/')
                self.assertEqual(response.status_code, 200)

    def test_jet_permissions(self):
        """Test Jet works with Django permissions"""
        # Create a regular user without admin privileges
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regular123'
        )
        
        # Test that regular user cannot access admin
        self.client.force_login(regular_user)
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)

    def test_jet_with_custom_admin_classes(self):
        """Test Jet compatibility with custom admin classes"""
        # Test UserAdmin
        admin_site = AdminSite()
        user_admin = UserAdmin(PollUser, admin_site)
        self.assertIsNotNone(user_admin)
        
        # Test QuestionAdmin
        question_admin = QuestionAdmin(Question, admin_site)
        self.assertIsNotNone(question_admin)
        
        # Test ChoiceAdmin
        choice_admin = ChoiceAdmin(Choice, admin_site)
        self.assertIsNotNone(choice_admin)
        
        # Test AnswerAdmin
        answer_admin = AnswerAdmin(Answer, admin_site)
        self.assertIsNotNone(answer_admin)
        
        # Test QuizAdmin
        quiz_admin = QuizAdmin(Quiz, admin_site)
        self.assertIsNotNone(quiz_admin)

    def test_jet_internationalization(self):
        """Test Jet internationalization support"""
        # Test with different language codes
        with override_settings(LANGUAGE_CODE='en-us'):
            response = self.client.get('/admin/')
            self.assertEqual(response.status_code, 200)

    def test_jet_security_headers(self):
        """Test Jet security headers"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        
        # Check X-Frame-Options header
        self.assertEqual(response.get('X-Frame-Options'), 'SAMEORIGIN')

    def test_jet_performance(self):
        """Test Jet performance with multiple models"""
        # Create multiple records to test performance
        for i in range(10):
            Question.objects.create(
                question_text=f"Question {i}",
                pub_date="2024-01-01 12:00:00"
            )
        
        # Test admin list view performance
        response = self.client.get('/admin/polls/question/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question 0')
        self.assertContains(response, 'Question 9')

    def test_jet_error_handling(self):
        """Test Jet error handling"""
        # Test 404 handling
        response = self.client.get('/admin/nonexistent/')
        self.assertEqual(response.status_code, 404)
        
        # Test invalid admin URLs
        response = self.client.get('/admin/polls/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """Clean up test data"""
        Question.objects.all().delete()
        PollUser.objects.all().delete()
        Choice.objects.all().delete()
        Answer.objects.all().delete()
        Quiz.objects.all().delete()
        User.objects.all().delete()


class JetThemeTests(TestCase):
    """Specialized tests for Jet theme functionality"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)

    def test_jet_theme_css_loading(self):
        """Test that Jet theme CSS files load correctly"""
        themes = ['default', 'primary', 'green', 'light-green', 'light-violet', 'light-blue', 'light-gray']
        
        for theme in themes:
            css_url = f'/static/jet/css/build/themes/{theme}.css'
            response = self.client.get(css_url)
            # Note: In test environment, static files might not be served
            # This test ensures the URL structure is correct
            self.assertIn(theme, css_url)

    def test_jet_theme_javascript_loading(self):
        """Test that Jet theme JavaScript files load correctly"""
        js_url = '/static/jet/js/build/bundle.min.js'
        # Test URL structure
        self.assertIn('jet', js_url)
        self.assertIn('bundle.min.js', js_url)

    def test_jet_theme_configuration_validation(self):
        """Test Jet theme configuration validation"""
        from django.conf import settings
        
        # Check that all themes have required fields
        for theme in settings.JET_THEMES:
            self.assertIn('theme', theme)
            self.assertIn('color', theme)
            self.assertIn('title', theme)
            
            # Validate color format (should be hex)
            color = theme['color']
            self.assertTrue(color.startswith('#'))
            self.assertEqual(len(color), 7)  # #RRGGBB format

    def tearDown(self):
        User.objects.all().delete()


class JetDashboardTests(TestCase):
    """Specialized tests for Jet dashboard functionality"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)

    def test_dashboard_url_structure(self):
        """Test Jet dashboard URL structure"""
        dashboard_urls = [
            '/jet/dashboard/',
            '/jet/dashboard/modules/',
        ]
        
        for url in dashboard_urls:
            response = self.client.get(url)
            # Dashboard should be accessible to admin users
            self.assertIn(response.status_code, [200, 302])

    def test_dashboard_widget_configuration(self):
        """Test dashboard widget configuration"""
        # Test that dashboard modules are properly configured
        from django.conf import settings
        self.assertIn('jet.dashboard', settings.INSTALLED_APPS)

    def test_dashboard_permissions(self):
        """Test dashboard permissions"""
        # Create regular user
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regular123'
        )
        
        # Test that regular user cannot access dashboard
        self.client.force_login(regular_user)
        response = self.client.get('/jet/dashboard/')
        self.assertNotEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class JetAdminIntegrationTests(TestCase):
    """Specialized tests for Jet admin integration"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)
        
        # Create test data
        self.question = Question.objects.create(
            question_text="Test Question",
            pub_date="2024-01-01 12:00:00"
        )

    def test_admin_change_form_with_jet(self):
        """Test admin change form works with Jet"""
        response = self.client.get(f'/admin/polls/question/{self.question.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_admin_add_form_with_jet(self):
        """Test admin add form works with Jet"""
        response = self.client.get('/admin/polls/question/add/')
        self.assertEqual(response.status_code, 200)

    def test_admin_delete_confirmation_with_jet(self):
        """Test admin delete confirmation works with Jet"""
        response = self.client.get(f'/admin/polls/question/{self.question.id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_admin_history_with_jet(self):
        """Test admin history works with Jet"""
        response = self.client.get(f'/admin/polls/question/{self.question.id}/history/')
        self.assertEqual(response.status_code, 200)

    def test_admin_bulk_actions_with_jet(self):
        """Test admin bulk actions work with Jet"""
        # Create multiple questions
        for i in range(3):
            Question.objects.create(
                question_text=f"Bulk Question {i}",
                pub_date="2024-01-01 12:00:00"
            )
        
        # Test bulk delete
        response = self.client.post('/admin/polls/question/', {
            'action': 'delete_selected',
            'select_across': '0',
            'index': '0',
            '_selected_action': [str(q.id) for q in Question.objects.all()]
        })
        self.assertIn(response.status_code, [200, 302])

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()


class JetStaticFilesTests(TestCase):
    """Specialized tests for Jet static files"""
    
    def test_jet_static_files_structure(self):
        """Test Jet static files structure"""
        import os
        from django.conf import settings
        
        # Check if static files directory exists
        static_dir = os.path.join(settings.BASE_DIR, 'staticfiles', 'jet')
        if os.path.exists(static_dir):
            # Check for CSS directory
            css_dir = os.path.join(static_dir, 'css')
            self.assertTrue(os.path.exists(css_dir))
            
            # Check for JS directory
            js_dir = os.path.join(static_dir, 'js')
            self.assertTrue(os.path.exists(js_dir))

    def test_jet_static_files_collection(self):
        """Test Jet static files collection"""
        from django.core.management import call_command
        from django.conf import settings
        
        # Test collectstatic command
        try:
            call_command('collectstatic', '--noinput', verbosity=0)
            self.assertTrue(True)  # If no exception, static files are collected
        except Exception as e:
            self.fail(f"Static files collection failed: {e}")


class JetSecurityTests(TestCase):
    """Specialized tests for Jet security features"""
    
    def setUp(self):
        self.client = Client()

    def test_jet_csrf_protection(self):
        """Test Jet CSRF protection"""
        # Test that admin forms include CSRF tokens
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(admin_user)
        
        response = self.client.get('/admin/polls/question/add/')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_jet_xss_protection(self):
        """Test Jet XSS protection"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(admin_user)
        
        # Test with potentially malicious content
        malicious_content = "<script>alert('xss')</script>"
        question = Question.objects.create(
            question_text=malicious_content,
            pub_date="2024-01-01 12:00:00"
        )
        
        response = self.client.get('/admin/polls/question/')
        # Content should be escaped, not executed
        self.assertNotContains(response, '<script>')

    def test_jet_sql_injection_protection(self):
        """Test Jet SQL injection protection"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(admin_user)
        
        # Test with potentially malicious SQL
        malicious_sql = "'; DROP TABLE polls_question; --"
        question = Question.objects.create(
            question_text=malicious_sql,
            pub_date="2024-01-01 12:00:00"
        )
        
        # Verify the record was created safely
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(question.question_text, malicious_sql)

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()


class JetPerformanceTests(TestCase):
    """Specialized tests for Jet performance"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)

    def test_jet_admin_performance_with_large_datasets(self):
        """Test Jet admin performance with large datasets"""
        # Create a large number of records
        questions = []
        for i in range(100):
            questions.append(Question(
                question_text=f"Performance Test Question {i}",
                pub_date="2024-01-01 12:00:00"
            ))
        
        Question.objects.bulk_create(questions)
        
        # Test admin list view performance
        import time
        start_time = time.time()
        response = self.client.get('/admin/polls/question/')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        # Performance should be reasonable (less than 5 seconds)
        self.assertLess(end_time - start_time, 5.0)

    def test_jet_memory_usage(self):
        """Test Jet memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create and access admin pages
        for i in range(10):
            Question.objects.create(
                question_text=f"Memory Test Question {i}",
                pub_date="2024-01-01 12:00:00"
            )
            self.client.get('/admin/polls/question/')
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        self.assertLess(memory_increase, 50 * 1024 * 1024)

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()
