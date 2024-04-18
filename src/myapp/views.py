
        
import os
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import cv2
import easyocr
from django.conf import settings
from subprocess import run, PIPE

# Constants
SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'images'))

LANGUAGE = ['en']  # Language for EasyOCR
 


def detect_text_in_image(image_path):
    try:
        # Read image
        img = cv2.imread(image_path)

        # Detect text on image using EasyOCR
        reader = easyocr.Reader(LANGUAGE)
        text_results = reader.readtext(img)

        return text_results
    except Exception as e:
        print(f"Error detecting text: {e}")
        return []

def process_text_results(text_results):
    try:
        # Process the text results to generate a response
        response_text = ' '.join([text_result[1] for text_result in text_results])
        return response_text
    except Exception as e:
        print(f"Error processing text results: {e}")
        return ""

class ImageOCRView(views.APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Check if the request contains an image
            if 'image' in request.FILES:
                image = request.FILES['image']

                # Ensure the save directory exists, create it if it doesn't
                os.makedirs(SAVE_DIR, exist_ok=True)

                # Define the path to save the image
                save_path = os.path.join(SAVE_DIR, image.name)

                # Open the file and write the image data
                with open(save_path, 'wb') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Detect text on the saved image using EasyOCR
                text_results = detect_text_in_image(save_path)

                # Process the text results to generate a response
                response_text = process_text_results(text_results)

                # Execute script.sh to generate audio based on response_text
                script_path = os.path.join(settings.BASE_DIR, 'script.sh')
                process = run(['sh', script_path], stdout=PIPE, input=response_text, text=True)


                # Get the generated audio file name from the script output
                audio_file_name = process.stdout.strip()

                # Construct the absolute path of the audio file
                audio_file_path = os.path.join(os.path.expanduser('~/Desktop/alpha/VALL-E-X'), audio_file_name)
                return Response(
                    {
                        'message': 'Image saved and processed successfully',
                        'text': response_text,
                        'audio_file': audio_file_path
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({'error': 'No image found in the request'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error processing image: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
