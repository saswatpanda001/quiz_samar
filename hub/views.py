import requests
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from hub.models import QuizModel, UserProfile, QuestionModel, UserResponse, QuizBadges, Badge
from hub.forms import UserProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hub.tasks import increment_counter
from django.utils import timezone
import uuid 

@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    quiz_data = QuizModel.objects.filter(user=request.user)
    badge_data = QuizBadges.objects.filter(user=request.user)
    print(badge_data)
    avg_score = 0
    for each in quiz_data:
        avg_score+=each.total_score
    if len(quiz_data)>0:
        avg_score/=len(quiz_data)
    else:
        avg_score = 0

    data =  {'profile': profile,'quiz_data':quiz_data,"total_quiz":len(quiz_data),'badge_data':badge_data,'total_badge':len(badge_data),'avg_score':avg_score}
    return render(request, 'profile.html', data)



@login_required
def profile_view_others(request,id):
    profile = UserProfile.objects.get(user__id=id)
    quiz_data = QuizModel.objects.filter(user__id=id)
    badge_data = QuizBadges.objects.filter(user__id=id)
    print(badge_data)
    avg_score = 0
    for each in quiz_data:
        avg_score+=each.total_score
    if len(quiz_data)>0:
        avg_score/=len(quiz_data)
    else:
        avg_score = 0
    

    data =  {'profile': profile,'quiz_data':quiz_data,"total_quiz":len(quiz_data),'badge_data':badge_data,'total_badge':len(badge_data),'avg_score':avg_score}
    return render(request, 'profile_others.html', data)




@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('hub:profile_view')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def level_completed(request,quiz_idd,level):
    quiz_data = QuizModel.objects.filter(quiz_id=quiz_idd)
    if len(quiz_data)==0 or level<=0 or level>50:
        return render(request,"error.html")
    else:
        quiz_data=  quiz_data[0]
        resp_data = UserResponse.objects.filter(quiz=quiz_data).filter(question__levels=level)
    
        print("resp_len: ",len(resp_data))
        skipped,correct,incorrect,score =0,0,0,0
        for each in resp_data:
            if each.status=="correct":
                score+=4
                correct+=1
            if each.status=="incorrect":
                incorrect+=1
            if each.status=="skipped":
                skipped+=1
            
        data = {"total_time":quiz_data.total_time,"skipped":skipped,"correct":correct,"incorrect":incorrect,"score":score,"level":level,"quiz_id":quiz_idd,"next_level":level+1}
        return render(request, "level_complete.html",data)


@csrf_exempt
@login_required
def quiz_completed(request,quiz_idd,level):
        quiz_data = QuizModel.objects.filter(quiz_id=quiz_idd)
        if len(quiz_data)==0 or level<=0 or level>50:
            print("complete:",request.body)
            return render(request,"error.html")
        else:
            quiz_data=  quiz_data[0]
            data = {"quiz_data":quiz_data}

            quiz_data.status = "completed"
            quiz_data.time_submit=timezone.now()
            
            end_level = quiz_data.current_level
            if quiz_data.current_question==1:
                if end_level>1:
                    end_level-=1
            
            quiz_data.level_end = end_level
            print("end_level: ",end_level)
            quiz_data.save()

            user_data = UserProfile.objects.filter(user=request.user)[0]
            if user_data.top_score<quiz_data.total_score:
                user_data.top_score_quiz = quiz_data
                user_data.top_score = quiz_data.total_score
                user_data.save()
            
            if quiz_data.total_score>=1400 and quiz_data.total_score<1600:
                bdg = QuizBadges.objects.create(
                    badge=Badge.objects.filter(name="Bronze")[0],
                    user = request.user,
                    quiz = quiz_data
                )
                bdg.save()
            elif quiz_data.total_score<=1600 and quiz_data.total_score<1800:
                bdg = QuizBadges.objects.create(
                    badge=Badge.objects.filter(name="Silver")[0],
                    user = request.user,
                    quiz = quiz_data
                )
                bdg.save()
            elif quiz_data.total_score>=1800:
                bdg = QuizBadges.objects.create(
                    badge=Badge.objects.filter(name="Gold")[0],
                    user = request.user,
                    quiz = quiz_data
                )
                bdg.save()
            
            
            
            

            


          
            return render(request, "quiz_complete.html",data)



@login_required
def quiz_details(request,quiz_idd):
    quiz_data = QuizModel.objects.filter(quiz_id=quiz_idd)
    if len(quiz_data)==0:
        return render(request,"error.html")
    else:
        quiz_data = quiz_data[0]
        if quiz_data.user != request.user:
            return render(request,"error.html")
        else:
            response_data = UserResponse.objects.filter(quiz=quiz_data)
            data = {"response_data":response_data,"quiz_data":quiz_data}
            return render(request,"quiz_details.html",data)


@csrf_exempt
@login_required(login_url='/accounts/login')
def quiz(request,quiz_idd,level,ques):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
       
        
        # Extract values from the JSON payload.
        qid = str(data.get("qid"))
        level = int(data.get("level"))
        qno = int(data.get("qno"))

        if level==50:
            if qno==10:
                return redirect(f"/quiz/{qiz}/{level}/complete")
            else:
                ques+=1
                return redirect(f"/quiz/{qid}/{level}/{ques}")
        else:
            if qno==10:
                level+=1
                return redirect(f"/quiz/{qid}/{level}/1")
            else:
                ques+=1
                print("yes_conf")
                return redirect(f"/quiz/{qid}/{level}/7")
        
        return JsonResponse({"data":"success"})

    quiz_data = QuizModel.objects.filter(quiz_id=quiz_idd)
    if(len(quiz_data))>=1 and level>=1 and level<=50:
        quiz_data = quiz_data[0]
        if quiz_data.current_level==level and quiz_data.current_question==ques and quiz_data.status!="completed":
            if level==50:
                if ques==10:
                    print("test completed")
            else:
                if ques==10:
                    print("level completed")


            ques_data = QuestionModel.objects.filter(levels=level).filter(num=ques)
            
            if len(ques_data)>=1:
                ques_data = ques_data[0]
                data = {"ques_data":ques_data, "quiz_data":quiz_data}

                return render(request, "quiz.html",data) 
            
            else:
                return render(request,"error.html")

            
            
            
        else:
            
            if quiz_data:
                print("yes")
                if quiz_data.status=="started":
                    return redirect("hub:quiz", quiz_idd=quiz_data.quiz_id, level=quiz_data.current_level, ques=quiz_data.current_question)
                elif quiz_data.status=="completed":
                    return redirect("hub:quiz_comp", quiz_idd=quiz_data.quiz_id, level=quiz_data.current_level)
                    
            
            return render(request,"error.html")

    else:
        return render(request,"error.html")




    


@login_required(login_url='/accounts/login')
def leaderboard(request):
    data = UserProfile.objects.all()
    leader_data = []

    n=1
    for each in data:
        leader_data.append([each,n])
        n+=1

    leader_data.sort(key=lambda x:x[0].top_score, reverse=True)
    
    data = {"leader_data":leader_data}
    return render(request, "leaderboard.html",data)



@login_required
def levels(request):
    
    if request.method=="POST":
        logged_in_user = request.user
        start_level = request.POST.get('level')
       
       
        quiz_data = QuizModel.objects.create(user=logged_in_user)
        quiz_data.quiz_id = str(uuid.uuid4())
        quiz_data.level_start = start_level
        quiz_data.current_level = start_level
        quiz_data.current_question = 1
        quiz_data.time_remaining = 30
        quiz_data.total_time = 0
        quiz_data.save()

        return redirect(reverse("hub:quiz", args=[quiz_data.quiz_id,start_level,1]))

    return render(request, "levels.html")


@login_required(login_url='/accounts/login')
def rules(request):
    return render(request, "rules.html")




@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, "dashboard.html")


def landing(request):
    return render(request, "landing.html")


def get_quiz_data(request, level):
    url = f"https://api-ghz-v2.azurewebsites.net/api/v2/quiz?level={level}"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)



@login_required(login_url='/accounts/login')
def quiz1(request):
    return render(request, "quiz1.html")


def login(request):
    return render(request, "login.html")





@csrf_exempt  # For simplicity; in production, handle CSRF tokens properly.
def update_quiz_data(request):
    if request.method == "POST":
        try:
            new_level=0
            new_ques=0
            data = json.loads(request.body)
            print(data)
            status = data.get("status")
            score = data.get("score")
            qid = data.get("qid")
            qlevel=int(data.get("qlevel"))
            qno = int(data.get("qno"))
            time = data.get("totalTimeSpend")
            selected_option = data.get("selectedOption")
            if selected_option=="none":
                selected_option=0
            


            

            
            quiz_data = QuizModel.objects.filter(quiz_id=qid)[0]
            if status=="correct":
                quiz_data.total_correct+=1
                quiz_data.total_score+=4
            if status=="incorrect":
                quiz_data.total_incorrect+=1
            if status=="skipped":
                quiz_data.total_skipped+=1
            
            print("trying to update current ques and levels")
            if qlevel==50:
                if qno==10:
                    pass
                else:
                    quiz_data.current_question+=1
            else:
                if qno==10:
                    quiz_data.current_level+=1
                    quiz_data.current_question=1
                else:
                    quiz_data.current_question+=1

            quiz_data.total_time = time
            
           
            quiz_data.save()

            resp = UserResponse.objects.create(
                user = request.user,
                quiz = quiz_data,
                question = QuestionModel.objects.filter(levels=int(qlevel)).filter(num=int(qno))[0],
                selected_option = selected_option,
                status = status
            )
            resp.save()
            




            return JsonResponse({
                "message": "Data received successfully.",
                "new_level": quiz_data.current_level,
                "new_ques": quiz_data.current_question
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

