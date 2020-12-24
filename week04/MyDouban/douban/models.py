from django.db import models

# Create your models here.
class T1(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_star = models.IntegerField()
    short = models.CharField(max_length=400)
    review_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't1'