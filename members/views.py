from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.

# importing rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

#importing models 
from  .models import GymMembers,Subscription,Paymentmethod
from .forms import GymMembersForm
from django.utils import timezone
import requests
from django.contrib import messages
from django.middleware.csrf import get_token
from django.core.files.storage import default_storage
from rest_framework import status
import datetime
#importing serializer
from .serializers import GymMembersSerializer


from django.http import JsonResponse
import json

class GymMembersAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    
 
    def get(self,request,id=None):
        if id:
            # Fetch a specific GymMember by ID
            gym_member = get_object_or_404(GymMembers, id=id)
            serializer = GymMembersSerializer(gym_member)
        else:
            # Fetch all GymMembers
            gym_members = GymMembers.objects.all()
            serializer = GymMembersSerializer(gym_members, many=True)
        
        return Response(serializer.data)
    
    def post(self,request,format=None):
        data = request.data  # Copy data to manipulate
        
        print(f'before')
        print(data)
        
        # Optionally convert model instances to primary keys if they are objects
        if isinstance(data.get('sub_type'), Subscription):
            data['sub_type'] = data['sub_type'].id
        if isinstance(data.get('pay_method'), Paymentmethod):
            data['pay_method'] = data['pay_method'].id
            
            
        data['created_at'] = timezone.now().isoformat()
        expiry_at = timezone.now() + datetime.timedelta(days=30)

        image_save = False
        # Edit user_profile_image field
        if 'user_profile_image' in data:
            user_profile_image = data['user_profile_image']
            if user_profile_image:
                data_path ='members/' + user_profile_image.name
                data['user_profile_image'] = 'media/members/' + user_profile_image.name
                if 'user_profile_image' in request.FILES:
                    user_profile_image = request.FILES['user_profile_image']
                    if user_profile_image:
                        default_storage.save(data_path, user_profile_image)
                        print('saved image')
                        image_save=True
                        
        if image_save or not data['user_profile_image']:
                
            data = {
                'name': data.get('name'),
                'email': data.get('email'),
                'phone_number': data.get('phone_number'),
                'address': data.get('address'),
                'city': data.get('city'),
                'sub_type': data.get('sub_type'),
                'pay_method': data.get('pay_method'),
                'user_profile_image': data.get('user_profile_image'),
                'is_active': data.get('is_active', False),
                'created_by': request.user.id,
                'created_at' : timezone.now().isoformat(),
                'expiry_date' : expiry_at
                # Default value if not present
            }
            # data = json.dumps(data)
            print('after')
            print(data)
            
            serializer = GymMembersSerializer(data=data)
            if serializer:
                print('serialized')
            
            if serializer.is_valid():
                print('validated')
                serializer.save()  # Save to get instance
                print('saved')
                
                # Save user_profile_image to storage if present
                
                        
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:   
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Failed to save image", status=status.HTTP_400_BAD_REQUEST)

    
    
    def put(self,request):
        data = request.data
        serializer = GymMembersSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def patch(self,request):
        data = request.data
        obj = GymMembers.objects.get(obj,id=data['id'])
        serializer = GymMembersSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def delete(self,request):
        try:
            data = request.data
            obj = GymMembers.objects.get(id=data['id'])
            obj.delete()
            return Response({'message': 'Member deleted successfully'}, status=204)
        except GymMembers.DoesNotExist:
            return Response({'message': 'Member not found'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=500)
        


@login_required
def add_member(request):

    # if request.method == 'POST':
    #     print('''this function called ''')
    #     form = GymMembersForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         data['created_by'] = request.user.id
    #         data['created_at'] = timezone.now().isoformat() 
            
    #         # Optionally convert model instances to primary keys
    #         data['sub_type'] = data['sub_type'].id
    #         data['pay_method'] = data['pay_method'].id
    #         if data['user_profile_image']:
    #             data['user_profile_image'] = 'members/' + user_profile_image.name 
            
            
    #         # Send data to API endpoint
    #         LOCAL_HOST = "http://127.0.0.1:8000/"
    #         csrf_token = get_token(request)
    #         headers = {'X-CSRFToken': csrf_token}
            
    #         try:
    #             response = requests.post(
    #                 f'{LOCAL_HOST}api/members/',
    #                 json=data,
    #                 headers=headers,
    #                 cookies=request.COOKIES
    #             )
                
    #             print("***********")
    #             print(response.status_code)
                
    #             if response.status_code == 201:
    #                 messages.success(request, 'User created successfully!')
    #                 # Handle user_profile_image if present
    #                 if 'user_profile_image' in request.FILES:
    #                     user_profile_image = request.FILES['user_profile_image']
    #                     # Save user_profile_image to storage
    #                     file_path = default_storage.save(data['user_profile_image'], user_profile_image)
    #                     print(f"Saved profile image to: {file_path}")

    #             elif response.status_code == 400:
    #                 messages.error(request, 'Failed to create user. Please try again.')
    #                 form.add_error(None, response.json())
                    
            
    #         except requests.exceptions.RequestException as e:
    #             print(f"Error making API request: {e}")
    #             messages.error(request, 'Failed to create user. Please try again.')
                
    # else:
    form = GymMembersForm()
    
    return render(request, 'members/add_members.html', {'form': form})

@login_required
def view_members(request):
    # member = GymMembers.objects.get(pk=pk)
    
    return render(request,'members/view_member.html')    

@login_required
def member_profile(request,pk):
    member = GymMembers.objects.get(pk=pk)
    return render(request,'members/member_profile.html',{'member':member})


@login_required
def update_renew():
    pass