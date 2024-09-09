from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.recipy_category import RecipyCategory
from ..serializers import RecipyCategorySerializer


class RecipyCategoryView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = RecipyCategory.objects.get(pk=pk)
            serializer = RecipyCategorySerializer(brand)
            return Response(serializer.data)
        except RecipyCategory.DoesNotExist:
            return Response({"error": "CategoryBrand not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'name')
        queryset = RecipyCategory.objects.all().order_by(sort_by)
        serializer = RecipyCategorySerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = RecipyCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = RecipyCategory.objects.get(pk=pk)
        except RecipyCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)