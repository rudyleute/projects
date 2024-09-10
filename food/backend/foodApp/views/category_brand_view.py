from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.category_brand import CategoryBrand
from ..serializers import CategoryBrandSerializer


class CategoryBrandView(APIView):
    def get(self, request, pk=None):
        return self.__get_by_id(request, pk) if pk else self.__get_all(request)

    def __get_by_id(self, request, pk):
        try:
            brand = CategoryBrand.objects.get(pk=pk)
            serializer = CategoryBrandSerializer(brand)
            return Response(serializer.data)
        except CategoryBrand.DoesNotExist:
            return Response({"error": "CategoryBrand is not found."}, status=status.HTTP_404_NOT_FOUND)

    def __get_all(self, request):
        sort_by = request.query_params.get('sort', 'name')
        queryset = CategoryBrand.objects.all().order_by(sort_by)
        serializer = CategoryBrandSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryBrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the new book in the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = CategoryBrand.objects.get(pk=pk)
        except CategoryBrand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)