from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.consumption import Consumption
from ..serializers import ConsumptionSerializer


class ConsumptionView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = Consumption.objects.get(pk=pk)
            serializer = ConsumptionSerializer(brand)
            return Response(serializer.data)
        except Consumption.DoesNotExist:
            return Response({"error": "Consumption is not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        queryset = Consumption.objects.all()
        serializer = ConsumptionSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = ConsumptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Consumption.objects.get(pk=pk)
        except Consumption.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)