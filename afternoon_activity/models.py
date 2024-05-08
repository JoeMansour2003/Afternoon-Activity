from django.db import models


class Afternoon_Activity(models.Model):
    """
    This is the Model to print and handout to the counselors, 

    It has all the camper names, the activity and the activity leader as well as the date just to top it off.
    It can be easliy searched by sorting my the second_activity booloean field.
    """
    def __str__(self):
        return "Afternoon Activity: " + str(self.date) + " " + str(self.activity) + " preference: " + str(self.preference)    
    date = models.DateField()
    second_activity= models.BooleanField(default=False)
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE, related_name="activity_with_preference")
    # camper = models.ManyToManyField("Camper", related_name="camper_associated_with_activity")
        # 1 being the highest priority and 3 being the lowest priority
    preference = models.IntegerField(default=0)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(preference__gte=0, preference__lte=3), name='preference_in_range'),
        ]

class Campers_Afternoon_Relation(models.Model):
    '''
    This is the relation between afternoon_activity and camper
    '''
    def __str__(self):
        return str(self.camper) + " + " + str(self.afternoon_activity)
    afternoon_activity = models.ForeignKey("Afternoon_Activity", on_delete=models.CASCADE, related_name="activity_for_camper")
    camper = models.ForeignKey("Camper", on_delete=models.CASCADE, related_name="camper_in_activity")

class Activity(models.Model):
    """
    List of all the activities that the campers can choose from
    """
    def __str__(self):
        return (str(self.activity))
    activity = models.CharField(max_length=20)
    rainy_day = models.BooleanField(default=False)

class Camper(models.Model):
    """ 
    Camper profile
    """
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    cabin = models.ForeignKey("Cabin", on_delete=models.CASCADE, related_name="cabin_for_camper")
    # afternoon_activity = models.ManyToManyField("Afternoon_Activity", related_name="afternoon_activity_selected", null=True, blank=True)

class Cabin(models.Model):
    """ 
    Every Cabin has Campers and Counselors
    """
    def __str__(self):
        return "Cabin: " + str(self.cabin_number)
    cabin_number = models.IntegerField(primary_key=True)
    week_one = models.BooleanField(default=True)
    # camper = models.ForeignKey("Camper", on_delete=models.CASCADE, related_name="camper_in_cabin", null=True, blank=True) 
    # counselor = models.ForeignKey("Counselor", on_delete=models.CASCADE, related_name="counselor_in_cabin", null=True, blank=True)

class Counselor(models.Model):
    """ 
    Counselors only profile
    
    P-staff / volunteers should get there own model"""
    def __str__(self):
        return self.first_name + " " + self.last_name
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    cabin = models.ForeignKey("Cabin", on_delete=models.CASCADE, related_name="counselors_cabin")
    # possition = models.ForeignKey("Activity", on_delete=models.SET_NULL, related_name="possition_Activity", null=True, default=None, blank=True)

