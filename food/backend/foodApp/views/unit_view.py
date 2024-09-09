from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.unit import Unit
from ..serializers import UnitSerializer


class UnitView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = Unit.objects.get(pk=pk)
            serializer = UnitSerializer(brand)
            return Response(serializer.data)
        except Unit.DoesNotExist:
            return Response({"error": "CategoryBrand not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'name')
        queryset = Unit.objects.all().order_by(sort_by)
        serializer = UnitSerializer(queryset, many=True)

        return Response(serializer.data)