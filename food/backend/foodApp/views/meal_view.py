from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.meal import Meal
from ..serializers import MealSerializer


class MealView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = Meal.objects.get(pk=pk)
            serializer = MealSerializer(brand)
            return Response(serializer.data)
        except Meal.DoesNotExist:
            return Response({"error": "Meal is not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'time')
        queryset = Meal.objects.all().order_by(sort_by)
        serializer = MealSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)