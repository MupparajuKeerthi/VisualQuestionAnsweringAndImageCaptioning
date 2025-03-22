from django.db import models

# Create your models here.
class bert_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10, default='96.0') 

    class Meta:
        db_table = "bert_model"

class Efficient_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10, default='98.6')  

    class Meta:
        db_table = "Efficient_model"

class cnn_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10, default='98.4')  

    class Meta:
        db_table = "cnn_model"



class Dataset(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True) 
  
    class Meta:
        db_table = 'dataset_table'