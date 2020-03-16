from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import vk
import random
import database
import time
import datetime

session = vk.Session(access_token='bd474e72f9fd5b28da782dbdd5fc1f3b1832bc10566d57ed68a74e9f18cdede0d81ea8335c11f532259c3')
vk_api = vk.API(session)

@csrf_exempt
def init(request):
	body = json.loads(request.body)
	if body == { "type": "confirmation", "group_id": 188996934 }:
		return HttpResponse("8806c6d6")

@csrf_exempt
def main_api(request):
	body = json.loads(request.body)
	if body["type"] == 'message_new':
		if "payload" in body["object"]["message"]:
			if body["object"]["message"]["payload"] == '{"command":"start"}':
				start(body)
			elif body["object"]["message"]["payload"] == '{"command":"shedule"}':
				send_shedule(body)
			elif body["object"]["message"]["payload"] == '{"command":"add"}':
				add_shedule(body)
	return HttpResponse("ok")

def start(body):
	user_id = body["object"]["message"]["from_id"]
	message = "Выбери предложенное действие"
	keyboard = {
		"one_time": True,
		"buttons": [
			[{
					"action": {
						"type": "text",
						"payload": '{"command":"shedule"}',
						"label": "Текущее рассписание"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command":"add"}',
						"label": "Добавить новое занятие"
					},
					"color": "primary"
				}
			]
		]
	}
	random_id = int(str(round(time.time()))+str(user_id))
	vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(keyboard), random_id=random_id ,v=5.103)

def send_shedule(body):
	user_id = body["object"]["message"]["from_id"]
	today = str(datetime.datetime.today().date())
	fields = database.get_field(today)
	message = "Рассписание на " + today + ":\n"
	print(fields)
	for field in fields:
		print(field)
		for data in field:
			message += str(data) + " "
		message += ";\n"	
	random_id = int(str(round(time.time()))+str(user_id))
	vk_api.messages.send(user_id=user_id, message=message, random_id=random_id ,v=5.103)

# def add_shedule(body):
# 	user_id = body["object"]["message"]["from_id"]
# 	today = str(datetime.datetime.today().date())
# 	fields = database.get_field(today)
# 	message = "Рассписание на " + today + ":\n"
# 	for field in fields:
# 		for data in field:
# 			message += data + " "
# 		message += ";\n"	
# 	random_id = int(str(round(time.time()))+str(user_id))
# 	vk_api.messages.send(user_id=user_id, message=message, random_id=random_id ,v=5.103)