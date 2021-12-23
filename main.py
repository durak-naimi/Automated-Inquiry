''''''
'''--------------------------Automated Inquiry System - Using Azure AI------------------------------------------'''

import json
import azure.cognitiveservices.speech as speechsdk
import load
import os
import requests
from requests.structures import CaseInsensitiveDict
from decouple import config
from pytz import timezone
from datetime import datetime

'''--------------------------------SPEECH RELATED CODE------------------------------------------------------------------'''
user_word = input("press enter to continue")



def Trigger():


    speech_config = speechsdk.SpeechConfig(subscription=config("speech_subs"), region=config("speech_region"))
    #speech_config.endpoint_id = config("speech_endpoint")


    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print('\n' + '\n'+"Welcome To Indian Railway Automated Inquiry System" + '\n' )

    print("You can use this platform to get information of train timing, station platform and next train to a location \n")

    print("Speak into the mic to get information")


    result = speech_recognizer.recognize_once()

    ndb = open("read.json", mode='w')
    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # ndb.write("Recognized: {}".format(result.text)+ '\n' )
        ndb.write('{"statement" : ' + '"' + result.text + '"}')
    elif result.reason == speechsdk.ResultReason.NoMatch:
        ndb.write('{"statement":' + '"'+"No speech could be recognized: {}".format(result.no_match_details) + '"' '}')
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason) + '\n')
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            ndb.write("Error details: {}".format(cancellation_details.error_details) + '\n')

    '''---------------------------------------LUIS CODE ----------------------------------------------'''


    inputus=load.value

    response = requests.get(config("luis_api")+result.text, auth=('user', 'password'))

    data = response.json()



    Intent=(data['prediction']['topIntent'])



    R2=(data['prediction']['entities'])

    R3=str(R2).split(':')


    R4=str(R3).split(',')



    if len(R4)<3:
        R5=R4[1]
    else:
        R5=R4[3]

    R6= str(R5).split("'")
    Entity= R6[1]






    Question =str(Intent) + " " +  str(Entity)


    print("Intent  + entity  = Question:")

    print(str(Intent) + " + " + str(Entity) + " = " + str(Question))


    '''----------------------------------------QNA MAKER CODE------------------------------------------------------------'''


    url = config("qna_url")

    headers = CaseInsensitiveDict()
    headers["Authorization"] = config("qna_authorisation")
    headers["Content-type"] = "application/json"



    data = "{'question':'<"+str(Question)+">'}"


    resp = requests.post(url, headers=headers, data=data)
    answer=resp.text

    now = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M')

    if Intent=="GetPlatform":
        answer2=answer.split(':')
        answer3=answer2[3]
        answer4=answer3.split(',')
        finalanswer= answer4[0]
        print(finalanswer)

    elif Intent=='GetTime':
        answer2 = answer.split(':')
        answer3=answer2[4].split(',')
        finalanswer=str(answer2[3]+ ' : ' + str(answer3[0]))
        print(finalanswer)

    elif Intent=='GetTrain':
        answer2=answer.split('|')
        length = len(answer2)



        i=1
        trains=[]
        while i<(length-1):
            trains.append(answer2[i])
            i=i+1


        totaltrains = len(trains)

        nowhour = int(now.split(':')[0])
        nowminute = int(now.split(':')[1])


        i = 0

        hourlist = []

        while i < totaltrains:
            hourlist.append(trains[i].split('-')[1])
            i = i + 1



        j = 0

        timedifflist = []
        while j < totaltrains:
            hour = int(hourlist[j].split(':')[0])
            minute = int(hourlist[j].split(':')[1])
            diff= hour - nowhour

            if diff<0:
                timediff=diff + 24
                timedifflist.append(timediff)

            elif diff==0:
                if minute > nowminute:
                    timediff = 0
                    timedifflist.append(timediff)
                else:
                    timediff = 24
                    timedifflist.append(timediff)
            else:
                timediff=diff
                timedifflist.append(timediff)

            j = j + 1

        k = 0
        while k < totaltrains:
            if timedifflist[k] == min(timedifflist):
                finalanswer= trains[k].split('-')[0] + ' at ' + trains[k].split('-')[1]
                break
            k = k + 1


        print('\n' + str(finalanswer))

while user_word!='Exit':
    try:
        Trigger()
    except KeyError:
        print("please try again")
    except IndexError:
        print("please try again")
