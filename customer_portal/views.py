from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.conf import settings
from rest_framework.views import APIView
from .models import NewSpeedRequest
from .serializers import NewSpeedRequestSerializer
from . import sendEmail
import pyodbc
import time

# from Django.self_service.customer_portal import serializers


# Create your views here.
class NewRequest(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    # list all new requests, or create a new request
    def get(self, request, format=None):
        allRequest = NewSpeedRequest.objects.all()
        serializer = NewSpeedRequestSerializer(allRequest, many=True)
        return Response(serializer.data)



    def timer(func):
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            print(f'{func.__name__} took {end_time - start_time:.2f} seconds to execute.')
            return result
        return wrapper



    @timer
    def post(self, request, format=None):
        data=request.data
        accountNumber = data['accountNumber']
        contractName = data['contractName']
        contractPhone = data['contractPhone']
        contractEmail = data['contractEmail']
        currentPlan = data['currentPlan']
        newMRC = data['newMRC']
        comment = data['comment']

        customerInfo = self.getCustomerType(accountNumber)
        if customerInfo != None:
            customerName, customerType = customerInfo
            data['customerName'], data['customerType'] = customerName, customerType
        else:
            raise CustomerTypeNotFound 

       
        sendFrom = 'newspeedrequest@cableone.biz'
        sendTo = self.emailSendTo(customerType)

        new_line = '\n'
        subject = f'New Speed Upgrade Request From Customer {customerName}'
        text = (
            f'From customer: {customerName}{new_line}Customer accnumber: {accountNumber}{new_line}'
            f'Contract Name: {contractName}{new_line}ContractPhone: {contractPhone}{new_line}'
            f'Contract Email: {contractEmail}{new_line}CurrentPlan: {currentPlan}{new_line}'
            f'New Requested Speed: {newMRC}MB{new_line}Customer comment: {comment}'
            )


        serializer = NewSpeedRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # create email object
            newEmail = sendEmail.SendEmail(sendFrom, sendTo, subject, text)
            newEmail.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def emailSendTo(self, customerType):
        return 'bizhou.duan@cableone.biz'



    # init SQL connection
    def pyodbc_db_connection(self, server, database, username, password):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                            server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        return cursor


    # SQL query
    def pyodbc_query(self, cursor, query):
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows



    def getCustomerType(self, accountNumber):
        c1_goldengateDB = self.pyodbc_db_connection(settings.SQL_SERVER, settings.SQL_DATABASE, settings.SQL_USERNAME, settings.SQL_PASSWORD)
        subType = self.pyodbc_query(
            c1_goldengateDB, 
            (
                f'select CustomerName, BusinessSubscriberType '
                f'from SVCustom.dbo.CustomerSummary '
                f'where SingleviewAccount = {accountNumber}'
            )
        )

        if subType != []:
            for line in subType:
                customerType = line.BusinessSubscriberType.strip()
                customerName = line.CustomerName.strip()
            return customerName, customerType
        else: return None


    def get_customer_info(self, accountNumber):
        customerInfo = {}
        c1_goldengateDB = self.pyodbc_db_connection(settings.SQL_SERVER, settings.SQL_DATABASE, settings.SQL_USERNAME, settings.SQL_PASSWORD)
        info = self.pyodbc_query(
            c1_goldengateDB, 
            (
                f'select cu.CustomerName, cu.CustomerStatus, cu.CustomerType, cu.MRC, cu.customer_node_id, se.product_offer_name,'
                f' ad.MailingAddress1 as Address, ad.MailingCity as City, ad.MailingState as State, ad.MailingZip as Zip'
                f' from SVCustom.dbo.CustomerSummary as cu'
                f' inner join Singleview.dbo.SERVICE_TRE_V as se'
                f' on cu.customer_node_id = se.CUSTOMER_NODE_ID'
                f' inner join SVCustom.dbo.CustomerAddresses as ad'
                f' on cu.SingleviewAccount = ad.SingleviewAccount'
                f' where SERVICE_STATUS_CODE in (3, 102, 103)'
                f' and PRODUCT_OFFER_ID in ('
                                    # -- hard coded list provided by business owner
                                    f'1002263'    # -- Fiber Data Transport
                                    f', 1003817'  # -- Ethernet Transport Access
                                    f', 1003819'  # -- Direct Internet Access
                                    f', 1004276'  # -- EZ Ethernet 3Mx3M Retail
                                    f', 1004277'  # -- EZ Ethernet 5Mx5M Retail
                                    f', 1004278'  # -- EZ Ethernet 10Mx10M Retail
                                    f', 1004279'  # -- EZ Ethernet 3Mx3M Wholesale
                                    f', 1004280'  # -- EZ Ethernet 5Mx5M Wholesale
                                    f', 1004281'  # -- EZ Ethernet 10Mx10M Wholesale
                                    f', 1004807'  # -- EZ Ethernet 3Mx3M Retail Interstate
                                    f', 1004808'  # -- EZ Ethernet 5Mx5M Retail Interstate
                                    f', 1004809'  # -- EZ Ethernet 10Mx10M Retail Interstate
                                    f', 1004814'  # -- Ethernet Private Line - Priority
                                    f', 1004815'  # -- Ethernet Private Line Interstate - Priority
                                    f', 1004816'  # -- Dark Fiber
                                    f', 1004820'  # -- Cell Back-Haul - Priority
                                    f', 1106965'  # -- Ethernet Private Line - Priority Plus
                                    f', 1106966'  # -- Ethernet Private Line - Priority MAX
                                    f', 1106968'  # -- Ethernet Private Line Interstate - Priority Plus
                                    f', 1106969'  # -- Ethernet Private Line Interstate - Priority MAX
                                    f', 1106970'  # -- Cell Back-Haul - Priority Plus
                                    f', 1106971'  # -- Cell Back-Haul - Priority MAX
                                    f', 1106972'  # -- Packet Performance SLA
                                    f', 1107085)'  # -- Wholesale DIA)
                f' and cu.SingleviewAccount = {accountNumber}'
            )
        )
        
        if info != []:
            for line in info:
                customerName, status, customerType, MRC, nodeID, productOffer, address, city, state, zipCode = [x for x in line]
                customerInfo['customerName'] = customerName
                customerInfo['status'] = status
                customerInfo['customerType'] = customerType
                customerInfo['MRC'] = MRC
                customerInfo['nodeID'] = nodeID
                customerInfo['productOffer'] = productOffer
                customerInfo['address'] = f'{address.strip()}, {city.strip()}, {state.strip()}, {zipCode.strip()}'
                # return the first record
                return customerInfo
        else: return None




    def get_all_email(self, nodeID):
        allEmails = []
        c1_goldengateDB = self.pyodbc_db_connection(settings.SQL_SERVER, settings.SQL_DATABASE, settings.SQL_USERNAME, settings.SQL_PASSWORD)
        emails = self.pyodbc_query(
            c1_goldengateDB, 
            (
                f'select em.INDEX1_VALUE as EmailAddress, em.[DESCRIPTION] as EmailDescription, em.CUSTOMER_NODE_ID	as CustomerNodeId'
                f' from  Singleview.dbo.customer_node_da_array as em'
                f' where em.[DESCRIPTION] is not null'
                f' and em.CUSTOMER_NODE_ID = {nodeID}'
            )
        )

        if emails != []:
            for line in emails:
                allEmails.append(line.EmailAddress)
            return set(allEmails)
        else: return None



class CustomerTypeNotFound(APIException):
    status_code = 404
    default_detail = 'Unable to locate the customer subtype.'
    default_code = 'service_unavailable'



class NewRequestDetail(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # reteieve, update or delete a new request instance
    def get_object(self, pk):
        try:
            return NewSpeedRequest.objects.get(pk=pk)
        except NewSpeedRequest.DoesNotExist:
            raise Http404

    def get(self, request, id):
        speedRequest = self.get_object(id)
        serializer = NewSpeedRequestSerializer(speedRequest)
        return Response(serializer.data)

