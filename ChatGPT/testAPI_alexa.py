# Import the os package
import os
import json
import sys
# Import the openai package
from openai import OpenAI
client = OpenAI()

def readFile(name, model_name):
    with open(name + '/testlogs.json', 'r') as f:
        val_data = json.load(f)

    with open(name + '/testlabels.json', 'r') as f:
        val_labels = json.load(f)
    
    print(len(val_data))
    preprocess(val_data, val_labels, name, model_name)

def preprocess(data, labels, name, model_name):
    out = open('logOut-alexa.txt', 'w')
    saved_results = dict()
    x = 0
    id = 1
    for k in range(len(data)):
        dialogue = data[k]
        
        prompt = ""
        t = 0
        if labels[k]["target"] != True or  labels[k]["knowledge"][0]["domain"]!="restaurant": #2200 non knowledge-seeking
            continue
        try:
            saved_results[id] = dict()
            for i in range(len(dialogue)):
                if dialogue[i]['speaker'] =="S":
                    prompt += "\"system turn "+ str(t) + "\": \"" + dialogue[i]["text"] + "\"\n"
                else:
                    t+=1
                    prompt += "\"user turn "+ str(t)+ "\": \"" + dialogue[i]["text"] + "\"\n"
                       
        except:
            print(dialogue['did'])
        # if labels[k]['target']==True:
        #     gold = "<Answer3>:Yes"
        # else:
        #     gold = {}
        content= createPrompt(prompt)
        output = ChatGPTAPI(content, model_name)
        saved_results[id] = {'prompt': prompt,'gold out': "<Answer3>:Yes", 'GPT_Out': output["content"]}
        # print(f'prompt: {prompt}')
        # print(saved_results[id])
        # print('\n\n')
        out.write( prompt + '\n' + "<Answer3>:Yes" + '\n' + output["content"]+'\n')
        out.write('\n')

        if id % 50 == 0 :
            print(id)
        id+=1
    with open('output/'+model_name+'/'+ name+'/GPT_output_'+ name + '.json', 'w') as f:
        json.dump(saved_results, f, indent = 4)


def createPrompt(s):
    content = """
    1. Consider the following dictionary <Slots> where each key in the dictionary is used to annotate one piece of information present in a user utterance and each value best describes the meaning of the key.
        <Slots>: {"restaurant-pricerange": "terms in the sentence such as 'expensive', 'moderate', 'cheap' etc.", "restaurant-area": "the location or area of the restaurant such as 'center', 'north', 'east' etc.", "restaurant-food": "the food type of the restaurant such as 'american', 'gastropub', 'italian' etc.", "restaurant-name": "the name of the restaurant", "restaurant-bookday": "the day for which to book the restaurant such as 'Sunday', 'Monday', 'Tuesday' etc.", "restaurant-bookpeople": "the number of people to book the restaurant for such as '2', '3', '4' etc.", "restaurant-booktime": "the time for which to book the restaurant such as '7:00', '17:00' etc."}.

    2. <Dialogue> is a conversation between a user and system. Each user utterance is preceeded by "user turn t" and each system utterances is preceeded by "system turn t".

    3.  For each dialogue,  your task is to answer the following three questions based on the latest user uterance:
    <Question1>: Did the user provide any slot value for the slots defined in <Slots> in the latest user utterance?
    <Question2>: Did the user ask a question about any slot defined in <Slots> in the latest user utterance?
    <Question3>: Did the user ask a question about something that is not defined in <Slots> in the latest user utterance?

    Note that you must answer all three questions. And the answer to Question3 can only be 'Yes' if both the answers to Question1 and Question2 are 'No'.

        ### Start of example
        <Dialogue>: "user turn 1": "Hello, I want a restaurant in the east."\n"system turn 1": "Pizza Hut is a moderately priced restaurant in that area."\n"user turn 2":"Can you book me a table on Friday at 11:00?"
    <Answer1>: Yes. User has provided the following slot values: ["restaurant-booktime": 11:00, "restaurant-bookday": Friday]
    <Answer2>:  No.
    <Answer3>:  No.
    ### End of example


        ### Start of example
        <Dialogue>: "user turn 1": "Hello, I am looking for a restaurant in Cambridge. I believe it is called Golden Wok."\n"system turn 1": "It is located at 191 Histon Road Chesterton"\n"user turn 2":"Do they accept Amex card?"
    <Answer1>: No.
    <Answer2>:  No.
    <Answer3>:  Yes
    ### End of example


        ### Start of example
        <Dialogue>: "user turn 1": "Can you recommend a restaurant?"\n"system turn 1": "I would recommend Royal Spice in the north end. Would you like me to make a reservation there for you?"\n"user turn 2": "What's the pricerange of the restaurant?"
    <Answer1>: No.
    <Answer2>:  Yes. User has asked a question about the following slots: ["restaurant-pricerange"]
    <Answer3>:  No.
    ### End of example


    ### Start of example
    <Dialogue>: "user turn 1": "I am also looking for an international restaurant."\n"system turn 1": "There are three. Two located in the centre that are moderate in price and one in the east that is cheap."\n"user turn 2": "Can I bring my pets with me?"
    <Answer1>: No.
    <Answer2>:  No.
    <Answer3>:  Yes.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "I am looking for a restaurant. I would like something cheap that has Chinese food."
    <Answer1>: Yes. User has provided the following slot values: ["restaurant-pricerange": cheap, "restaurant-food": Chinese]
    <Answer2>:  No.
    <Answer3>:  No.
    ### End of example

    ### Start of example
    <Dialogue>: 
    """ + s
    return content


def ChatGPTAPI(content, model_name):
    completion = client.chat.completions.create(
    model= model_name, #"gpt-4",#"gpt-3.5-turbo",#
    messages=[
        {"role": "system", "content": content}
    ]
    )

    # print(completion)
    return dict(completion.choices[0].message)



def main():
    n = sys.argv[1]

    if n=="4":
        model_name = "gpt-4"
        print("gpt-4")
    else:
        model_name = "gpt-3.5-turbo"
        print("gpt-3.5-turbo")
    
    name = "alexaData"
    readFile(name, model_name)
    
main()

