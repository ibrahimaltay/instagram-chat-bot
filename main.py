from selenium import webdriver
# from chatbot import GetResponse
import time
import os

USERNAME = ''
# Assign your password as a string to the PASSWORD variable instead of using environment variables.
# For example:
# PASSWORD = 123456
PASSWORD = os.getenv("FLASK_PASSWORD")

browser = webdriver.Chrome()

def start():
    browser.get('https://instagram.com/direct/inbox')
    time.sleep(5)
    browser.find_element_by_xpath("//input[@name=\"username\"]").send_keys(USERNAME)
    time.sleep(0.3)
    browser.find_element_by_xpath("//input[@name=\"password\"]").send_keys(PASSWORD)
    time.sleep(0.5)
    browser.find_element_by_xpath("//button[@type='submit']").click()


def dont_remember_me(): 
	not_now_btn = browser.find_elements_by_css_selector('button')[1]
	not_now_btn.click()

def dont_allow_notifications():
    not_now_btn = browser.find_element_by_xpath("//button[contains(text(),'Not Now')]")
    #not_now_btn = browser.find_element_by_xpath("//button[contains(text(),'Şimdi Değil')]")
    not_now_btn.click()

def Botify(x):
	print("botify entered")
	try:
		ret = '"' + str(x) + "''"
	 	
	except Exception as e:
		print(e)  
	print("string altered")
	return ret

def SendMessage(resp):
	print("yolla received")
	typeArea = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
	print("typearea found")
	typeArea.send_keys(Botify(resp))
	print("sent keys to area")
	print("sending text", resp)
	time.sleep(1)
	sendBtn = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button")
	print("sendbtn clicked")
	sendBtn.click()

def get_dm_box(n):
	try:
		dm_box = browser.find_element_by_xpath(f'/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div[{n}]')
		return dm_box
	except Exception as e:
		print(e)
		print('ChatBox not Found!')
		return None
def get_dm_box_count():
	dm_box_list = browser.find_elements_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div')
	return len(dm_box_list)-1

def check_if_unread_messages(box):
	blue_dot_list = box.find_elements_by_css_selector('a > div > div')
	# print(len(blue_dot_list))
	if len(blue_dot_list) == 3:
		return True
	else:
		return False

def read_messages():
	message_area = browser.find_elements_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div')
	ret = []
	for message in message_area:
		try:
			if message.text[0] == '"' and message.text[-1] == "'" and message.text[-2] == "'":
				ret.clear()
				continue
			elif message.text[2] == ":":
				ret.clear()
				continue
			elif message.text.lower() in ["dün","pazartesi","salı","çarşamba", "perşembe", "cuma","cumartesi","pazar"]:
				ret.clear()
				continue
		except Exception as e:
			continue
		
		try:
			if message.text in ret:
				continue
		except Exception as e:
			raise e
		
		ret.append(message.text)
		# print(message.text)
	return ' '.join(ret)


def loop_chats():
	while True:
		for i in range(1, get_dm_box_count()+1):
			dm_box = get_dm_box(i)
			if check_if_unread_messages(dm_box):
				dm_box.click()
				time.sleep(1)
				for _ in range(20):
					if is_typing():
						time.sleep(2)
				messages = read_messages()
				SendMessage('This is sad :(')
				time.sleep(1)
				browser.back()
				time.sleep(1)
			else:
				continue
		print('Checked All Messages!')
		browser.get('https://instagram.com/direct/inbox')
		time.sleep(3)

def is_typing():
	Messages = browser.find_elements_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div")
	if Messages[-1].text == 'Yazıyor...':
		return True
	else:
		return False
	

# def accept_message_requests():
# 	dm_requests = browser.find_element_by_xpath('//button[contains(text(),"İstekler")]')
# 	if dm_requests:
# 		dm_requests.click()
		




start()
time.sleep(5)
dont_remember_me()
time.sleep(3)
dont_allow_notifications()
time.sleep(2)
loop_chats()
