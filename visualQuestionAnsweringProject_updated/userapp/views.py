from django.shortcuts import render,redirect
from django.contrib import messages
import urllib.request
import urllib.parse
from django.contrib.auth import logout
from django.core.mail import send_mail
import os
import random
from django.conf import settings
from userapp.models import *
from adminapp.models import *
from django.utils.datastructures import MultiValueDictKeyError

import warnings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
from django.http import HttpResponse
from PIL import Image
import base64





def user_logout(request):
    logout(request)
    messages.info(request, "Logout Successfully ")
    return redirect("user_login")

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')



def generate_otp(length=4):
    otp = "".join(random.choices("0123456789", k=length))
    return otp



def index(request):
    return render(request,"user/index.html")





def about(request):
    return render(request,"user/about.html")



def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            if user.password != password:
                messages.error(request, "Incorrect password.")
                return redirect("user_login")
            if user.status == "Accepted":
                if user.otp_status == "Verified":
                    request.session["user_id_after_login"] = user.pk
                    messages.success(request, "Login successful!")
                    return redirect("user_dashboard")
                else:
                    new_otp = generate_otp()
                    user.otp = new_otp
                    user.otp_status = "Not Verified"
                    user.save()
                    subject = "New OTP for Verification"
                    message = f"Your new OTP for verification is: {new_otp}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(
                        subject, message, from_email, recipient_list, fail_silently=False
                    )
                    messages.warning(
                        request,
                        "OTP not verified. A new OTP has been sent to your email and phone.",
                    )
                    request.session["id_for_otp_verification_user"] = user.pk
                    return redirect("user_otp")
            else:
                messages.success(request, "Your Account is Not Accepted by Admin Yet")
                return redirect("user_login")
        except User.DoesNotExist:
            messages.error(request, "No User Found.")
            return redirect("user_login")
    return render(request,"user/user-login.html")





def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('user_register') 
        user = User(
            full_name=full_name,
            email=email,
            password=password, 
            phone_number=phone_number,
            age=age,
            address=address,
            photo=photo
        )
        otp = generate_otp()
        user.otp = otp
        user.save()
        subject = "OTP Verification for Account Activation"
        message = f"Hello {full_name},\n\nYour OTP for account activation is: {otp}\n\nIf you did not request this OTP, please ignore this email."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        request.session["id_for_otp_verification_user"] = user.pk
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, "Otp is sent your mail and phonenumber !")
        return redirect("user_otp")
    return render(request,"user/user-register.html")




def user_otp(request):
    otp_user_id = request.session.get("id_for_otp_verification_user")
    if not otp_user_id:
        messages.error(request, "No OTP session found. Please try again.")
        return redirect("user_register")
    if request.method == "POST":
        entered_otp = "".join(
            [
                request.POST["first"],
                request.POST["second"],
                request.POST["third"],
                request.POST["fourth"],
            ]
        )
        try:
            user = User.objects.get(id=otp_user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect("user_register")
        if user.otp == entered_otp:
            user.otp_status = "Verified"
            user.save()
            messages.success(request, "OTP verification successful!")
            return redirect("user_login")
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
            return redirect("user_otp")
    return render(request,"user/user-otp.html")




def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request,"user/admin-login.html")



def contact(request):
    return render(request,"user/result-result.html")

def result_result(request):
    return render(request,"user/contact.html")


def user_dashboard(request):
    user_id = request.session.get('user_id_after_login')
    user = User.objects.get(pk=user_id)
    detection_results = DetectionResult.objects.filter(user=user).order_by('-timestamp')

    context = {
        'user': user,
        'detection_results': detection_results,
    }

    return render(request, "user/user-dashboard.html", context)

from django.shortcuts import render
from django.conf import settings
import os
import requests
from django.core.files.storage import default_storage
from googletrans import Translator

def user_detection(request):
    context = {}
    if request.method == 'POST':
        
        selected_language = request.POST.get('language', 'english')
        
        if 'image' in request.FILES:
            
            uploaded_file = request.FILES['image']
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            print("Image saved at:", file_path)
        
        
        print("Selected language:", selected_language)

        
        filename = default_storage.save(uploaded_file.name, uploaded_file)
        default_storage_image_url = request.build_absolute_uri(default_storage.url(filename))
        print("Default Storage Image URL:", default_storage_image_url)

        public_ngrok_url = settings.PUBLIC_NGROK_URL
        image_url = public_ngrok_url + settings.MEDIA_URL + uploaded_file.name
        print("Public Image URL:", image_url)
        
        
        api_endpoint = "https://easy-peasy.ai/api/generate"
        api_key = "c24619c0-ca11-4b19-81f0-b470331d98ab"  
        headers = {
            "accept": "application/json",
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "preset": "image-description-generator",
            "keywords": image_url
        }
        
        response = requests.post(api_endpoint, headers=headers, json=payload)
        print("Easy-Peasy Response status code:", response.status_code)
        print("Easy-Peasy Response text:", response.text)
        
        caption = "No caption generated"
        if response.status_code == 200:
            try:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    caption = data[0].get("text", "No caption generated")
                elif isinstance(data, dict):
                    caption = data.get("caption", "No caption generated")
                print("Generated Caption:", caption)
            except Exception as e:
                print("Error parsing Easy-Peasy JSON:", e)
        else:
            print("Easy-Peasy API call failed:", response.status_code, response.text)
        
        
        
        if caption == "No caption generated":
            qa_output = ""
            print("Skipping Perplexity API call due to missing caption.")
        else:
            perplexity_api_url = "https://api.perplexity.ai/chat/completions"
            perplexity_token = "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"  
            
            
            prompt_text = (
                f"Based on the following image caption: '{caption}', "
                f"generate 5 concise questions and their corresponding answers in {selected_language}. "
                "Please provide only the questions and answers."
            )
            
            perplexity_payload = {
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": "Be precise and concise."},
                    {"role": "user", "content": prompt_text}
                ],
                "max_tokens": 1500,
                "temperature": 0.2,
                "top_p": 0.9,
                "search_domain_filter": None,
                "return_images": False,
                "return_related_questions": False,
                "search_recency_filter": "",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1,
                "response_format": None
            }
            
            perplexity_headers = {
                "Authorization": f"Bearer {perplexity_token}",
                "Content-Type": "application/json"
            }
            
            perplexity_response = requests.post(perplexity_api_url, headers=perplexity_headers, json=perplexity_payload)
            print("Perplexity Response status code:", perplexity_response.status_code)
            print("Perplexity Response text:", perplexity_response.text)
            
            qa_output = "No Q&A generated."
            if perplexity_response.status_code == 200:
                try:
                    data = perplexity_response.json()
                    
                    qa_output = data.get("choices", [{}])[0].get("message", {}).get("content", qa_output)
                    print("Generated Q&A:", qa_output)
                except Exception as e:
                    print("Error parsing Perplexity JSON:", e)
            else:
                print("Perplexity API call failed:", perplexity_response.status_code, perplexity_response.text)
        
        
        context['qa_data'] = qa_output
        context['image_url'] = default_storage_image_url
        
    return render(request, "user/detection.html", context)





def user_feedback(request):
    user_id = request.session.get('user_id_after_login')
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        additional_comments = request.POST.get('additional_comments')
        UserFeedback.objects.create(
            user=user,
            rating=rating,
            additional_comments=additional_comments
        )
        messages.success(request, 'Feedback submitted successfully.')
        return redirect('user_feedback')
    return render(request,"user/user-feedback.html",{'user':user})







def user_profile(request):
    user_id  = request.session.get('user_id_after_login')
    print(user_id)
    user = User.objects.get(pk= user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.photo = profile
        except MultiValueDictKeyError:
            profile = user.photo
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.full_name = name
        user.email = email
        user.phone_number = phone
        user.password = password
        user.address = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('user_profile')
    return render(request,'user/user-profile.html',{'user':user})



def image_upload(request):
    
    return render(request, 'user/upload.html')

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from duckduckgo_search import DDGS

def image_search(request):
    search_results = []

    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        filename = default_storage.save(uploaded_file.name, uploaded_file)
        image_url = request.build_absolute_uri(default_storage.url(filename))

        # Extract keywords from the image filename (excluding extension)
        keywords = os.path.splitext(uploaded_file.name)[0]

        # Perform image search using DuckDuckGo
        with DDGS() as ddgs:
            search_results = [
                result["image"]
                for result in ddgs.images(keywords, max_results=10)
            ]

        return render(request, 'user/image_search.html', {
            'image_url': image_url,
            'search_results': search_results
        })

    return render(request, 'user/image_search.html')




import os
import requests
from django.conf import settings
from django.shortcuts import render


def user_caption(request):
    caption = ""  
    if request.method == 'POST':
        
        image_file = request.FILES.get('image')
        language = request.POST.get('language')
        if language:
            print("Selected language:", language)
        
        if image_file:
            
            file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            print("Image saved at:", file_path)
            
            
            
            public_ngrok_url = settings.PUBLIC_NGROK_URL
            image_url = public_ngrok_url + settings.MEDIA_URL + image_file.name
            print("Public Image URL:", image_url)
            
            
            api_endpoint = "https://easy-peasy.ai/api/generate"
            api_key = "c24619c0-ca11-4b19-81f0-b470331d98ab"  
            headers = {
                "accept": "application/json",
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "preset": "image-description-generator",
                "keywords": image_url
            }
            
            response = requests.post(api_endpoint, headers=headers, json=payload)
            print("Easy-Peasy Response status code:", response.status_code)
            print("Easy-Peasy Response text:", response.text)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if isinstance(data, list) and len(data) > 0:
                        caption = data[0].get("text", "No caption generated")
                    elif isinstance(data, dict):
                        caption = data.get("caption", "No caption generated")
                    else:
                        caption = "No caption generated"
                    print("Generated Caption:", caption)
                except Exception as e:
                    print("Error parsing Easy-Peasy JSON:", e)
            else:
                print("Easy-Peasy API call failed:", response.status_code, response.text)
            
            
            if language and language.lower() != "english" and caption:
                perplexity_url = "https://api.perplexity.ai/chat/completions"
                perplexity_api_key = "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"
                perplexity_headers = {
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                }
                
                translation_prompt = f"Translate the following text into {language.capitalize()}: {caption}"
                translate_payload = {
                    "model": "sonar",
                    "messages": [
                        {"role": "system", "content": "Be precise and concise."},
                        {"role": "user", "content": translation_prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "search_domain_filter": None,
                    "return_images": False,
                    "return_related_questions": False,
                    "search_recency_filter": "",
                    "top_k": 0,
                    "stream": False,
                    "presence_penalty": 0,
                    "frequency_penalty": 1,
                    "response_format": None
                }
                perplexity_response = requests.post(perplexity_url, headers=perplexity_headers, json=translate_payload)
                print("Perplexity Response status code:", perplexity_response.status_code)
                print("Perplexity Response text:", perplexity_response.text)
                if perplexity_response.status_code == 200:
                    try:
                        perplexity_data = perplexity_response.json()
                        
                        if "choices" in perplexity_data and len(perplexity_data["choices"]) > 0:
                            translated_text = perplexity_data["choices"][0]["message"]["content"]
                            caption = translated_text
                        else:
                            print("No translation found; using original caption.")
                    except Exception as e:
                        print("Error parsing Perplexity JSON:", e)
                else:
                    print("Perplexity API call failed:", perplexity_response.status_code, perplexity_response.text)
                    
    return render(request, "user/caption.html", {"caption": caption})





def user_result(request):
    
    return render(request, "user/results.html")



