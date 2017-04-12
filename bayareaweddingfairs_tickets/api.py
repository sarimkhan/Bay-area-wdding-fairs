from django.shortcuts import render
from restless.models import serialize
from restless.auth import BasicHttpAuthMixin, login_required
from restless.views import Endpoint
from django.contrib.auth.models import User
from django_comments.models import Comment
from restless.http import Http201, Http404, Http400, HttpError
from django.contrib.auth import authenticate, logout, login
from rest_framework import status
from rest_framework.response import Response
from fullcalendar.util import events_to_json, calendar_options
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import get_object_or_404, HttpResponse
from django.db.models import Q
from .models import EventTickets
import stripe
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
import json
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
from restless.http import Http201, Http404, Http400, HttpError, Http200
from django.http import QueryDict
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authtoken.models import Token

@csrf_exempt
def iOSLoginBAWF(request):
    if request.method == "POST":
        print 'abcd'
        print request.POST
        print request.GET
        print request
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username and not password:
            print "response inside if"
            return Http400("failed")
        print 'ca', username
        print 'ca', password
        user_auth = authenticate(username=username, password=password)
        try:
            print 'auth', user_auth
            user_auth.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user_auth)
            print 'auth'
            if not user_auth.is_staff:
                return Http400("failed")
            token = Token.objects.get_or_create(user=user_auth)[0]

            # return HttpResponse(json.dumps({
            #     'key':token.key,
            # }))
            return Http200(serialize({
                'key':token.key,
            }))
        except Exception as e:
            print e

    return Http400("failed")

from rest_framework.authentication import SessionAuthentication as OriginalSessionAuthentication

class SessionAuthentication(OriginalSessionAuthentication):
    def enforce_csrf(self, request):
        return
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# @csrf_exempt
from rest_framework.permissions import IsAdminUser, IsAuthenticated
class TicketsAPI(APIView):
   # permission_classes = (AllowAny,)
    permission_classes = (IsAdminUser,)
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication,SessionAuthentication)

    # @csrf_exempt
    def post(self, request, format=None):
        print "User: ",request.user
        print "Data: ",request.POST
        # print "Method: ",request.method
        if request.method == "POST":
            print request.POST
            if "code" in request.POST:
                code = request.POST.get('code')
                print code
                ticket = get_object_or_404(EventTickets, code=code)
                print ticket.email, ticket
                dict_obj = {
                    'id':ticket.id,
                    'email':ticket.email,
                    'promocode_success':ticket.promocode_success,
                    'expire':ticket.expire,
                    'amount':ticket.amount,
                    'quantity':ticket.quantity,
                    'earlybird_ticket':ticket.earlybird_ticket,
                    'group_ticket':ticket.group_ticket,
                    'code':ticket.code,
                    'is_attended':ticket.is_attended,
                    'created_at':str(ticket.created_at),
                    'phone':ticket.phone,
                    'event':ticket.event.name,
                }
                print dict_obj
                return Http200(serialize(dict_obj))
            elif "code_update" in request.POST:
                code = request.POST.get('code_update')
                print code
                ticket = get_object_or_404(EventTickets, code=code)
                ticket.is_attended = True
                ticket.save()
                dict_obj = {
                    'id':ticket.id,
                    'email':ticket.email,
                    'promocode_success':ticket.promocode_success,
                    'expire':ticket.expire,
                    'amount':ticket.amount,
                    'quantity':ticket.quantity,
                    'earlybird_ticket':ticket.earlybird_ticket,
                    'group_ticket':ticket.group_ticket,
                    'code':ticket.code,
                    'is_attended':ticket.is_attended,
                    'created_at':str(ticket.created_at),
                    'phone':ticket.phone,
                    'event':ticket.event.name,
                }
                print Http200(serialize(dict_obj))
                return Http200(serialize(dict_obj))
        print 'get'
        return HttpResponse("No such method available.")

from yapjoy_files.models import Event_fairs
class iOSEvent(APIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAdminUser,)
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication,SessionAuthentication)

    # @csrf_exempt
    def get(self, request):
        dict_obj = []
        tickets = EventTickets.objects.all().distinct('event_id')
        events = Event_fairs.objects.filter(id__in=tickets.values_list('event_id',flat=True))
        for event in events:
           add_ticket = {
               'event_name':event.name,
               'event_date':event.date,
               'tickets':str(tickets.filter(event=event).count()),
           }
           dict_obj.append(add_ticket)

        return Http200(serialize(dict_obj))