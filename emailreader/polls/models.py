from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Category(models.Model):
    """Category model for organizing questions and polls"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model for flexible categorization"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(models.Model):
    """Extended user model for polls application"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
        ('user', 'Regular User'),
        ('guest', 'Guest'),
    ]
    
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(13), MaxValueValidator(120)])
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Question(models.Model):
    """Enhanced question model with more fields for Django Jet demo"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    
    title = models.CharField(max_length=200)
    question_text = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_questions')
    points = models.PositiveIntegerField(default=1)
    time_limit = models.DurationField(null=True, blank=True, help_text='Time limit for answering')
    explanation = models.TextField(blank=True, help_text='Explanation for the correct answer')
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-pub_date', '-created_at']
    
    def __str__(self):
        return self.title


class Choice(models.Model):
    """Enhanced choice model"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    votes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    explanation = models.TextField(blank=True, help_text='Explanation for this choice')
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.title} - {self.choice_text[:50]}"


class Answer(models.Model):
    """Enhanced answer model for quiz responses"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    confidence_level = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    source = models.URLField(blank=True, help_text='Source URL for the answer')
    
    class Meta:
        ordering = ['-is_correct', '-confidence_level']
    
    def __str__(self):
        return f"{self.question.title} - {self.answer_text[:50]}"


class Quiz(models.Model):
    """Enhanced quiz model with comprehensive tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    is_correct = models.BooleanField(default=False)
    time_spent = models.DurationField(null=True, blank=True)
    score_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feedback = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-started_at']
        unique_together = ['question', 'user', 'started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.title} - {self.status}"


class Poll(models.Model):
    """New poll model for showcasing more Django Jet features"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_polls')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    allow_multiple_choices = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=True)
    max_votes_per_user = models.PositiveIntegerField(default=1)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    total_votes = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class PollOption(models.Model):
    """Poll option model"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['poll', 'order']
    
    def __str__(self):
        return f"{self.poll.title} - {self.option_text}"


class PollVote(models.Model):
    """Poll vote tracking model"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='vote_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_votes', null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-voted_at']
        unique_together = ['poll', 'user'] if 'user' else ['poll', 'ip_address']
    
    def __str__(self):
        user_info = self.user.username if self.user else self.ip_address
        return f"{user_info} voted for {self.option.option_text}"


class Analytics(models.Model):
    """Analytics model for dashboard data"""
    date = models.DateField()
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', 'metric_name']
        unique_together = ['date', 'metric_name', 'category']
    
    def __str__(self):
        return f"{self.date} - {self.metric_name}: {self.metric_value}"
