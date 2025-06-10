from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from PIL import Image
import io
from django.http import HttpResponse
from rembg import remove

class Index(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']

        try:
            input_image = Image.open(image_file)
            output_image = remove(input_image)

            # Sauvegrader dans un buffer
            buffered = io.BytesIO()
            output_image.save(buffered, content_type="image/png")

        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 