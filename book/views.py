from book.services import book_service
from book.schema import BookCreateReq
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from decorators.auth_decorators import must_be_user


@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def create_book(request):
    user_id = request.user
    params = BookCreateReq(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(
        book_service.create({**params.data, "user": user_id}),
        status=status.HTTP_201_CREATED,
    )


@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def update(request, book_id: str):
    params = BookCreateReq(data=request.data)
    params.is_valid(raise_exception=True)
    user_id = request.user
    return JsonResponse(
        book_service.update(int(book_id), user_id, params.data),
        status=status.HTTP_201_CREATED,
    )


@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def delete_book(request, book_id: str):
    is_deleted = book_service.delete(int(book_id), request.user)
    return JsonResponse(
        data={"success": is_deleted},
        status=status.HTTP_201_CREATED,
    )


@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def get_book(request, book_id: str):
    return JsonResponse(
        book_service.get(book_id=int(book_id), user_id=request.user),
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def revocer_book(request, book_id: str):
    return JsonResponse(
        book_service.recover(int(book_id), request.user), status=status.HTTP_201_CREATED
    )


@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def find_book(request):
    q = request.GET
    user_id = request.user
    offset = q.get("offset", 0)
    limit = q.get("limit", 50)
    return JsonResponse(
        book_service.find(user_id, offset, limit), status=status.HTTP_200_OK
    )


class BookDetailAPI(APIView):
    def get(self, request, book_id: str):
        return get_book(request, book_id)

    def post(self, request, book_id: str):
        return update(request, book_id)

    def delete(self, request, book_id: str):
        return delete_book(request, book_id)


class BookAPI(APIView):
    def post(self, request):
        return create_book(request)

    def get(self, request):
        return find_book(request)
