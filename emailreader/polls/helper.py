

from polls.models import User, Question, Choice, Answer, Quiz

for i in range(1000):
    User.objects.create(username=f'User {i}', email=f'user{i}@example.com', password='password')
    Question.objects.create(question_text=f'Question {i}', pub_date='2020-01-01 00:00:00')
    Choice.objects.create(question_id=1, choice_text=f'Choice {i}', votes=0)
    Answer.objects.create(question_id=1, answer_text=f'Answer {i}', is_correct=False)
    Quiz.objects.create(question_id=1, answer_id=1, user_id=1, is_correct=False)