from django.contrib import admin
from .models import CalenderSlot, SlotBooking
# Register your models here.

class CalenderSlotAdmin(admin.ModelAdmin):
	model = CalenderSlot
	list_display = ('pk', 'belongs_to', 'date', 'start_time', 'interval', 'created_at')
	list_editable = ('belongs_to', 'date', 'start_time', 'interval')

admin.site.register(CalenderSlot, CalenderSlotAdmin)

class SlotBookingAdmin(admin.ModelAdmin):
	model = SlotBooking
	list_display = ('pk', 'slot', 'email', 'name', 'booked_at')
	list_editable = ('slot', 'email', 'name')

admin.site.register(SlotBooking, SlotBookingAdmin)