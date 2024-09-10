from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.nutrition import Nutrition
from ..serializers import NutritionSerializer


class NutritionView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = Nutrition.objects.get(pk=pk)
            serializer = NutritionSerializer(brand)
            return Response(serializer.data)
        except Nutrition.DoesNotExist:
            return Response({"error": "Nutrition is not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        queryset = Nutrition.objects.all()
        serializer = NutritionSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = NutritionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Nutrition.objects.get(pk=pk)
        except Nutrition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)