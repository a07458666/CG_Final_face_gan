from django.shortcuts import render
from django.http import JsonResponse, Http404

import cv2
import base64
import torch
import numpy as np
from PIL import Image
from json import dumps, loads

from .inference import converFace
from .wing import align_face

# init models
model_dir = './PredictPage/models/'
model_name_list = ['Female2Avatar.tar', '2Fire.tar', '2MB.tar', '2Werewolf.tar']
model_list = [torch.load(model_dir + model_name) for model_name in model_name_list]
for model in model_list:
	model.eval()


# Create your views here.
def index(request):
	return render(request, 'PredictPage/index.html', {})


def cycle_gan(request):
	# to cv2 image
	json_data = loads(request.body)

	img_blob = json_data['img']

	nparr = np.array(img_blob, dtype='uint8')
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	cv2.imwrite('temp.png', img)
	pil_img = Image.open('temp.png').convert('RGB')

	'''
	# align face
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = align_face('./PredictPage/models/wing.ckpt', './PredictPage/models/celeba_lm_mean.npz', 256, img).squeeze(0).cpu().numpy()
	img = np.clip(np.swapaxes(np.swapaxes(img, 0, 1) , 1, 2) * 256, 0, 255)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).astype('uint8')
	'''

	# handle img
	img = converFace(model_list[int(json_data['model'])], pil_img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	img = 255 * (img + 1) / 2
	img.astype('uint8')

	# return base64 img
	retval, buffer = cv2.imencode('.jpg', img)
	base64_img = base64.b64encode(buffer)

	return JsonResponse({'base64_img': str(base64_img)[2:-1]})