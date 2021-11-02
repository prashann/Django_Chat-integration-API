# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from chatIntegration.models import chat_rooms, messages
from django.contrib.auth.models import User

# Create your views here.

u = chat_rooms.objects.all()

def welcome(request):
    return JsonResponse('This is the Chat Integration API by Abhishek' , safe=False, status = status.HTTP_200_OK)

def index(request):
    data = u.order_by('-created_at')
    final = []
    for i in range(len(data)):
        g = [
            data[i].__dict__
        ]
        del(g[0]['_state'])
        # usD = User.objects.filter(id = data[i].User_id)
        # userDetails = {'ID':usD[0].id, 'First Name':usD[0].first_name,'Last Name':usD[0].last_name, 'Email':usD[0].email}
        # g[0]['User'] = userDetails
        final.append(g)
    if final != None or len(final) != 0:
        return JsonResponse(final , safe=False)
    elif len(final) == 0:
        return JsonResponse('No Chats Created!', safe=False)

def update(request, field, chat_id, update):
    check = u.filter(chat_room_id = chat_id).exists()
    if check == True:
        dta = u.get(chat_room_id = chat_id)
        if field == 'chat_room_id':
            return JsonResponse('Cannot Update Chat Room ID!',safe=False)
        elif field == 'name':
            if len(update) <= 100:
                che = chat_rooms.objects.filter(name = update).exists()
                if che == True:
                    return JsonResponse(f'Chat Room with name {update} already exists!' , safe=False, status=status.HTTP_401_UNAUTHORIZED)
                elif che == False:    
                    dta.name = update
                    dta.save()
                    return JsonResponse('Chat Room Updated Successfully!', safe=False, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse('Please enter an chat room name of 100 or less characters' , safe=False, status=status.HTTP_401_UNAUTHORIZED)
        elif field == 'created_at':
            dta.created_at = update
            dta.save()
            return JsonResponse('Chat Room Updated Successfully!' , safe=False, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse(f"No field named {field}!" , safe=False)
    
    elif check==False:
        return JsonResponse(f'Chat Room with ID {chat_id} does not exist!' , safe=False)

def delete(request, chat_id):
    check = chat_rooms.objects.filter(chat_room_id = chat_id).exists()
    msgCheck = messages.objects.filter(chat_room_id = chat_id).exists()
    if check == True:
        try:
            if msgCheck is True:
                msg_ID = messages.objects.filter('message_id').filter(chat_room_id=chat_id)
                for i in range(len(msg_ID)):
                    messages.objects.filter(message_id = msg_ID[i][0]).delete()
            chat_rooms.objects.filter(chat_room_id = chat_id).delete()
            return JsonResponse('Chat Room Deleted Successfully!', safe=False, status = status.HTTP_201_CREATED)
        except:
            return JsonResponse('Chat Room Deletion Failed!', safe=False, status = status.HTTP_409_CONFLICT)

    elif check == False:
        return JsonResponse('Chat Room does not exists. Please try deleting an existing Chat room.', safe=False, status=status.HTTP_404_NOT_FOUND)

def show(request, chat_id):
    findOrFail = u.filter(chat_room_id = chat_id).exists()
    if findOrFail == True:
        sh = u.get(chat_room_id = chat_id).__dict__
        del(sh['_state'])
        # sh['User'] = {'ID':u.get(alert_id = alert_id).User.id ,'Username':u.get(alert_id=alert_id).User.username ,'First Name':u.get(alert_id = alert_id).User.first_name, 'Last Name':u.get(alert_id= alert_id).User.last_name ,'Email':u.get(alert_id = alert_id).User.email,'Date Joined':u.get(alert_id = alert_id).User.date_joined}
        msg = messages.objects.filter(chat_room_id = sh['chat_room_id'])
        gu = []
        for i in range(len(msg)):
            G = {'Message ID':msg[i].message_id , 'Message':msg[i].message, 'Created_at':msg[i].created_at, 'Chat Room ID':msg[i].chat_room_id, 'User ID':msg[i].user_id}
            gu.append(G)
        sh['Messages'] = gu
        # hu = []
        # for j in range(len)
        shw = {'YOUR EXISTING DETAILS:' : sh}
        return JsonResponse(shw, safe=False, status = status.HTTP_200_OK)
    else:
        return JsonResponse("Chat Room does not exist" , safe=False,status=status.HTTP_409_CONFLICT)

# def form(request):
#     return render(request, 'form_alert.html' , status=status.HTTP_200_OK)

# def store(request):
#     if request.method == 'POST' :
#         alert_id = request.POST['alert_id']
#         alert_name = request.POST['alert_name']
#         alert_option = request.POST['alert_option']
#         latitude = request.POST['location_lat']
#         longitude = request.POST['location_lang']
#         address = request.POST['address']
#         description = request.POST['description']
#         User_id = request.POST['User_id']
#         is_active = request.POST['is_active']
#         created_by = request.POST['created_by']
#         created_at = request.POST['created_at']
#         updated_at = request.POST['updated_at']
#         deleted_at = request.POST['deleted_at']

#         check = Alert.objects.filter(alert_name = alert_name).exists()

#         if check == True:
#             return JsonResponse(f'User with Alert Name{alert_name} already exists!', safe=False)
#         if alert_name == None:
#             return JsonResponse('Alert Name is a required field. Alert creation failed!', safe=False)
#         elif alert_name != None:
#             try:
#                 prod = Alert()
#                 prod.User_id = request.POST.get('User_id')
#                 prod.alert_id = request.POST.get('alert_id')
#                 prod.alert_name = request.POST.get('alert_name')
#                 prod.alert_option = request.POST.get('alert_option')
#                 prod.location_lat = request.POST.get('location_lat')
#                 prod.image = request.FILES['image']
#                 prod.video = request.FILES['video']
#                 prod.location_lang = request.POST.get('location_lang')
#                 prod.address = request.POST.get('address')
#                 prod.description = request.POST.get('description')
#                 prod.is_active = request.POST.get('is_active')
#                 prod.created_at = request.POST.get('created_at')
#                 prod.created_by = request.POST.get('created_by')
#                 prod.updated_at = request.POST.get('updated_by')
#                 prod.updated_by = request.POST.get('updated_at')
#                 prod.deleted_by = request.POST.get('deleted_at')
#                 prod.save()
#                 return JsonResponse('Alert Created Successfully!', safe=False, status=status.HTTP_201_CREATED)
#             except:
#                 return JsonResponse('Alert Creation Failed!', safe=False, status= status.HTTP_409_CONFLICT)