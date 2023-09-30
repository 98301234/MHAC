import speech_recognition as sr
import pyttsx3
import datetime
from SentenceSegmenter import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
def log(tts,stt):#To save conversations
    tl=[]
    sl=[]
    tl.append(tts)
    sl.append(stt)
    with open("logfile.txt","a+") as logfile:
        logfile.writelines(str(datetime.datetime.now())+'\n')
        logfile.writelines(str(tl)+'\n')
        logfile.writelines(str(sl)+'\n')
def speak(x):#text-to-speech engine
    print("MHAC: ",x)
    a=pyttsx3.init()
    voices=a.getProperty('voices')
    a.setProperty('voice',voices[1].id)
    a.setProperty('rate',140)
    a.say(x)
    log(x,"")
    a.runAndWait()
def listen():#Speech-to-text-engine
    recognizer = sr.Recognizer()
    max_attempts = 2  # Maximum number of recognition attempts
    for _ in range(max_attempts):
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Adjust the timeout as needed
            words = recognizer.recognize_google(audio)
            log("",words)
            print("You:", words)
            break  # Break out of the loop if recognition is successful
        except sr.WaitTimeoutError:
            speak("No speech detected. Please speak.")
        except sr.UnknownValueError:
            speak("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Speech recognition request failed: {str(e)}")
    else:
        speak("Sorry I couldn't hear you, please enter your answer below:")
        words=input("You: ")
    return words
#System
time=datetime.datetime.now().date()
speak("I'm Mental Health Analysis Chatbot")
speak("Enter your name below:")
name=input()
speak("I'm going to ask you some questions, please answer accordingly")
file="Analysis_Report "+name+".pdf"
c = canvas.Canvas(file, pagesize=letter)
questions=["How are you feeling lately?",
           "Do you feel overwhelmed by your studies?",
           "What do you like to do in your free times?",
           "Do you have a proper six to eight hour sleep?",
           "What are your future aspirations?",
           "Do you get mental support from your parents?",
           "Do you feel pressurized by your parents or academic system?"]
answers=[]
for q in questions:
    speak(q)
    a=listen()
    answers.append(a)
#analysis
score=0
anlanswers=[{"fine":10,"stressed":-10,"underconfident":-10,"hopeless":-10},
            {"yes":-5,"no":5,"never":5},
            {},
            {"yes":5,"no":-5,"never":-5},
            {},
            {"yes":5,"no":-5,"never":-5},
            {"yes":-5,"no":5,"never":5}]
for i in range(len(answers)):
    c.drawString(50,600-(20*i),questions[i])
    if len(anlanswers)>0:    
        for j in ss(answers[i]):
            if j in anlanswers[i]:
                score+=anlanswers[i][j]
            else:
                c.drawString(400,600-(20*i),answers[i])
speak("Share your worries and problems with the people you trust")
speak("Thanks for your patience and have a nice day ahead")
if score<-20:
    remark="Highly stressed and needs mental support"
elif (score>-20) and score<20:
    remark="Moderate stress"
else:
    remark="Low stress"
c.drawString(40,420,"Comments:-")
c.drawString(50,390,"Mental score:"+str(score)+"         scale(-30 to +30)")
c.drawString(50,350,"The student condition: "+remark)
c.drawString(50,682,"Student's name: "+name)
c.drawString(450,700,"Date: "+str(time))
c.drawString(46,640,"Questions Asked:-")
c.drawString(400,640,"Student's responses:-")
c.setFont("Helvetica-Bold", 30)
c.drawString(200, 750, "Analysis Report")
c.save()