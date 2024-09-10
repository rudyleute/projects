from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.nutritional_element import NutritionalElement
from ..serializers import NutritionalElementSerializer


class NutritionalElementView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = NutritionalElement.objects.get(pk=pk)
            serializer = NutritionalElementSerializer(brand)
            return Response(serializer.data)
        except NutritionalElement.DoesNotExist:
            return Response({"error": "NutritionalElement is not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'name')
        queryset = NutritionalElement.objects.all().order_by(sort_by)
        serializer = NutritionalElementSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = NutritionalElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)