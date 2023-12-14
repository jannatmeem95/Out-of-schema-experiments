# Import the os package
import os
import json
import sys
# Import the openai package
from openai import OpenAI
client = OpenAI()

def readFile(name):
    with open(name+'/D-' + name + '.json', 'r') as f:
        data = json.load(f)
    
    return data

def preprocess(data, name, model_name):
    saved_results = dict()
    x = 0
    out = open('logOut'+name+'.txt', 'w')
    for dialogue in data:
       
            saved_results[dialogue["UUID"]] = dict()
            prompt = ""
            t = 1
        
            for i in range(0, len(dialogue['turns']), 2):
                    
                    if i == 0:
                        prompt = "\"user turn "+ str(t)+ "\": \"" + dialogue['turns'][0]['utterance'] + "\"\n"
                    else:
                        prompt += "\"system turn "+ str(t-1) + "\": \"" + dialogue['turns'][i-1]['utterance'] + "\"\n"
                        if i == len(dialogue['turns'])-1:
                            prompt += "\"user turn "+ str(t)+ "\": \"" + dialogue["question"] + "\"\n"
                        else:
                            prompt += "\"user turn "+ str(t)+ "\": \"" + dialogue['turns'][i]['utterance'] + "\"\n"
                    # print(dialogue['turns'][i]['utterance'])
                    content= createPrompt(prompt)

                    output = ChatGPTAPI(content, model_name)
                  
              
                
                    if i == len(dialogue['turns'])-1:
                        gold = "<Answer3>:Yes"
                        utter = dialogue['turns'][i]["question"]
                    elif len(dialogue['turns'][i]["frames"]) > 0:
                        gold = dialogue['turns'][i]["frames"][0]['state']['slot_values']
                        utter = dialogue['turns'][i]['utterance']
                    else:
                        gold = {}
                        utter = dialogue['turns'][i]['utterance']
                    t += 1
                    saved_results[dialogue["UUID"]][str(i)] = {'utterance': utter,'gold out': gold, 'GPT_Out': output["content"]}
                    out.write( utter + '\n' + str(gold) + '\n' + output["content"]+'\n')
                    out.write('\n')
                    
            # except:
            #     print(dialogue["UUID"])
        # if x > 10 :
        # break
            x += 1
            if x%20 == 0:
                print(x)
    out.close()
    with open('output/'+model_name+'/'+ name+'/GPT_output_'+ name + '.json', 'w') as f:
        json.dump(saved_results, f, indent = 4)


def createPrompt(s):
    content = """
    1. Consider the following dictionary <Slots> where each key in the dictionary is used to annotate one piece of information present in a user utterance and each value best describes the meaning of the key.
        <Slots>: { "city_of_event": "the city or area where the event is going to take place such as 'New York City', 'London' etc.", "event_name": "the name of the event", "date": "the specific day for which to book the tickets of the event such as 'Tuesday', 'March 13th' etc.", "number_of_seats": "the number of people to book the tickets for such as '2', '3', '4' etc.", "category": "category of the event such as 'Sports', 'Music'", "subcategory": "This an exist only if the category slot has been filled. If the category of the event is 'Music', the subcategory maybe 'Jazz', 'Pop', 'Rock' etc.,  If the category of the event is 'Sports', the subcategory maybe 'Football', 'Baseball' etc."}.

    2. <Dialogue> is a conversation between a user and system. Each user utterance is preceeded by "user turn t" and each system utterances is preceeded by "system turn t".

    3.  For each dialogue,  your task is to answer the following three questions based on the latest user uterance:
    <Question1>: In the latest user utterance, did the user provide any slot value, for the slots defined in <Slots>?
    <Question2>: In the latest user utterance, did the user ask a question about any of the slots defined in <Slots>?
    <Question3>: In the latest user utterance, did the user ask a question about something that is not defined in <Slots>?

    Note that you must answer all three questions in the same order they are asked. The answer to <Question1> should start with "<Answer1>: ", answer to <Question2> should start with "<Answer2>: ", and answer to <Question3> should start with "<Answer3>: ". The answer to Question3 can only be 'Yes' if both the answers to Question1 and Question2 are 'No'. 

    ### Start of example
    <Dialogue>: "user turn 1": "I'd like to reserve tickets to an event."\n"system turn 1": "How many tickets would you like to reserve? Is there a certain event that you have in mind? Do you know when the event will occur?"\n"user turn 2":"I'd like something on Tuesday. The event is the Blue Jays Vs Indians game. I'd like four tickets."
    <Answer1>: Yes. User has provided the following slot values: ["date": "Tuesday", "event_name": "Blue Jays Vs Indians", "number_of_seats": "4"]
    <Answer2>: No.
    <Answer3>: No.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "I want to reserve two tickets for a Billy Idol event."\n"system turn 1": "In which area do you want me to search in?"\n"user turn 2": "Which acts have been opening for Billy Idol?"
    <Answer1>: No.
    <Answer2>: No.
    <Answer3>: Yes.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "I am wanting to attend some interesting events. Can you help me find some that are coming up?"
    <Answer1>: No.
    <Answer2>: No.
    <Answer3>: No.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "I want to find some neat events coming up."\n"system turn 1": "Is there any particular category, like music or sports or movies? And what city or area should I look in?"\n"user turn 2": "I'll be in Seattle. Maybe sports or games?"
    <Answer1>: Yes. User has provided the following slot values: ["category": "Sports", "city_of_event": "Seattle"]
    <Answer2>: No.
    <Answer3>: No.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "Can you help me reserve tickets for an event?"\n"system turn 1": "Do you have an invent in mind? If so what is the date?"\n"user turn 2": "Something around the 1st of this month. I think the Mets vs Braves game would be interesting."\n"system turn 2": "Is there a particular city I should search?"\n"user turn 3": "What are the last three cities where Mets and Braves played?"
    <Answer1>: No
    <Answer2>: No.
    <Answer3>: Yes.
    ### End of example

    ### Start of example
    <Dialogue>: "user turn 1": "I want to reserve two tickets for a Billy Idol event."\n"system turn 1": "In which area do you want me to search in?"\n"user turn 2": "Which city is the event taking place?"
    <Answer1>: No.
    <Answer2>: Yes. User has asked a question about the following slots: ["city_of_event"]
    <Answer3>: No.
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
    
    name = "SGD"
    data = readFile(name)
    # print(len(data))
    preprocess(data,name,model_name)

main()