from django.contrib import admin

# Register your models here.

from .models import UserInfo
from .models import Role
from .models import Bundle
from .models import Schedule

admin.site.register(UserInfo)
admin.site.register(Role)
admin.site.register(Bundle)
admin.site.register(Schedule)
