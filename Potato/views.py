import tensorflow as tf
import os
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai

openai_Secret_key ="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"

openai.api_key = openai_Secret_key


class_names = ['Early blight', 'Late blight', 'Healthy']

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow import keras
from keras.preprocessing import image
import numpy as np
from PIL import Image

earlyInfo = [
    {
        "recommendations": [
            {"Early Detection": "Regularly inspect your potato plants for symptoms of early blight, which include dark, irregularly shaped lesions on the leaves. Early detection allows for prompt action."},
            {"Pruning and Removal": "Remove and destroy infected leaves as soon as you spot them. This helps prevent the disease from spreading to healthy parts of the plant."},
            {"Fungicide Treatment": "Consider applying a fungicide specifically designed for early blight. Follow the manufacturer's instructions for application timing and rates."},
            {"Crop Rotation": "Practice crop rotation to reduce the buildup of disease in the soil. Avoid planting potatoes or other solanaceous crops (e.g., tomatoes) in the same location for at least two years."},
            {"Spacing and Ventilation": "Ensure proper spacing between potato plants to promote air circulation, which can reduce humidity and slow the spread of the disease."},
            {"Irrigation Management": "Water your potato plants at the base to keep the foliage dry. Damp foliage can encourage disease development."},
            {"Mulching": "Apply a layer of organic mulch to the soil around the plants to prevent soil from splashing onto the leaves, which can carry the disease."},
            {"Resistant Varieties": "Consider planting potato varieties that are known to be resistant to early blight."},
            {"Good Sanitation": "Clean your tools and equipment to prevent the spread of the disease between plants and fields.",}
        ]
    },
    {
        "background": [
            {"Background": '''
            Early blight disease, scientifically known as Alternaria solani, is a common and destructive fungal disease that affects potato plants (Solanum tuberosum) 
            as well as other solanaceous plants such as tomatoes. It can lead to reduced yields and lower quality tubers. Early blight is caused by the fungus Alternaria 
            solani and is typically more prevalent in warm and humid conditions.'''
            },
            {"Symptoms": '''
            Early blight primarily affects the leaves of potato plants. Symptoms typically 
            appear on the lower leaves first and may include small, dark brown to black circular lesions 
            with concentric rings. These lesions can grow larger and often have a target-like appearance. 
            As the disease progresses, leaves may turn yellow, wither, and eventually die. Infected tubers 
            can also develop shallow, sunken, dark lesions.
            '''
            },
            {"Spread": '''
            The fungus responsible for early blight can survive in the soil and on infected 
            plant debris. It can be spread by wind, rain, irrigation, and through contact with infected 
            plant material. The disease often starts on older, lower leaves and can move upward in the 
            plant canopy.
            '''
            }
        ]
    }
]


model_filename = 'potatoes.h5'
model_path = os.path.join("Potato", "trained_model", "models", model_filename)
model = keras.models.load_model(model_path)

def preprocess_image(uploaded_image):
    img = Image.open(uploaded_image)
    img = img.resize((256, 256))  # Resize the image to match the model's input size
    img_array = np.array(img) / 255.0  # Normalize the image data if needed
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

    

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        sent_image = request.FILES.get('image')

        try:
            im = preprocess_image(sent_image)
            result = model.predict(im)
            confidence = tf.reduce_max(result).numpy() * 100
            predicted_class = class_names[np.argmax(result)]
            early= late= healthy = False
            if predicted_class == class_names[0]:early=True
            elif predicted_class == class_names[1]:late=True
            else: healthy = True


            return JsonResponse({
                'confidence': "{:.2f}%".format(confidence),
                'early': early,
                'late': late,
                'healthy':healthy,
                'documentation': earlyInfo
                })
        except Exception as e:
            # Handle any exceptions that might occur during image processing or prediction
            print("Prediction error:", str(e))
            return JsonResponse({'message': 'Error processing the image.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})


def index(request):
    return render(request, 'Potato/html/base.html')

def askAgribot(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are AgriBot, a multilingual AI assistant expert in Agriculture trained by USIU AgriTech Team"},
            {"role": "user", "content":message},
        ]
    )
    
    answer = response.choices[0].message.content
    return answer

    

def agribot(request):
    if request.method == 'POST':
        message = request.POST['message']
        response = askAgribot(message)
        
        return JsonResponse({
            "response": response,
        })
    return render(request, 'Potato/html/agribot.html')
