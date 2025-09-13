"""
Management command to create sample data for Django Jet demo
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
import random
from decimal import Decimal

from polls.models import (
    Category, Tag, User, Question, Choice, Answer, Quiz,
    Poll, PollOption, PollVote, Analytics
)


class Command(BaseCommand):
    help = 'Create sample data for Django Jet demo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new sample data',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)',
        )
        parser.add_argument(
            '--questions',
            type=int,
            default=100,
            help='Number of questions to create (default: 100)',
        )
        parser.add_argument(
            '--polls',
            type=int,
            default=30,
            help='Number of polls to create (default: 30)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Creating sample data...')

        self.stdout.write('Creating super user...')
        self.create_super_user()
        self.stdout.write('   ✅ Created super user')
        
        # Create categories and tags first
        self.stdout.write('📁 Creating categories...')
        categories = self.create_categories()
        self.stdout.write(f'   ✅ Created {len(categories)} categories')
        
        self.stdout.write('🏷️  Creating tags...')
        tags = self.create_tags()
        self.stdout.write(f'   ✅ Created {len(tags)} tags')
        
        # Create users
        self.stdout.write(f'👥 Creating {options["users"]} users...')
        users = self.create_users(options['users'])
        self.stdout.write(f'   ✅ Created {len(users)} users')
        
        # Create questions
        self.stdout.write(f'❓ Creating {options["questions"]} questions...')
        questions = self.create_questions(options['questions'], categories, tags, users)
        self.stdout.write(f'   ✅ Created {len(questions)} questions')
        
        # Create choices for questions
        self.stdout.write('🔘 Creating choices for questions...')
        self.create_choices(questions)
        self.stdout.write(f'   ✅ Created choices for {len(questions)} questions')
        
        # Create answers
        self.stdout.write('💬 Creating answers...')
        self.create_answers(questions)
        self.stdout.write(f'   ✅ Created answers for {len(questions)} questions')
        
        # Create polls
        self.stdout.write(f'📊 Creating {options["polls"]} polls...')
        polls = self.create_polls(options['polls'], categories, tags, users)
        self.stdout.write(f'   ✅ Created {len(polls)} polls')
        
        # Create poll options
        self.stdout.write('📋 Creating poll options...')
        self.create_poll_options(polls)
        self.stdout.write(f'   ✅ Created options for {len(polls)} polls')
        
        # Create quiz attempts
        self.stdout.write('🎯 Creating quiz attempts...')
        self.create_quiz_attempts(users, questions)
        self.stdout.write('   ✅ Created quiz attempts')
        
        # Create poll votes
        self.stdout.write('🗳️  Creating poll votes...')
        self.create_poll_votes(users, polls)
        self.stdout.write('   ✅ Created poll votes')
        
        # Create analytics data
        self.stdout.write('📈 Creating analytics data...')
        self.create_analytics_data()
        self.stdout.write('   ✅ Created analytics data')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Successfully created sample data:\n'
                f'   • {len(users)} users\n'
                f'   • {len(questions)} questions\n'
                f'   • {len(polls)} polls\n'
                f'   • {len(categories)} categories\n'
                f'   • {len(tags)} tags'
            )
        )

    def clear_data(self):
        """Clear all existing data"""
        Analytics.objects.all().delete()
        PollVote.objects.all().delete()
        PollOption.objects.all().delete()
        Poll.objects.all().delete()
        Quiz.objects.all().delete()
        Answer.objects.all().delete()
        Choice.objects.all().delete()
        Question.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

    def create_super_user(self):
        """Create sample super user"""
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='1234'
        )

    def create_categories(self):
        """Create sample categories"""
        categories_data = [
            {'name': 'General Knowledge', 'description': 'General knowledge questions', 'color': '#007bff'},
            {'name': 'Science', 'description': 'Science and technology questions', 'color': '#28a745'},
            {'name': 'History', 'description': 'Historical questions', 'color': '#dc3545'},
            {'name': 'Sports', 'description': 'Sports and athletics', 'color': '#ffc107'},
            {'name': 'Entertainment', 'description': 'Movies, music, and entertainment', 'color': '#17a2b8'},
            {'name': 'Geography', 'description': 'World geography questions', 'color': '#6f42c1'},
            {'name': 'Literature', 'description': 'Books and literature', 'color': '#e83e8c'},
            {'name': 'Technology', 'description': 'Technology and programming', 'color': '#20c997'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color'],
                    'is_active': True,
                }
            )
            categories.append(category)
            
        return categories

    def create_tags(self):
        """Create sample tags"""
        tags_data = [
            'beginner', 'intermediate', 'advanced', 'easy', 'hard',
            'popular', 'trending', 'educational', 'fun', 'challenging',
            'multiple-choice', 'true-false', 'open-ended', 'timed',
            'featured', 'community', 'expert', 'quiz', 'test'
        ]
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={
                    'slug': f"{tag_name.replace(' ', '-')}-{random.randint(100, 999)}",
                    'description': f'Tag for {tag_name} content',
                    'usage_count': 0,
                }
            )
            tags.append(tag)
            
        return tags

    def create_users(self, count):
        """Create sample users"""
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica',
            'William', 'Ashley', 'James', 'Amanda', 'Christopher', 'Jennifer', 'Daniel',
            'Lisa', 'Matthew', 'Nancy', 'Anthony', 'Karen', 'Mark', 'Betty', 'Donald',
            'Helen', 'Steven', 'Sandra', 'Paul', 'Donna', 'Andrew', 'Carol', 'Joshua'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'
        ]
        
        roles = ['admin', 'moderator', 'user', 'guest']
        genders = ['M', 'F', 'O', 'P']
        
        users = []
        for i in range(count):
            if i % 10 == 0:  # Log every 10 users
                self.stdout.write(f'   Creating user {i+1}/{count}...')
            
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}{last_name.lower()}{i}{random.randint(100, 999)}"
            
            user = User.objects.create(
                username=username,
                email=f"{username}@example.com",
                password='pbkdf2_sha256$test$test',
                first_name=first_name,
                last_name=last_name,
                gender=random.choice(genders),
                role=random.choice(roles),
                age=random.randint(18, 65),
                bio=f"This is a sample bio for {first_name} {last_name}",
                is_verified=random.choice([True, False]),
                is_premium=random.choice([True, False]),
                score=Decimal(str(round(random.uniform(0, 1000), 2))),
                last_login=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            users.append(user)
            
        return users

    def create_questions(self, count, categories, tags, users):
        """Create sample questions"""
        question_templates = [
            "What is the capital of {}?",
            "Who wrote the book {}?",
            "In which year did {} happen?",
            "What is the chemical symbol for {}?",
            "Which country is known for {}?",
            "What is the largest planet in our solar system?",
            "Who invented the telephone?",
            "What is the speed of light?",
            "Which programming language is known for its simplicity?",
            "What is the largest ocean on Earth?",
            "Who painted the Mona Lisa?",
            "What is the currency of Japan?",
            "Which sport uses a shuttlecock?",
            "What is the largest mammal?",
            "Who wrote Romeo and Juliet?",
        ]
        
        difficulties = ['easy', 'medium', 'hard', 'expert']
        statuses = ['draft', 'published', 'archived']
        
        questions = []
        for i in range(count):
            if i % 20 == 0:  # Log every 20 questions
                self.stdout.write(f'   Creating question {i+1}/{count}...')
            
            template = random.choice(question_templates)
            if '{}' in template:
                question_text = template.format(f"Item {i}")
            else:
                question_text = template
                
            question = Question.objects.create(
                title=f"Sample Question {i+1}",
                question_text=question_text,
                slug=f"sample-question-{i+1}-{random.randint(1000, 9999)}",
                category=random.choice(categories),
                difficulty=random.choice(difficulties),
                status=random.choice(statuses),
                author=random.choice(users),
                points=random.randint(1, 100),
                time_limit=timedelta(minutes=random.randint(1, 10)),
                explanation=f"Explanation for question {i+1}",
                image=None,  # No image for sample data
                is_featured=random.choice([True, False]),
                view_count=random.randint(0, 1000),
                like_count=random.randint(0, 1000),
                pub_date=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            
            # Add tags to question
            question.tags.set(random.sample(tags, random.randint(1, 3)))
            questions.append(question)
            
        return questions

    def create_choices(self, questions):
        """Create sample choices for questions"""
        for question in questions:
            num_choices = random.randint(2, 5)
            correct_choice = random.randint(0, num_choices - 1)
            
            for i in range(num_choices):
                Choice.objects.create(
                    question=question,
                    choice_text=f"Choice {i+1} for {question.title}",
                    is_correct=(i == correct_choice),
                    votes=random.randint(0, 100),
                    order=i,
                    explanation=f"Explanation for choice {i+1}",
                )

    def create_answers(self, questions):
        """Create sample answers for questions"""
        for question in questions:
            Answer.objects.create(
                question=question,
                answer_text=f"Sample answer for {question.title}",
                is_correct=random.choice([True, False]),
                confidence_level=round(random.uniform(0.0, 1.0), 2),
                source=f"https://example.com/source/{question.id}",
            )

    def create_polls(self, count, categories, tags, users):
        """Create sample polls"""
        poll_templates = [
            "What is your favorite {}?",
            "Which {} do you prefer?",
            "How often do you {}?",
            "What do you think about {}?",
            "Which is better: {} or {}?",
            "Do you like {}?",
            "What's your opinion on {}?",
            "How important is {} to you?",
        ]
        
        statuses = ['draft', 'active', 'closed', 'archived']
        
        polls = []
        for i in range(count):
            if i % 10 == 0:  # Log every 10 polls
                self.stdout.write(f'   Creating poll {i+1}/{count}...')
            
            template = random.choice(poll_templates)
            if '{}' in template:
                # Count the number of placeholders and provide appropriate arguments
                placeholder_count = template.count('{}')
                if placeholder_count == 1:
                    poll_text = template.format(f"item {i}")
                elif placeholder_count == 2:
                    poll_text = template.format(f"option A {i}", f"option B {i}")
                else:
                    # For any other number of placeholders, use generic items
                    args = [f"item {i}_{j}" for j in range(placeholder_count)]
                    poll_text = template.format(*args)
            else:
                poll_text = template
                
            poll = Poll.objects.create(
                title=f"Sample Poll {i+1}",
                description=f"Description for poll {i+1}: {poll_text}",
                category=random.choice(categories),
                status=random.choice(statuses),
                author=random.choice(users),
                allow_multiple_choices=random.choice([True, False]),
                is_anonymous=random.choice([True, False]),
                max_votes_per_user=random.randint(1, 3),
                start_date=timezone.now() - timedelta(days=random.randint(0, 30)),
                end_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                is_featured=random.choice([True, False]),
            )
            
            # Add tags to poll
            poll.tags.set(random.sample(tags, random.randint(1, 3)))
            polls.append(poll)
            
        return polls

    def create_poll_options(self, polls):
        """Create sample poll options"""
        for poll in polls:
            num_options = random.randint(2, 6)
            
            for i in range(num_options):
                PollOption.objects.create(
                    poll=poll,
                    option_text=f"Option {i+1} for {poll.title}",
                    votes=random.randint(0, 50),
                    order=i,
                    description=f"Description for option {i+1}",
                )

    def create_quiz_attempts(self, users, questions):
        """Create sample quiz attempts"""
        statuses = ['pending', 'in_progress', 'completed', 'abandoned']
        
        total_attempts = 0
        for i, user in enumerate(users):
            if i % 10 == 0:  # Log every 10 users
                self.stdout.write(f'   Creating quiz attempts for user {i+1}/{len(users)}...')
            
            # Each user attempts 5-15 random questions
            num_attempts = random.randint(5, 15)
            user_questions = random.sample(questions, min(num_attempts, len(questions)))
            
            for question in user_questions:
                choices = list(question.choices.all())
                if choices:
                    selected_choice = random.choice(choices)
                    is_correct = selected_choice.is_correct
                else:
                    selected_choice = None
                    is_correct = random.choice([True, False])
                
                Quiz.objects.create(
                    question=question,
                    selected_choice=selected_choice,
                    user=user,
                    status=random.choice(statuses),
                    is_correct=is_correct,
                    time_spent=timedelta(seconds=random.randint(30, 300)),
                    score_earned=Decimal(str(round(random.uniform(0, question.points), 2))),
                    feedback=f"Feedback for {user.username} on {question.title}",
                    ip_address=f"192.168.1.{random.randint(1, 254)}",
                    user_agent=f"Mozilla/5.0 (Sample Browser) {random.randint(1, 100)}",
                    completed_at=timezone.now() - timedelta(days=random.randint(0, 7)),
                )
                total_attempts += 1

    def create_poll_votes(self, users, polls):
        """Create sample poll votes"""
        total_votes = 0
        for i, poll in enumerate(polls):
            if i % 10 == 0:  # Log every 10 polls
                self.stdout.write(f'   Creating votes for poll {i+1}/{len(polls)}...')
            
            poll_options = list(poll.options.all())
            if not poll_options:
                continue
                
            # Generate 10-50 votes per poll, but ensure each user votes at most once
            num_votes = random.randint(10, min(50, len(users)))
            
            # Randomly select users who will vote (each user votes at most once)
            voting_users = random.sample(users, num_votes) if not poll.is_anonymous else [None] * num_votes
            
            for j in range(num_votes):
                option = random.choice(poll_options)
                user = voting_users[j] if not poll.is_anonymous else None
                
                PollVote.objects.create(
                    poll=poll,
                    option=option,
                    user=user,
                    ip_address=f"192.168.1.{random.randint(1, 254)}",
                    user_agent=f"Mozilla/5.0 (Sample Browser) {random.randint(1, 100)}",
                    voted_at=timezone.now() - timedelta(days=random.randint(0, 30)),
                )
                
                # Update option vote count
                option.votes += 1
                option.save()
                total_votes += 1
            
            # Update poll total votes
            poll.total_votes = num_votes
            poll.save()

    def create_analytics_data(self):
        """Create sample analytics data"""
        metrics = [
            'page_views', 'user_registrations', 'quiz_attempts', 'poll_votes',
            'questions_created', 'polls_created', 'user_logins', 'avg_session_time'
        ]
        
        categories = ['users', 'content', 'engagement', 'performance']
        
        # Create analytics data for the last 30 days
        total_analytics = 0
        for i in range(30):
            if i % 10 == 0:  # Log every 10 days
                self.stdout.write(f'   Creating analytics for day {i+1}/30...')
            
            date = timezone.now().date() - timedelta(days=i)
            
            for metric in metrics:
                category = random.choice(categories)
                value = random.randint(1, 1000)
                
                Analytics.objects.create(
                    date=date,
                    metric_name=metric,
                    metric_value=Decimal(str(value)),
                    category=category,
                    metadata={
                        'source': 'sample_data',
                        'generated_at': timezone.now().isoformat(),
                    }
                )
                total_analytics += 1