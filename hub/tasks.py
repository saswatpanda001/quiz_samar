# hub/tasks.py
from celery import shared_task
from django.db.models import F
from .models import QuizModel

@shared_task
def increment_counter(quiz_id):
    try:
        obj = QuizModel.objects.filter(quiz_id=quiz_id)[0]  # Adjust the query as needed

        if obj.total_time < 7200:
            QuizModel.objects.filter(quiz_id=quiz_id).update(total_time=F('total_time') + 1)
            print(quiz_id,obj.total_time)
        else:
            # Optionally log that the limit has been reached
            print("Counter reached 7200. No further increment.")
    except QuizModel.DoesNotExist:
        print("QuizModel instance not found.")
