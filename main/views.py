from django.shortcuts import render
from main.utilities import createDottedImage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .serializers import ArtSerializer
from .models import Art
from django.shortcuts import redirect

class DashboardApiView(APIView):
    def get(self, request):
        data = Art.objects.all()
        serializer = ArtSerializer(data, many=True)
        print(serializer.data)
        return render(request, "main/dashboard.html", {"data":serializer.data})

class ArtAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return render(request, "main/imageupload.html")

    def post(self, request):
        data = request.data
        dots = request.data.get('dots') if request.data.get('dots') else 5000
        shape = request.data.get('shape') if request.data.get('shape') else "circle" 
        dot_size = request.data.get('size') if request.data.get('size') else 3 

        serializer = ArtSerializer(data=data)
        
        if serializer.is_valid():
            instance = serializer.save()
            # Generate Dot Images
            dot_image = createDottedImage(instance.original_file.path, int(dots), shape, int(dot_size))
            instance.dotted_image.name = dot_image.split('media/')[-1]
            instance.save()
            return redirect("/")
            # return Response(ArtSerializer(instance).data)
        return Response(serializer.errors, status=404)