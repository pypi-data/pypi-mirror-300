from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import uuid

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        filename = f"{uuid.uuid4().hex}{os.path.splitext(image.name)[1]}"
        filepath = os.path.join(settings.MEDIA_ROOT, 'markdown_uploads', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        url = f"{settings.MEDIA_URL}markdown_uploads/{filename}"
        return JsonResponse({'url': url})
    
    return JsonResponse({'error': 'No image provided'}, status=400)