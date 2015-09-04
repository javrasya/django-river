from django.contrib import admin
from .models import *

admin.site.register(Handler)
admin.site.register(Proceeding)
admin.site.register(ProceedingMeta)
admin.site.register(ProceedingTrack)
admin.site.register(State)
admin.site.register(Transition)