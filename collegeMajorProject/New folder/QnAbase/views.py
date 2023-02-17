from .qnnna1 import check_similaritys
from .bert_ester import runner
runner()
from .models import Question,Answer,Comment,Upvote,Downvote
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import AnswerForm,QuestionForm
from django.db.models import Count
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from QnA_System import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token
from django.http import JsonResponse
from django.core.mail import EmailMessage


# Create your views here.
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')

    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'home.html',{'quests':quests})

def detail(request,id):
    quest = Question.objects.get(pk=id)
    answers=Answer.objects.filter(question=quest)
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user
            answer.save()
            messages.success(request,'Answer has been submitted.')
    return render(request,'detail.html',{'quest':quest,'answers':answers,'answerform':answerform})

# Save Comment
def save_comment(request):
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        return JsonResponse({'bool':True})

# Save Upvote
def save_upvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Upvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Upvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

# Save Downvote
def save_downvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Downvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Downvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})


def signup(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist. Please try another username")
            return redirect('QnAbase:signup')
        
        if User.objects.filter(email=email):
            messages.error(request,"your email address is already register")
            return redirect('QnAbase:signup')
        
        if len(username)>10:
            messages.error(request,"User name must be less than 10 characters")
        
        if pass1 != pass2:
            messages.error(request,"Password didn't match")
            return redirect('QnAbase:signup')
            
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('QnAbase:signup')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        messages.success(request,"Your account has been successfully created. We have sent you a verification email. Please verify your email in order to activate account")
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Verify your email @ Ayush Blog!"
        message = render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)), 
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        # email.fail_silently = True
        email.send()
        return redirect('QnAbase:signin')

    return render(request, "signup.html")
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username = username, password = pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('/',  name=fname)
        
        else:
            messages.error(request,"Bad credintials!")
            return redirect('QnAbase:signin')
            
    return render(request, "signin.html")
    
def logout_view(request):
    logout(request)
    return redirect('/')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('QnAbase:home')

def live(request):
    if request.method == 'POST':
        q1 =  request.POST['textField1'] 
        q2 =  request.POST['textField2']
        result = check_similaritys(q1,q2)
        messages.success(request,f"Text similiraty Score is : {result} ",extra_tags='alert')

    return render(request, "live.html")
    
def ask_form(request):
    
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            
            ####
            quests=Question.objects.values('title')
            ll=[d['title'] for d in quests]
            print(ll)
            scores='Following DUPLICATE questions are found \t \t \t'

            scores = 0

            for i in range(len(ll)):
                acc=check_similaritys(questForm, ll[i])
                if float(acc)>0.90:
                    # scores+= f"\n {ll[i]} {acc*100 : .2f}% \n"

                    scores+=1
                    if scores==1:   
                        messages.error(request, '---- Following DUPLICATES were found !!! ----')

                    messages.error(request, ll[i] + ' '+ str(int(acc*100)) +'%')

            if scores==0:
                messages.success(request,"Your Question was added SUCCESSFULLY",extra_tags='alert')
        ### Enable this to save new question            
                questForm.save()


            print(scores)

            
            #### Enable this to save new question            
            # questForm.save()

            # if len(scores)>0:
            #     messages.error(request, scores)
       

    return render(request,'ask-question.html',{'form':form})

