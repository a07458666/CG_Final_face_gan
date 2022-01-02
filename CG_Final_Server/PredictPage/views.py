from django.shortcuts import render
from django.http import JsonResponse, Http404

import cv2
import base64
import torch
import numpy as np
from json import dumps, loads

from .inference import converFace

model_list = [
    torch.load('./PredictPage/model/v1.pth.tar')
]

# Create your views here.
def index(request):
	return render(request, 'PredictPage/index.html', {})

def cycle_gan(request):
	# to cv2 image
	json_data = loads(request.body)

	img_blob = json_data['img']

	nparr = np.array(img_blob, dtype='uint8')
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	# handle img
	img = converFace(model_list[int(json_data['model'])], img)
	img = np.clip(img*256, 0, 255)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	import matplotlib.pyplot as plt
	# plt.imshow(img)
	# plt.show()

	# return base64 img
	retval, buffer = cv2.imencode('.jpg', img)
	base64_img = base64.b64encode(buffer)

	return JsonResponse({'base64_img': str(base64_img)[2:-1]})