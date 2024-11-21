from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

#connection to AWS DynamoDB
db= boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
     )


@api_view(['GET','POST'])
def drinks_list(request):
    table = db.Table('drinks')
    drinks= table.scan()
    if request.method ==  "GET":     
        return Response({'drinks':drinks.get("Items")})
    
    elif request.method == "POST":
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({"error":'Failed to input data'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def health(request):
    return Response({"Status":'Healthy'}, status=status.HTTP_200_OK)

@api_view(['GET','DELETE','PUT'])     
def drink_detail(request, name):
    
    table = db.Table('drinks')

    if request.method == 'GET':
        drink = table.get_item(Key= {
            'name' : name
        })

        item = drink.get('Item')

        if item is not None:
            return Response({'drink': item})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({"error":'Failed to update'}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method =="DELETE":
        table.delete_item(Key= {
            'name' : name
        })
        return Response(status=status.HTTP_200_OK)

