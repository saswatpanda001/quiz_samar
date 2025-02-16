from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

import uuid


User = get_user_model()

        

class QuizLevel(models.Model):
    level_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Level {self.level_number}"



class QuestionModel(models.Model):
    question = models.CharField(max_length=1000, blank=True, null=True);
    option1 = models.CharField(max_length=1000, blank=True, null=True);
    option2 = models.CharField(max_length=1000, blank=True, null=True);
    option3 = models.CharField(max_length=1000, blank=True, null=True);
    option4 = models.CharField(max_length=1000, blank=True, null=True);
    levels = models.IntegerField(blank=True,null=True);
    num = models.IntegerField(blank=True,null=True);
    correct_option = models.CharField(max_length=500, blank=True, null=True);
    correct_answer = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return f"level: {self.levels}  Num: {self.num}"

    




    
    



class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    current_level = models.IntegerField(default=1,blank=True, null=True)
    last_question = models.IntegerField(default=0,blank=True, null=True)
    time_remaining = models.IntegerField(default=0,blank=True, null=True)
    total_time = models.IntegerField(default=0,blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - Level {self.current_level}"


class QuizModel(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    level_start = models.IntegerField(blank=True,null=True)
    level_end = models.IntegerField(blank=True,null=True)
    quiz_id = models.CharField(max_length=100, editable=False, unique=True)
    
    
    time_started = models.DateTimeField(default=timezone.now,blank=True, null=True)
    time_submit = models.DateTimeField(default=timezone.now, blank=True, null=True)

    total_score = models.IntegerField(default=0,blank=True, null=True)
    total_skipped = models.IntegerField(default=0,blank=True, null=True)
    total_correct = models.IntegerField(default=0,blank=True, null=True)
    total_incorrect = models.IntegerField(default=0,blank=True, null=True)
    total_unattempted = models.IntegerField(default=0,blank=True, null=True)


    current_level = models.IntegerField(default=1,blank=True, null=True)
    current_question = models.IntegerField(default=0,blank=True, null=True)
    time_remaining = models.IntegerField(default=0,blank=True, null=True)
    total_time = models.IntegerField(default=0,blank=True, null=True)
    status = models.CharField(max_length=100,default="started",blank=True, null=True)




    def save(self, *args, **kwargs):

        if not self.quiz_id:
            self.quiz_id = str(uuid.uuid4())
        
        # Call the original save() method to save to the database
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} - Quiz_Id: {self.quiz_id}"


class Badge(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    pic =  models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name


class QuizBadges(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE,blank=True, null=True)

    
    def __str__(self):
        return self.badge.name





class UserResponse(models.Model):
    STATUS_CHOICES = [
        ("skipped", "skipped"),
        ("correct", "correct"),
        ("incorrect", "incorrect"),
        ("notattempted", "notattempted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE,blank=True, null=True) 
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE,blank=True, null=True)
    selected_option = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="notattempted",blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.question} ({self.status})"




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    top_score_quiz = models.OneToOneField(QuizModel, on_delete=models.CASCADE, blank=True,null=True)
    top_score = models.IntegerField(default=0,blank=True,null=True)

    
    def __str__(self):
        return self.user.username