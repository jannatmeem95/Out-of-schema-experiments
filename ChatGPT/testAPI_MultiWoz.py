# Import the os package
import os
import json
import sys
# Import the openai package
from openai import OpenAI
client = OpenAI()

def readFile(dname, model_name):
    dir_path = dname 
    # Iterate directory
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if '.json' in os.path.join(dir_path, file_path):
            # add filename to list
            with open(os.path.join(dir_path, file_path), 'r') as f:
                data = json.load(f)
            name = file_path.split('.')[0]
            preprocess(data,name, model_name)
            
            print(name)


def preprocess(data, name, model_name):
    saved_results = dict()
    x = 0
    for dialogue in data:
        saved_results[dialogue['did']] = dict()
        prompt = ""
        t = 1
        try:
            for i in range(0, len(dialogue['turns']), 2):
                if i == 0:
                    prompt = "\"user turn "+ str(t)+ "\": \"" + dialogue['turns'][0]['utterance'] + "\"\n"
                else:
                    prompt += "\"system turn "+ str(t-1) + "\": \"" + dialogue['turns'][i-1]['utterance'] + "\"\n"
                    prompt += "\"user turn "+ str(t)+ "\": \"" + dialogue['turns'][i]['utterance'] + "\"\n"
                content= createPrompt(prompt)
                output = ChatGPTAPI(content, model_name)
                if i == len(dialogue['turns'])-2:
                    gold = "<Answer3>:Yes"
                elif len(dialogue['turns'][i]["frames"]) > 0:
                    gold = dialogue['turns'][i]["frames"][0]['state']['slot_values']
                else:
                    gold = {}
                t += 1
                saved_results[dialogue['did']][dialogue['turns'][i]["turn_id"]] = {'utterance': dialogue['turns'][i]['utterance'],'gold out': gold, 'GPT_Out': output["content"]}
                # x += 1
                # if x > 10 :
                #     break
        except:
            print(dialogue['did'])
        # if x > 10 :
        #     break
    with open('output/'+model_name+'/'+ name+'/GPT_output_'+'.json', 'w') as f:
        json.dump(saved_results, f, indent = 4)


def createPrompt(s):
    content = """
    1. Consider the following dictionary <Slots> where each key in the dictionary is used to annotate one piece of information present in a user utterance and each value best describes the meaning of the key.
        <Slots>: {"restaurant-pricerange": "terms in the sentence such as 'expensive', 'moderate', 'cheap' etc.", "restaurant-area": "the location or area of the restaurant such as 'center', 'north', 'east' etc.", "restaurant-food": "the food type of the restaurant such as 'american', 'gastropub', 'italian' etc.", "restaurant-name": "the name of the restaurant", "restaurant-bookday": "the day for which to book the restaurant such as 'Sunday', 'Monday', 'Tuesday' etc.", "restaurant-bookpeople": "the number of people to book the restaurant for such as '2', '3', '4' etc.", "restaurant-booktime": "the time for which to book the restaurant such as '7:00', '17:00' etc."}.

    2. <Dialogue> is a conversation between a user and system. Each user utterance is preceded by "user turn t" and each system utterances is preceeded by "system turn t".

    3.  For each dialogue,  your task is to answer the following three questions based on the latest user utterance:
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
    
    name = "MultiWoz"
    readFile(name, model_name)
    
main()




