from user.services import user_service
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from user.schema import SignUpReqSchema
from decorators.auth_decorators import must_be_user


@api_view(["POST"])
@parser_classes([JSONParser])
def signup(request):
    schema = SignUpReqSchema(data=request.data)
    schema.is_valid(raise_exception=True)
    request_data = schema.data
    return JsonResponse(
        user_service.sign_up(
            email=request_data["email"], password=request_data["password"]
        ),
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@parser_classes([JSONParser])
def login(request):
    schema = SignUpReqSchema(data=request.data)
    schema.is_valid(raise_exception=True)
    request_data = schema.data
    return JsonResponse(
        user_service.login(
            email=request_data["email"], password=request_data["password"]
        ),
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@must_be_user()
@parser_classes([JSONParser])
def logout(request):
    return JsonResponse(
        {"success": user_service.logout(request.user)},
        status=status.HTTP_201_CREATED,
    )
