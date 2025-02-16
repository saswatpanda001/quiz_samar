from django.contrib import admin
from hub.models import QuizModel, QuestionModel, UserProgress, UserResponse, UserProfile, Badge, QuizBadges
# Register your models here.


admin.site.register(QuizModel)
admin.site.register(QuestionModel)
admin.site.register(UserResponse)
admin.site.register(UserProgress)
admin.site.register(UserProfile)
admin.site.register(Badge)
admin.site.register(QuizBadges)




