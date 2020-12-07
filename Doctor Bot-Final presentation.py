#!/usr/bin/env python
# coding: utf-8

# In[1]:


from newspaper import Article
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS 
import os 
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pyaudio
import speech_recognition as sr
import statistics 
import matplotlib.pyplot as plt


# In[22]:


nltk.download('punkt', quiet=True)
### website from where we want to extract the data
article1 = Article('https://www.unicef.org/india/coronavirus/covid-19')
article1.download()
article1.parse()
article1.nlp()


# In[23]:


article2 = Article('https://www.who.int/health-topics/coronavirus#tab=tab_1')
article2.download()
article2.parse()
article2.nlp()


# In[24]:


article3 = Article('https://www.euro.who.int/en/health-topics/noncommunicable-diseases/mental-health/data-and-resources/mental-health-and-covid-19')
article3.download()
article3.parse()
article3.nlp()


# In[25]:


article4 = Article('http://www.emro.who.int/health-topics/corona-virus/about-covid-19.html')
article4.download()
article4.parse()
article4.nlp()


# In[26]:


article5 = Article('https://www.helpguide.org/articles/depression/dealing-with-depression-during-coronavirus.htm')
article5.download()
article5.parse()
article5.nlp()


# In[27]:


article6 = Article('https://www.hopkinsmedicine.org/health/conditions-and-diseases/coronavirus')
article6.download()
article6.parse()
article6.nlp()


# In[28]:


article7 = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')
article7.download()
article7.parse()
article7.nlp()


# In[29]:


article8 = Article('https://www.longdom.org/special-issue/mental-health-and-depression-during-covid19-991.html')
article8.download()
article8.parse()
article8.nlp()


# In[30]:


article9 = Article('https://link.springer.com/article/10.1007/s10389-020-01325-9')
article9.download()
article9.parse()
article9.nlp()


# In[31]:


article10 = Article('https://theprint.in/opinion/india-lost-more-jobs-due-to-coronavirus-lockdown-than-us-did-during-depression/397693/')
article10.download()
article10.parse()
article10.nlp()


# In[32]:


article11 = Article('https://theconversation.com/covid-19-could-lead-to-an-epidemic-of-clinical-depression-and-the-health-care-system-isnt-ready-for-that-either-134528')
article11.download()
article11.parse()
article11.nlp()


# In[33]:


article12 = Article('https://link.springer.com/article/10.1007/s10668-020-00739-5')
article12.download()
article12.parse()
article12.nlp()


# In[34]:


corpus = article1.summary + article2.summary + article3.summary + article4.summary + article5.summary + article6.summary + article7.summary + article8.summary + article9.summary + article10.summary + article11.summary + article12.summary
sentence_list = nltk.sent_tokenize(corpus)
len(sentence_list)


# In[35]:


question_dict = {"who","what","where","when","why","how","which","?"}
length = len(sentence_list)
list_index = list(range(0, length))


# In[36]:


len(sentence_list)


# In[37]:


def greeting_response(text):
  text = text.lower()

  #Bots respnse
  bot_greetings = ["hi","hey","hello","hey there"]
  #Users Greeing
  user_greeting = ["hi","hello","greetings","wassup","hey","hey there"]
  info = ["how are you","how have you been"]

  for word in text.split():
    if word in user_greeting:
      return random.choice(bot_greetings)+", tell me how can I help you"
  for word in text.split():
    if word in user_greeting:
      return random.choice(bot_greetings)+", tell me how can I help you"
      

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]]>x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index

def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response=""
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1],cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)  
  response_flag = 0
  z=0  
  j=0
  for i in range(1,len(index)):    
    if similarity_scores_list[index[i]] > 0.0 and sentence_list[index[i]]!=user_input and z<=3:
      bot_response = bot_response +" "+ sentence_list[index[i]]
      z=z=1
      y.append(similarity_scores_list[index[i]])
      response_flag = 1
      j = j+1
    if j > 2:
      scores.append(statistics.mean(y)) 
      break

  if response_flag==0:
    bot_response = bot_response+" "+"I apologise, I don't Understand."
    scores.append(0)
  sentence_list.remove(user_input) 
    
  return bot_response


# In[38]:


print("Doctor Bot")
Question=[]
Answer = []
scores=[]
while(True):
    y=[]
    exit_list = ["exit", "see you later", "bye", "break", "quit"]
    r=sr.Recognizer()
    r.energy_threshold=4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        r.dynamic_energy_threshold = True 
        s=("Speak now")
        language = 'en'
        myobj = gTTS(text=s, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        playsound("welcome.mp3") 
        os.remove("welcome.mp3")
        print('Bot: '+s)

        audio=r.listen(source,timeout=40,phrase_time_limit=40)
        user_input=r.recognize_google(audio)
        print("YOU: "+ user_input)

    if user_input.lower() in exit_list:
        res = ("BOT: Bye, Chat with you later")
        language = 'en'
        myobj = gTTS(text=res, lang=language) 
        myobj.save("welcome.mp3") 
        playsound("welcome.mp3") 
        os.remove("welcome.mp3")
        print(res)
        scores.append(0)
        Question.append(user_input)
        Answer.append(res)
        break
    
    else:
        if greeting_response(user_input) != None:
            res = (greeting_response(user_input))
            scores.append(0)
        else:
            res = (bot_response(user_input))
    language = 'en'
    myobj = gTTS(text=res, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
    print('Bot:'+res)
    playsound("welcome.mp3") 
    os.remove("welcome.mp3")
    Question.append(user_input)
    Answer.append(res)


# In[ ]:


import pandas as pd
df = pd.DataFrame(list(zip(Question, Answer, scores)), 
               columns =['Question', 'Answer', 'Similiarity Scores']) 
df 
df.to_csv('5.csv') 


# In[ ]:


df


# In[ ]:


x=[]
for i in range(1,len(scores)+1):
    x.append(i)
plt.style.use('seaborn')
plt.title("Similiarity Score Graph")
plt.xlabel("Question No.")
plt.ylabel("Similiarity Between Question and Answer")
plt.plot(x,scores,color='black')
plt.scatter(x,scores,color='orange')


# In[ ]:


statistics.mean(scores)


# In[ ]:





# In[ ]:




