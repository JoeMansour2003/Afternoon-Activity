from django.contrib import admin

from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Group,Session,SessionCabin,Period

admin.site.register(Afternoon_Activity)
admin.site.register(Activity)
admin.site.register(Camper)
admin.site.register(Cabin)
admin.site.register(Counselor)
admin.site.register(Group)
admin.site.register(Period)
admin.site.register(Session)
admin.site.register(SessionCabin)