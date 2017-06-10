from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.shortcuts import render

from api.models import Notes
def index(request):
    html="<body style='background:#222'>";
    html+="<br><hr><h1 style='text-align:center;color:#FFF'>ISYNC</h1><hr><br><br><br>"
    html+="<div style='font-size:2em; text-align:center;color:#FFF'>This is an Api For Isync Android APP </div>"
    html+="<br><br> <br><br><br><div  style='text-align:center;color:#FFF;font-size:2em;'> " \
          "<a style='color:#FFF;text-decoration: none;' href='https://drive.google.com/file/d/0B5NESpCL3GJPUmNCdXFnTEdLQ2s/view?usp=drivesdk' >Click Here To download the app</a> </div>"
    html+="<br><br> <br><br><br><hr><br><div  style='position:relative; margin-bottom:20px;text-align:center;color:#FFF;font-size:2em;'> " \
          "DEVELOPED BY YOKESH RANA CSE BIET JHANSI </div><hr>"
    return HttpResponse(html)
@csrf_exempt
def Addnow(request):
    res=request.POST
    object=Notes.objects.all()
    try:
     t=object.create(text=res['text'],title=res['title'],username=res['username'])
     h = {
         'add': 'true'
     }
    except:
        h = {
            'add': 'false'
        }

    return JsonResponse(h)

@csrf_exempt
def update(request):
    res = request.POST
    try:
        t = Notes.objects.get(pk=res['pk'])
        t.text=res['text']
        t.username=res['username']
        t.title = res['title']
        t.save()
        h = {
            'update': 'true'
        }
    except:
        h = {
            'update': 'false'
        }

    return JsonResponse(h)

@csrf_exempt
def delete(request):
    res = request.POST
    try:
        t=Notes.objects.filter(username=res['username'])
        t = t.get(pk=res['pk']) #send pk for deletion
        t.delete()
        h = {
            'update': 'true'
        }
    except:
        h = {
            'update': 'false'
        }

    return JsonResponse(h)


def check(username, token):

    try:
        o=Token.objects.get(user__username=username).__str__()
        if o==token:
            return 1
        else:
            return 0
    except:
        return 0
    pass

@csrf_exempt
def show(request):
    res = request.POST
    username = res['username']
    token = res['token']
    option = res['option']
    if check(username, token):
        if option == "short":
            obj = Notes.objects.filter(username=username).order_by('-date')
            jsonarray = []
            for object in obj:
                str = object.title.__str__()
                pk=object.pk

                jsonobj = {'title': str,
                           'pk':pk,
                           'date': object.date.strftime('%d-%m-%Y'+" at " + '%H:%M:%S')}
                jsonarray.append(jsonobj)
            print(jsonarray)
            return JsonResponse(jsonarray, safe=False)

        elif option == "full":
            obj = Notes.objects.filter(username=username).order_by('date')
            jsonarray = []
            for object in obj:
                str = object.title.__str__()
                text = object.text.__str__()
                pk=object.pk
                jsonobj = {'title': str,
                           'text': text,
                           'pk':pk,
                                'date': object.date.strftime('%d-%m-%Y'+" at " + '%H:%M:%S')}

                jsonarray.append(jsonobj)
            print(jsonarray)
            return JsonResponse(jsonarray, safe=False)
        else:
            return JsonResponse({'error': 'true'})


@csrf_exempt
def login(request):
    u = request.POST['username']
    p = request.POST['password']
    userobj = authenticate(username=u, password=p)
    p = {
        "login": "false",
        "token": "null",
        "username": "null",

    }
    if userobj is not None:
        token = Token.objects.get(user__username=u).__str__()
        p['login'] = 'true'
        p['token'] = token
        p['username'] = userobj.email
        return JsonResponse(p)
    else:
        p['login'] = 'false'
        p['token'] = 'null'
        p['username'] ="null"
        return JsonResponse(p)
@csrf_exempt
def register(request):
    emailid = request.POST['username']
    password = request.POST['password']
    username = request.POST['emailid']
    updaterequired = request.POST['updaterequired']
    p = {
        "created": "false",
        "token": "null",
        "update": "false"  # return false if no updatation done or return true if some updation done
    }
    try:
        if updaterequired == 'false':
            obj = User.objects.create_user(username, emailid, password, is_staff=True)
            p['created'] = 'true'
            # obj.email_user("Registered succesfully","Thanks For registering on Hostel Management System", from_email='yokeshrana@gmail.com', )
        elif updaterequired == 'true':
            p['created'] = 'true'
            obj = User.objects.get(username=username)
            print(obj)

            if username not in ['admin', 'default']:
                obj.set_password(password)
                obj.save()
                p['update'] = 'updated'
            else:
                p['update'] = 'cant update admin bro'

        p['token'] = Token.objects.get(user__username=username).__str__()

        return JsonResponse(p)
    except:
        return JsonResponse(p)

@csrf_exempt
def showindividual(request,pk):

    res = request.POST
    username = res['username']
    token = res['token']
    jsonobj = {'text': "",
               'title':""
               }
    if check(username,token):
        obj = Notes.objects.get(pk=pk)

        jsonobj = {'text': obj.text,
                   'title':obj.title
                }

    return JsonResponse(jsonobj, safe=False)
