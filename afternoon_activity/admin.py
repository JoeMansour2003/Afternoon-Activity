from django.contrib import admin

from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Campers_Afternoon_Relation,Group

admin.site.register(Afternoon_Activity)
admin.site.register(Activity)
admin.site.register(Camper)
admin.site.register(Cabin)
admin.site.register(Counselor)
admin.site.register(Campers_Afternoon_Relation)
admin.site.register(Group)