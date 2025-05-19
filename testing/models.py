
from django.test import TestCase
from django.contrib.auth import get_user_model
from hub.models import QuizLevel, QuestionModel, QuizModel, UserProgress, UserResponse

User = get_user_model()

class QuizLevelModelTest(TestCase):
    def test_create_quiz_level(self):
        level = QuizLevel.objects.create(level_number=1)
        self.assertEqual(level.level_number, 1)
    
    def test_quiz_level_str(self):
        level = QuizLevel.objects.create(level_number=5)
        self.assertEqual(str(level), "Level 5")

class QuestionModelTest(TestCase):
    def test_create_question(self):
        question = QuestionModel.objects.create(
            question="What is 2 + 2?",
            option1="3",
            option2="4",
            option3="5",
            option4="6",
            correct_answer="4"
        )
        self.assertEqual(question.correct_answer, "4")
        self.assertEqual(str(question), "level: None  Num: None")  # Since levels and num are null

class UserProgressTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
    
    def test_create_user_progress(self):
        progress = UserProgress.objects.create(user=self.user, current_level=2)
        self.assertEqual(progress.current_level, 2)
        self.assertEqual(str(progress), "testuser - Level 2")
