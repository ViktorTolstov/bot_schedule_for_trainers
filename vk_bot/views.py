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
				message = "Выбери предложенное действие"
				send_keyboard(body,message)
			elif body["object"]["message"]["payload"] == '{"command":"shedule"}':
				send_shedule(body)
			elif body["object"]["message"]["payload"] == '{"command":"add"}':
				add_shedule(body)
		elif body["object"]["message"]["text"].find("new",0,3)!=-1:
			add_new(body)
	return HttpResponse("ok")

def send_keyboard(body,message):
	user_id = body["object"]["message"]["from_id"]
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
	message = "Рассписание на " + today + ":\n\n"
	print(fields)
	for field in fields:
		message += "Тренировка: " + field[4] + ";\n"
		message += "Тренер: " + field[1] + ";\n"
		message += "Время: " + field[2] + " " + field[3] + ";\n\n"
	send_keyboard(body,message)

def add_shedule(body):
	user_id = body["object"]["message"]["from_id"]
	message = """Добавь новую запись в формате:
	new/Имя тренера/время/дата/тип тренировки
	
	Например:
	new/Иванов И.И/17:30/18.03.2020/Бокс
	"""	
	random_id = int(str(round(time.time()))+str(user_id))
	vk_api.messages.send(user_id=user_id, message=message, random_id=random_id ,v=5.103)

def add_new(body):
	data = body["object"]["message"]["text"].split("/")
	print(data)
	data_date = data[3].split(".")
	database.add_field(data[1],data[2],str(datetime.date(int(data_date[2]),int(data_date[1]),int(data_date[0]))),data[4])
	user_id = body["object"]["message"]["from_id"]
	message = "Новая запись успешно добавлена"
	send_keyboard(body,message)