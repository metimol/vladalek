from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
import json, os
from .dialog import get_generative_replica

@method_decorator(csrf_exempt, name='dispatch')
class API(View):
	def get(self, request):
		return render(request, 'jarvis/index.html')
	
	def post(self, request):
		text, name="ERROR!","Metimol"
		post_body = json.loads(request.body)
		password = post_body.get("password")
		if password==os.environ["password_jarvis"]:
			text = post_body.get("text")
			answer = get_generative_replica(text)
		data = {
			'name': name,
			'text': answer,
		}
		return JsonResponse(data)