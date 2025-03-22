from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from userapp.models import *
from adminapp.models import *
from django.contrib import messages
from django.core.mail import send_mail
import os
# import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.paginator import Paginator



def index(request):
    t_users = User.objects.all()
    a_users = User.objects.filter(status="Accepted")
    p_users = User.objects.filter(status="Pending")
    context ={
        't_users':len(t_users),
        'a_users':len(a_users),
        'p_users':len(p_users),

    }
    return render(request,'admin/index.html',context)







def all_users(request):
    user = User.objects.filter(status="Accepted")
    context = {
        'user':user,
    }
    return render(request,'admin/all-users.html',context)










from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest

def upload_dataset(request):
    if request.method == 'POST':
        messages.success(request,"image Uploaded successfully !")
        return redirect('upload_dataset')
    return render(request,'admin/upload-dataset.html')



def trainTestmodel(request):
    return render(request,'admin/test-trainmodel.html')




# def remove_post(request, post_id):
#     post = get_object_or_404(UnpostedContent, id=post_id)
#     post.delete()
#     messages.success(request, "The post has been successfully removed.")
#     return redirect('latest_posts')

from django.db.models import Count



def change_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.status == 'Hold':
        user.status = 'Accepted'
    else:
        user.status = 'Hold'
    user.save()
    messages.success(request, f"User {user.full_name} status has been changed to {user.status}.")
    return redirect('users_hate')













def nb(request):
    if not bert_model.objects.exists():
        bert_model.objects.create(model_accuracy='96.0')
    request.session['bert_accuracy'] = bert_model.objects.first().model_accuracy
    bert_accuracy = None
    if request.method == 'POST':
        bert_accuracy = bert_model.objects.first().model_accuracy
        return render(request, 'admin/mb.html',{'bert_accuracy':bert_accuracy})
    return render(request, 'admin/mb.html')













from django.conf import settings
import secrets
import string


def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def pending_users(request):
    user = User.objects.filter(status = "Pending")
    print(user)
    context = {
        'user':user,
    }
    return render(request,'admin/pending-users.html',context)

def accept_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.status = 'Accepted'
    user.save()
    messages.success(request,"user is Accepted")
    return redirect('pending_users')

def reject_user(request,user_id):
    user = User.objects.get(pk = user_id)
    user.delete()
    messages.success(request,"user is rejected")
    return redirect('pending_users')



def delete_user(request,user_id):
    user = User.objects.get(pk = user_id)
    user.delete()
    messages.warning(request,"user is Deleted")
    return redirect('all_users')


def graph(request):
    bert_accuracy = bert_model.objects.first()

    bert_accuracy = bert_accuracy.model_accuracy if bert_accuracy else 'N/A'


    context = {
        'bert_accuracy': bert_accuracy,
    }
    return render(request, 'admin/graph.html', context)





def view_feedbacks(request):
    feedbacks_list = UserFeedback.objects.all()
    paginator = Paginator(feedbacks_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'admin/view-feedbacks.html', {'page_obj': page_obj})


def remove_feedback(request, feedback_id):
    feedback = UserFeedback.objects.get(pk=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback removed successfully.')
    return redirect('view_feedbacks')





def feedbacks_graph(request):
    rating_counts = {
        'rating1': UserFeedback.objects.filter(rating=1).count(),
        'rating2': UserFeedback.objects.filter(rating=2).count(),
        'rating3': UserFeedback.objects.filter(rating=3).count(),
        'rating4': UserFeedback.objects.filter(rating=4).count(),
        'rating5': UserFeedback.objects.filter(rating=5).count(),
    }
    return render(request,"admin/feedback-graph.html", {'rating_counts': rating_counts})

