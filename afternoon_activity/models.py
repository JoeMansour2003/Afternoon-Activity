from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models,transaction


class Group(models.Model):
    """
    Groups for the activities
    Seniors, Juniors, or specific cabins 1-4 only
    """
    UNDELETABLE_NAMES = {"All", "Seniors", "Juniors"}

    def __str__(self):
        if self.group_name != None:
            return str(self.group_name)
        return str(self.group)
    def delete(self, *args, **kwargs):
        # Prevent deletion of undeletable periods
        if self.group_name in self.UNDELETABLE_NAMES:
            return
        super().delete(*args, **kwargs)
    group_name = models.CharField(max_length=30, null=True, blank=True) # Seniors, Juniors, All
    group = models.ManyToManyField("Cabin", related_name="cabins_in_group")
class Period(models.Model):
    """
    List of period options: {First Period, Second Period, Morning Exercise, Cabin Time Activities} 
    """
    UNDELETABLE_NAMES = {"First Period"}
    
    def __str__(self):
        return str(self.period)
    def delete(self, *args, **kwargs):
        # Prevent deletion of undeletable periods
        if self.period in self.UNDELETABLE_NAMES:
            return
        super().delete(*args, **kwargs)
    period = models.CharField(max_length=30)
    
def get_first_period():
    return Period.objects.get(period="First Period").id

def get_default_group():
    return Group.objects.get(group_name="All").id

class Afternoon_Activity(models.Model):
    """
    This is the Model that is used to create the afternoon activities for that day.

    It can be easily searched by sorting by the second_activity boolean field.
    """
    def __str__(self):
        return str(self.date) + "; " + str(self.period) + "; " + str(self.allowed_groups) + "; Activity: " + str(self.activity)# + " preference: " + str(self.preference)
    date = models.DateField()
    rainy_day= models.BooleanField(default=False)
    allowed_groups = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="group_for_activity", default=get_default_group())
    period = models.ForeignKey("Period", on_delete=models.CASCADE, related_name="afternoon_activity_period", default=get_first_period())
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE, related_name="afternoon_activity")
    spots_left = models.IntegerField(help_text="Will be automatically overwritten with 'max_participants' for the activity in question.", null=True, blank=True, default=None) # Set to max_participants in the save function bellow
    campers = models.ManyToManyField("Camper", related_name="camper_associated_with_activity", blank=True)
    def save(self, *args, **kwargs):
        self.spots_left = self.activity.max_participants # No matter what you put in the spots_left field, it will always be the max_participants
        super().save(*args, **kwargs)
    
    # counselor = models.ForeignKey("Counselor", on_delete=models.CASCADE, related_name="counselor_for_activity")

    # group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="group_for_afternoon_activity")
    
    # camper = models.ManyToManyField("Camper", related_name="camper_associated_with_activity")
        # 1 being the highest priority and 3 being the lowest priority
    # preference = models.IntegerField(default=0)
    class Meta:
        constraints = [
            # models.CheckConstraint(check=models.Q(preference__gte=0, preference__lte=3), name='preference_in_range'),
        ]
# class Campers_Activity_Relation(models.Model):
#     '''
#     << THIS IS THE MODEL THAT YOU PRINT >>
    
#     This is the relation between afternoon_activity and camper    
#     '''
#     def __str__(self):
#         return str(self.afternoon_activity) + "; Camper: " + str(self.camper)
#     afternoon_activity = models.ForeignKey("Afternoon_Activity", on_delete=models.CASCADE, related_name="activity_for_camper")
#     camper = models.ForeignKey("Camper", on_delete=models.CASCADE, related_name="camper_in_activity")


class Activity(models.Model):
    """
    List of all the activities that the campers can choose from
    """
    def __str__(self):
        return (str(self.activity))
    activity = models.CharField(max_length=20)
    rainy_day = models.BooleanField(default=False)
    max_participants = models.IntegerField(default=15)
class Camper(models.Model):
    """
    Camper profile
    """
    def __str__(self):
        return self.first_name + " " + self.last_name

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    session_cabin = models.ManyToManyField("SessionCabin", related_name="cabin_for_camper")
    
    # afternoon_activity = models.ManyToManyField("Afternoon_Activity", related_name="afternoon_activity_selected", null=True, blank=True)

class Session(models.Model):
    """
    List of all Sessions
    """
    def __str__(self):
        return "Session: " + str(self.session_number)
    session_number = models.IntegerField(null=True, blank=True) #primary_key=True
    # camper = models.ForeignKey("Camper", on_delete=models.CASCADE, related_name="camper_in_cabin", null=True, blank=True)
    # counselor = models.ForeignKey("Counselor", on_delete=models.CASCADE, related_name="counselor_in_cabin", null=True, blank=True)
class Cabin(models.Model):
    """
    List of all Cabins
    """
    def __str__(self):
        return "Cabin: " + str(self.cabin_number)
    cabin_number = models.IntegerField(primary_key=True)
    
class SessionCabin(models.Model):
    """
    Automatically created Cartesian Product of Session and Cabin 
    """
    def __str__(self):
        return f"Session: {self.session.session_number}, Cabin: {self.cabin.cabin_number}"
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)

@transaction.atomic
def populate_session_cabin():
    """
    Preforms the Cartesian Product of Session and Cabin
    """
    sessions = Session.objects.all()
    cabins = Cabin.objects.all()
    
    for session in sessions:
        for cabin in cabins:
            SessionCabin.objects.create(session=session, cabin=cabin)
            
@receiver(post_save, sender=Cabin)
@receiver(post_save, sender=Session)
def run_on_create_or_update(sender, **kwargs):
    populate_session_cabin()

class Counselor(models.Model):
    """
    Counselors only profile

    P-staff / volunteers should get there own model"""
    def __str__(self):
        return self.first_name + " " + self.last_name
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    sessionCabin = models.ManyToManyField("SessionCabin", related_name="counselors_for_session_cabin", blank=True)
    afternoon_role = models.ManyToManyField("Afternoon_Activity", related_name="counselor_for_activity", blank=True)
    
