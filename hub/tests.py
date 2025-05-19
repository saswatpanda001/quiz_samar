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


from django.test import TestCase
from django.urls import reverse

class ViewTests(TestCase):
    def test_landing_page(self):
        response = self.client.get(reverse("hub:landing"))
        self.assertEqual(response.status_code, 200)  # Should return HTTP 200 OK


from django.test import SimpleTestCase
from django.urls import resolve, reverse
from hub.views import landing, quiz

class URLTests(SimpleTestCase):
    def test_landing_url(self):
        url = reverse("hub:landing")
        self.assertEqual(resolve(url).func, landing)

    def test_quiz_url(self):
        url = reverse("hub:quiz", args=["1234-5678", 1, 1])
        self.assertEqual(resolve(url).func, quiz)


from django.test import TestCase
from .models import QuizLevel

class QuizLevelModelTest(TestCase):
    def setUp(self):
        self.level = QuizLevel.objects.create(level_number=1)

    def test_string_representation(self):
        self.assertEqual(str(self.level), "Level 1")




from django.test import TestCase
from .models import QuestionModel

class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = QuestionModel.objects.create(
            question="What is the capital of France?",
            option1="Paris",
            option2="London",
            option3="Berlin",
            option4="Madrid",
            levels=1,
            num=1,
            correct_option="option1",
            correct_answer="Paris"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.question), "level: 1  Num: 1")


from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProgress

User = get_user_model()

class UserProgressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.progress = UserProgress.objects.create(user=self.user, current_level=2)

    def test_string_representation(self):
        self.assertEqual(str(self.progress), "testuser - Level 2")



from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import QuizModel

User = get_user_model()

class QuizModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.quiz = QuizModel.objects.create(user=self.user)

    def test_quiz_id_generation(self):
        self.assertIsNotNone(self.quiz.quiz_id)
        self.assertEqual(len(self.quiz.quiz_id), 36)  # UUID length


from django.test import TestCase
from .models import Badge

class BadgeModelTest(TestCase):
    def setUp(self):
        self.badge = Badge.objects.create(name="Achiever")

    def test_string_representation(self):
        self.assertEqual(str(self.badge), "Achiever")


from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import QuestionModel, QuizModel, UserResponse

User = get_user_model()

class UserResponseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.quiz = QuizModel.objects.create(user=self.user)
        self.question = QuestionModel.objects.create(
            question="What is 2+2?",
            option1="3",
            option2="4",
            option3="5",
            option4="6",
            levels=1,
            num=1,
            correct_option="option2",
            correct_answer="4"
        )
        self.response = UserResponse.objects.create(
            user=self.user,
            quiz=self.quiz,
            question=self.question,
            selected_option=2,
            status="correct"
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.response),
            f"{self.user.username} - {self.question} ({self.response.status})"
        )


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import QuizLevel

User = get_user_model()

class QuizViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.level = QuizLevel.objects.create(level_number=1)

    def test_dashboard_view(self):
        response = self.client.get(reverse("hub:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_quiz_view(self):
        response = self.client.get(reverse("hub:quiz", args=[self.level.level_number, 1, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "error.html")
