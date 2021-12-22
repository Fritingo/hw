# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import threading

from Dummy_Device_IoTtalk_v1_py.csmapi import tree

line_bot_api = LineBotApi('86N4wsFGNnA3eEO/dxa9ZW6w2ppkQkXvtrLK5Nf/8f0bF+tPnmQjOPXinpdbAkFgbem0qeu7/vAFdqd0SgbtoqtIcNbKtOLwtBCsO59/pxArCcJeeDJv/esm+yU4m4jSdT2l6LdJU9HfPPazebDGHwdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('003b158fecd2ff1bee201e213c172b93')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)

#============line init============

#============dummy device init=========
import time, random, requests
import DAN

ServerURL = 'https://6.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = '1demo310832007' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='linebot'
DAN.profile['df_list']=['linebot-I', 'linebot-O',]
DAN.profile['d_name']= '310832007' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)

notify_state = True


#============dummy device init=========

#============dummy device loop=========
def dummy_device_loop():
    while True:
        try:
            # IDF_data = random.uniform(1, 10)
            # DAN.push ('linebot-I', IDF_data) #Push data to an input device feature "Dummy_Sensor"

            #==================================

            ODF_data = DAN.pull('linebot-O')#Pull data from an output device feature "Dummy_Control"
            if ODF_data != None:
                print (ODF_data[0])
                if ODF_data[0] != 'stop':
                    line_bot_api.push_message(userId, TextSendMessage(text=str(ODF_data[0])))

                #     notify_state = False
                # elif ODF_data[0] == 'open':
                #     notify_state = True
                # else:
                #     if ODF_data[0] == '好熱' and notify_state == True:
                #         line_bot_api.push_message(userId, TextSendMessage(text='好熱'))
                #     elif ODF_data[0] != '好熱':
                #         line_bot_api.push_message(userId, TextSendMessage(text=str(ODF_data[0])))

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    

        time.sleep(0.2)




#============dummy device loop=========

def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text

    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))
    DAN.push ('linebot-I', Msg)

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!")) 
      # Reply API example
    
    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

   
if __name__ == "__main__":
    dummy_threading = threading.Thread(target= dummy_device_loop)
    dummy_threading.start()

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    

