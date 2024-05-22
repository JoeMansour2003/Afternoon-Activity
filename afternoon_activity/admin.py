from django.contrib import admin
from django.db import models


from .models import ProgramActivity,Activity,Camper,Cabin,Counselor,Group,Session,SessionCabin,Period
from .widgets import AdminDateWidgetWithTomorrowButton

class ProgramActivityAdmin(admin.ModelAdmin):
    filter_horizontal = ('campers',)
    formfield_overrides = {
        models.DateField: {'widget': AdminDateWidgetWithTomorrowButton},
    }

admin.site.register(ProgramActivity,ProgramActivityAdmin)
admin.site.register(Activity)
admin.site.register(Camper)
admin.site.register(Cabin)
admin.site.register(Counselor)
admin.site.register(Group)
admin.site.register(Period)
admin.site.register(Session)
admin.site.register(SessionCabin)