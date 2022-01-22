import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from .models import CalenderSlot, SlotBooking
from django.contrib.auth import get_user_model
from datetime import datetime

class AvailableSlot(DjangoObjectType):
	class Meta:
		model = CalenderSlot


class Schedules(DjangoObjectType):
    class Meta:
    	model = SlotBooking


class Query(graphene.ObjectType):
    slots = graphene.List(AvailableSlot, username=graphene.String())
    user_slots = graphene.List(AvailableSlot)
    schedules = graphene.List(Schedules)


    def resolve_slots(self, info, username):
        """ This  takes one argument username
        Returns Availabe Slots of that username 
        """
        try:
           user = get_user_model().objects.get(username=username)
        except:
           user = None
        if user:
           if CalenderSlot.objects.filter(belongs_to=user).exclude(id__in = SlotBooking.objects.all().values('slot__id') ).exists():
               return CalenderSlot.objects.filter(belongs_to=user).exclude(id__in = SlotBooking.objects.all().values('slot__id') )
           else:
                raise GraphQLError ("No Slot Avaialable")
        else:
            raise GraphQLError ("Invalid User")


#This  Returns all the created Slots of the logged in user
    def resolve_user_slots(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("user must be logged in to create a slot")
        if CalenderSlot.objects.filter(belongs_to=user).exists():
            return CalenderSlot.objects.filter(belongs_to=user)
        else:
            raise GraphQLError("No Slots Created")


#This  Returns all the scheduled meetings  of the logged in user
    def resolve_schedules(self, info):
        user = info.context.user

        if user.is_anonymous:
           raise GraphQLError("user must be logged in to create a slot")
        if SlotBooking.objects.filter(slot__in = CalenderSlot.objects.filter(belongs_to=user).values('id')).exists():
           return SlotBooking.objects.filter(slot__in = CalenderSlot.objects.filter(belongs_to=user).values('id'))
        else:
           raise GraphQLError("No Meeting Scheduled")


"""
This creates a meeting slot for the logged in user.
It takes three arguments date, start time and interval.
Interval Should be 15, 30 or 45
"""
class CreateAvailableSlot(graphene.Mutation):
    slot = graphene.Field(AvailableSlot)

    class Arguments:
        date = graphene.String()
        start_time = graphene.String()
        interval = graphene.Int()

    def mutate(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("user must be logged in to create a slot")
        if kwargs.get('interval') == 15 or kwargs.get('interval') == 30 or kwargs.get('interval') == 45:
            if CalenderSlot.objects.filter(belongs_to=user).filter(date=kwargs.get('date')).filter(start_time=kwargs.get('start_time')).exists():
               raise GraphQLError("Slot Already Created")
            else:
                CalenderSlotObj = CalenderSlot(belongs_to=user, date=kwargs.get('date'), start_time = kwargs.get('start_time'), interval=kwargs.get('interval'))
            CalenderSlotObj.save()
            return CreateAvailableSlot(slot=CalenderSlotObj)
        else:
            raise GraphQLError("Interval Can only be 15 or 30 or 45")


"""
This Updates a meeting slot for the logged in user.
It takes three arguments slot id,date, start time and interval.
Interval Should be 15, 30 or 45
"""
class UpdateSlot(graphene.Mutation):
    slot = graphene.Field(AvailableSlot)

    class Arguments:
        slot_id = graphene.Int()
        date = graphene.String()
        start_time = graphene.String()
        interval = graphene.Int()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
           raise GraphQLError("user must be logged in to make any changes")
        if kwargs.get('interval') == 15 or kwargs.get('interval') == 30 or kwargs.get('interval') == 45:
            if CalenderSlot.objects.filter(id=kwargs.get('slot_id')).exists():
                CalenderSlotObj = CalenderSlot.objects.filter(id=kwargs.get('slot_id'))[0]
                if user != CalenderSlotObj.belongs_to:
                	raise GraphQLError("You are not the owner")
                date_obj = datetime.strptime(kwargs.get('date'), '%Y-%m-%d')
                CalenderSlotObj.date = date_obj.date()
                time_obj = datetime.strptime(kwargs.get('start_time'), '%H:%M:%S')
                CalenderSlotObj.start_time = time_obj.time()
                CalenderSlotObj.interval = kwargs.get('interval')
                CalenderSlotObj.save(update_fields=['date', 'start_time', 'interval'])
                return UpdateSlot(slot=CalenderSlotObj)
            else:
                raise GraphQLError("Invalid ID")
        else:
        	raise GraphQLError("Interval Can only be 15 or 30 or 45")


"""
This Delets a meeting slot for the logged in user.
It takes one arguments slot id.
"""
class DeleteSlot(graphene.Mutation):
    ok = graphene.Boolean();

    class Arguments:
        slot_id = graphene.Int()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("user must be logged in to make any changes")
        if CalenderSlot.objects.filter(id=kwargs.get('slot_id')).exists():
            CalenderSlotObj = CalenderSlot.objects.filter(id=kwargs.get('slot_id'))[0]
            if user != CalenderSlotObj.belongs_to:
               raise GraphQLError("You are not the owner")
            CalenderSlotObj.delete()
            return DeleteSlot(ok=True)
        else:
            raise GraphQLError("Invalid ID")


"""
This books the meeting for non logged in users.
It takes three arguments slot id, email and name
"""
class CreateSchedule(graphene.Mutation):
    schedule = graphene.Field(Schedules) 

    class Arguments:
        slot_id = graphene.Int()
        email = graphene.String()
        name = graphene.String()

    def mutate(self, info, **kwargs):
        CalenderSlotObj = CalenderSlot.objects.get(id=kwargs.get('slot_id'))
        if SlotBooking.objects.filter(slot=CalenderSlotObj).exists():
            raise GraphQLError("Meeting Already Booked For This Slot!")
        SlotBookingObj = SlotBooking.objects.create(slot=CalenderSlotObj, email=kwargs.get('email'), name=kwargs.get('name'))
        SlotBookingObj.save()
        return CreateSchedule(schedule=SlotBookingObj)



class Mutation(graphene.ObjectType):
    create_available_slot = CreateAvailableSlot.Field()
    update_slot = UpdateSlot.Field()
    delete_slot = DeleteSlot.Field()
    create_schedule = CreateSchedule.Field()




