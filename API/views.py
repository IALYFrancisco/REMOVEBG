from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import io
from django.http import HttpResponse
from rembg import remove
from PIL import Image, ImageEnhance
import numpy as np
import cv2

from rembg import remove, new_session  # <-- ajout de new_session


class Index(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        # Vérifier si l'image est fournie
        if 'image' not in request.FILES:
            return Response({"error": "Aucun fichier image fourni."}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        try:
            # Ouvrir l'image
            input_image = Image.open(image_file)
            print("Image ouverte avec succès.")  # Pour debug

            # Supprimer l'arrière-plan
            output_image = remove(input_image)

            # Sauvegarde dans un buffer
            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            buffered.seek(0)  # Repositionner le buffer

            # Retourner l'image traitée
            return HttpResponse(buffered.getvalue(), content_type="image/png")

        except Exception as e:
            print("Erreur:", str(e))  # Log de l'erreur
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class V2(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response({"error": "Aucun fichier image fourni."}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        try:
            # Ouvrir et convertir l'image
            input_image = Image.open(image_file).convert("RGBA")

            # === PRÉTRAITEMENT ===
            # 1. Améliorer le contraste
            input_image = ImageEnhance.Contrast(input_image).enhance(1.5)

            # 2. Réduire le bruit
            img_np = np.array(input_image)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
            img_denoised = cv2.fastNlMeansDenoisingColored(img_bgr, None, 10, 10, 7, 21)
            input_image = Image.fromarray(cv2.cvtColor(img_denoised, cv2.COLOR_BGRA2RGBA))

            # === SUPPRESSION DU FOND ===
            session = new_session(model_name='isnet-general-use')  # <-- création de la session
            output_image = remove(input_image, session=session)  # <-- passage de la session

            # === NETTOYAGE LÉGER DES BORDS (si nécessaire) ===
            output_np = np.array(output_image)
            alpha_channel = output_np[:, :, 3]
            mask = alpha_channel > 10  # Seuillage léger
            clean_np = np.zeros_like(output_np)
            clean_np[mask] = output_np[mask]

            final_image = Image.fromarray(clean_np)

            # === ENVOI ===
            buffered = io.BytesIO()
            final_image.save(buffered, format="PNG")
            buffered.seek(0)

            return HttpResponse(buffered.getvalue(), content_type="image/png")

        except Exception as e:
            print("Erreur:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
