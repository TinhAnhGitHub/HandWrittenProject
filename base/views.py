from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CanvasImage
from PIL import Image
import base64
from io import BytesIO
import json
from django.core.files.base import ContentFile
from .LeNet import LeNet5
from torch import load, device
from torchvision import transforms
from numpy import argmax
from pathlib import Path

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

img_url = None
pred_number = None
pred_list = []
init_pred_list = [0 for i in range(0,10)]

def get_image_from_data_url(data_url):
    _format, _dataurl = data_url.split(';base64,')
    _filename, _extension = 'digit_picture', 'png'
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
    return file 
@csrf_exempt
def ProjectOne(request):
    print(request.method)
    if request.method == 'POST':
        if 'submit-canvas' in request.POST:
            global img_url
           
            img_url = request.POST.get('image') 
            imgdata = get_image_from_data_url(img_url) 
            PATH = Path.cwd();
            model = LeNet5(num_classes=10)
            model.load_state_dict(load(PATH / 'base/LeNet.pt', map_location=device('cpu')))

            data = Image.open(imgdata).convert("L")
            resize_transform = transforms.Compose(
                [transforms.Resize((32, 32)),
                transforms.ToTensor(),
                transforms.Normalize((0,), (1,))  # standarize data with zero means and unit variance
                ]
            )
            data = resize_transform(data)
            if data.sum() == 0:
                context = {'result': "Blank canvas - No prediction", 'img_url': img_url, 'print': False, 'pred_list': init_pred_list}
            else:
                data = data.unsqueeze(0)
                _, output = model(data)

                output = output.tolist()[0]
        
                global pred_list
                pred_list = output

                print(pred_list)
                print(type(pred_list))
                prediction = argmax(output)

                global pred_number
                pred_number = prediction

                context = {'result': "Your image produces number " + str(prediction), 'img_url': img_url,'print': True, 'pred_list': pred_list}
            
            return render(request, '../templates/ProjectOneComponents/HomeTwo.html', context= context)
        elif 'error-detect' in request.POST:
            context = {
                'img_url' : img_url,
                'pred_list_print': True,
                'pred_list': pred_list
            }
            return render(request, '../templates/ProjectOneComponents/Detect.html',context=context)
        elif 'confirm-detect' in request.POST:
            imgdata = get_image_from_data_url(img_url)
            img = CanvasImage.objects.create(
                image = imgdata,
                result = request.POST.get("correct_number"),
                predict = str(pred_number),

            )
            img.save()
            black_canvas = Image.new("L", (280, 280), 0)

            black_canvas_url = image_to_data_url(black_canvas)

            
            context = {'result': "Blank canvas", 'img_url': black_canvas_url, 'pred_list': init_pred_list}
            return render(request, '../templates/ProjectOneComponents/HomeTwo.html', context=context )
    else:
        
        black_canvas = Image.new("L", (280, 280), 0)

        black_canvas_url = image_to_data_url(black_canvas)
        
        context = {'result': "Blank canvas", 'img_url': black_canvas_url, 'print': False, 'pred_list' : json.dumps(init_pred_list)}
        return render(request, '../templates/ProjectOneComponents/HomeTwo.html', context=context)

    return render(request, 'Project1.html')


def image_to_data_url(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"






