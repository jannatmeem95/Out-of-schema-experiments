# Import the os package
import os
import json
# Import the openai package
from openai import OpenAI
client = OpenAI()

def readFile():
    dir_path = '/Users/jannatarameem/Desktop/Fall23/ChatGPT/input' #'/Users/jannatarameem/Desktop/Fall23/OQS/ModelingOQS/Modeling-OQS/data/D-MultiWoz'
  
    # Iterate directory
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if '.json' in os.path.join(dir_path, file_path):
            # add filename to list
            with open(os.path.join(dir_path, file_path), 'r') as f:
                data = json.load(f)
            name = file_path.split('.')[0]
            preprocess(data,name)
            
            print(name)
    # with open('/Users/jannatarameem/Desktop/Fall23/ChatGPT/input/dialogues_003.json', 'r') as f:
    #     data = json.load(f)
    # return data

def preprocess(data, name):
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
                output = ChatGPTAPI(content)
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
    with open('output/gpt-3.5/GPT_output_'+ name + '.json', 'w') as f:
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

def ChatGPTAPI(content):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",#"gpt-4",#
    messages=[
        {"role": "system", "content": content}
    ]
    )

    return dict(completion.choices[0].message)


readFile()


s2 = """
<Dialogue>: "user turn 1": "I am looking for a restaurant."\n"system turn 1": "Is there a price range or type of food that you would prefer?"\n"user turn 2 ": "Not sure of that, I am looking for a restaurant named 'ask'."\n"system turn 2": "That is an Italian restaurant located in the centre of town. It is at 12 Bridge Street. Can I call and reserve a table for you?"\n"user turn 3": "I would like to book a table for 5 people on Sunday at 14:15."\n"system turn 3": "I am afraid that booking was unsuccessful. Would you like to try another restaurant?"\n"user turn 4": "Yes, a different restaurant in the same area and with the same price range."\n"system turn 4": "Yes there are 15 restaurants that are a similar price range. Did you still want Italian?"\n"user turn 5": "Is there any bar available in the area?"
<Answer1>: 
"""

s1 = """
    <Dialogue>: "user turn 1": "I'm looking for a place to eat. I would like it to be an expensive restaurant in the centre."\n"system turn 1": "I found 33 expensive restaurants in the centre. What type of cuisine would you like?"\n"user turn 2": "I'm looking for a restaurant with mediterranean food."\n"system turn 2": "I have found two restaurants. One is La mimosa, and the other is Shiraz restaurant, would you like me to book one for you?"\n"user turn 3": "Please book the One is La mimosa."\n"system turn 3": "Can I please get the number of people dining,day,and time please."\n"user turn 4": "Yes, it's for 8 people. 16:45 on Monday. I would like the reference number, if it is available."
    <Answer1>:
"""
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )


# openai.api_key = "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"
# model_id = "gpt-3.5-turbo"
# completion = openai.ChatCompletion.create(
# model=model_id,
# messages=[
# {"role": "user", "content": "Where was the last Olympics held? Just tell me the year & country?"}
# ]
# )
# print(completion.choices[0].message.content)