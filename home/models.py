from django.db import models

# Create your models here.

class Job(models.Model):

    def __str__(self):
        return self.item_name

    
    job_name = models.CharField(max_length=100)
    job_desc = models.CharField(max_length=100)
    job_phnnumber = models.IntegerField(max_length=10)
    job_image = models.CharField(max_length=500,default="https://p.kindpng.com/picc/s/79-798754_hoteles-y-centros-vacacionales-dish-placeholder-hd-png.png")
