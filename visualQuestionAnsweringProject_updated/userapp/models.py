from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="User Name")
    email = models.EmailField(verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    age =models.CharField(max_length=15, verbose_name="age")
    address = models.TextField(verbose_name="Address")
    photo = models.ImageField(upload_to='profiles/', verbose_name="Upload Profile", null=True, blank=True)
    otp = models.CharField(max_length=6, default='000000', help_text='Enter OTP for verification')
    otp_status = models.CharField(max_length=15, default='Not Verified', help_text='OTP status')
    status = models.CharField(max_length=15,default='Pending')

    def __str__(self):
        return self.full_name
    

from django.db import models

class DetectionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    image = models.ImageField(upload_to='detected_images/', verbose_name="Uploaded Image")
    image_url = models.URLField(max_length=255, verbose_name="Image URL")
    questions_answers = models.JSONField(verbose_name="Question and Answers")  # Store Q&A in JSON format
    model_accuracy = models.FloatField(verbose_name="Model Accuracy", default=96)  # Default model accuracy if not available
    timestamp = models.DateTimeField(auto_now_add=True)  # Store when the detection result was created

    def __str__(self):
        return f"Detection result for {self.user.full_name} on {self.image_url} at {self.timestamp}"



from django.db import models

class CaptionPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="captions", verbose_name="User")
    uploaded_image_url = models.URLField(max_length=200, verbose_name="Uploaded Image URL")
    actual_captions = models.JSONField(verbose_name="Actual Captions")  # Assuming captions is a list of strings
    predicted_caption = models.CharField(max_length=500, verbose_name="Predicted Caption")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp of Caption")
    
    def __str__(self):
        return f"Caption Prediction for {self.user.full_name} on {self.timestamp}"



class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    additional_comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_feedback'


class ImageUpload(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    enhanced_image = models.ImageField(upload_to='media/', blank=True, null=True)
    pixel_difference = models.FloatField(default=0.0)
    differing_pixels = models.IntegerField(default=0)
    total_pixels = models.IntegerField(default=0)

    def __str__(self):
        return f"Image {self.id}"


class Dataset(models.Model):
   Data_id = models.AutoField(primary_key=True)
   Image = models.ImageField(upload_to='media/') 
   class Meta:
        db_table = "upload_caption" 