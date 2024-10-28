from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


from members.models import GymMembers
from django.utils import timezone
from django.db import transaction

from datetime import timedelta
# Create your views here.

@login_required
def update_status(request):
    members = GymMembers.objects.all()

    expired_members = []
    active_members = []

    try:
        for member in members:
            if member.expiry_date < timezone.now():
                member.is_active = False
                expired_members.append(member)
            else:
                member.is_active = True
                active_members.append(member)

        # Use bulk update for better performance
        with transaction.atomic():
            GymMembers.objects.bulk_update(expired_members + active_members, ['is_active'])

        return redirect('home:dashboard')

    except Exception as e:
        print(f"An error occurred: {e}")

@login_required
def update_status_members(request):
    members = GymMembers.objects.all()

    expired_members = []
    active_members = []

    try:
        for member in members:
            if member.expiry_date < timezone.now():
                member.is_active = False
                expired_members.append(member)
            else:
                member.is_active = True
                active_members.append(member)

        # Use bulk update for better performance
        with transaction.atomic():
            GymMembers.objects.bulk_update(expired_members + active_members, ['is_active'])

        return redirect('members:view')

    except Exception as e:
        print(f"An error occurred: {e}")

@login_required
def home(request):
    
    return render(request,'home/index.html',{
        'user': request.user
    })

