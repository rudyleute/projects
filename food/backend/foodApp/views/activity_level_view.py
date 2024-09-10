from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.activity_level import ActivityLevel
from ..serializers import ActivityLevelSerializer


class ActivityLevelView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = ActivityLevel.objects.get(pk=pk)
            serializer = ActivityLevelSerializer(brand)
            return Response(serializer.data)
        except ActivityLevel.DoesNotExist:
            return Response({"error": "ActivityLevel not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'multiplier')
        queryset = ActivityLevel.objects.all().order_by(sort_by)
        serializer = ActivityLevelSerializer(queryset, many=True)

        return Response(serializer.data)