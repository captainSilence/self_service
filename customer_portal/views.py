from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import NewSpeedRequest
from .serializers import NewSpeedRequestSerializer
from . import sendEmail

# from Django.self_service.customer_portal import serializers


# Create your views here.

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getNewRequest(request):
    # data = {'accountNumber':123456, 'name': 'test', 'email':'test@cableone.biz', 'phoneNumber': '4806375524', 'newSpeed':'500', 'comment':'no comment'}
    allRequest = NewSpeedRequest.objects.all()
    serializer = NewSpeedRequestSerializer(allRequest, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addNewRequest(request):
    data=request.data
    sendFrom = 'newspeedrequest@cableone.biz'
    sendTo = 'bizhou.duan@cableone.biz'
    accountNumber = data['accountNumber']
    name = data['name']
    email = data['email']
    phoneNumber = data['phoneNumber']
    newSpeed = data['newSpeed']
    comment = data['comment']
    new_line = '\n'
    subject = f'New Speed Upgrade Request From Customer {name}'
    text = (
        f'From customer: {name}{new_line}Customer accnumber: {accountNumber}{new_line}'
        f'Customer email: {email}{new_line}Customer Phone#: {phoneNumber}{new_line}'
        f'Customer new desired speed: {newSpeed}MB{new_line}Comment from customer: {comment}'
    )

    serializer = NewSpeedRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # create email object
        newEmail = sendEmail.SendEmail(sendFrom, sendTo, subject, text)
        newEmail.send()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)