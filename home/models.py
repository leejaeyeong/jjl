from django.db import models

# Create your models here.

class Home(models.Model) :
    log = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    startH = models.TimeField()
    endH = models.TimeField()
    hour = models.IntegerField()
    minute = models.IntegerField()

    def __str__(self) :
        return str(self.id ) + "번째 근무 시간"