from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
class CalenderSlot(models.Model):
    """Stores the calender slots available for the user to book by other people.

    """
    belongs_to = models.ForeignKey(get_user_model(), related_name='created_slots', on_delete=models.CASCADE, help_text="""
    Stores the user the slot belongs to.
    """)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False, help_text="""
    Contains the Date of the slot.
    """)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False, help_text="""
    Contains the start time of the slot.
    """)
    interval = models.IntegerField(null=False, blank=False ,help_text="""
    Contains the interval of the slot.
    """)
    created_at = models.DateTimeField(default=timezone.now, help_text="""
    Django auto populates this field whenever a slot is created by a user.
    """)


class SlotBooking(models.Model):
    """Contains the booking details of the slots.

    """
    slot = models.OneToOneField(to=CalenderSlot, related_name='booking_details', on_delete=models.CASCADE, help_text="""
    References to the slot that is booked.
    """)
    email = models.EmailField(null=False, blank=False, help_text="""
    Contains the email id of the non user booking the slot
    """)
    name = models.TextField(null=False, blank=False, help_text=""" 
    Contains the name of the non user booking the slot
    """)
    booked_at = models.DateTimeField(default=timezone.now, help_text="""
    Django automatically populates this field whenever a slot is booked.
    """)
    