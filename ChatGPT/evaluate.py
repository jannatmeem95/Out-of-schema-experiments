import json
import os



def check(data):
    truth = 0
    correct_pred = 0
    for key, val in data.items():
        for turn_id, v in val.items():
            if v["gold out"] == "<Answer3>:Yes":
                truth += 1
                if "<Answer3>:Yes" in v["GPT_Out"]:
                    correct_pred += 1

    return truth, correct_pred


def checkAlexa(data):
    truth = 0
    correct_pred = 0
    for key, val in data.items():
        if val["gold out"] == "<Answer3>:Yes":
            truth += 1
            if "<Answer3>:Yes" in val["GPT_Out"]:
                correct_pred += 1

    return truth, correct_pred


class Metric:
    def __init__(self):
        self.reset()

    def reset(self):
        self._detection_tp = 0.0
        self._detection_fp = 0.0
        self._detection_tn = 0.0
        self._detection_fn = 0.0
        self.tmpSet = set()
    
    def update(self, obj, id, turn):
        tmp = obj["GPT_Out"].split('<Answer3>:')
        try:
            pred = tmp[1].strip().split(' ')[0].strip().strip('.')
            # if pred != "Yes" and pred != "No":
            #     print(tmp)
            #     print("pred: " + pred + ",id: " + id + ", turn: "+ turn +'\n' ) 
            if "<Answer3>:Yes" in obj["gold out"]:
                if 'Yes' in pred:#pred true, gold true
                    self._detection_tp += 1   
                    self.tmpSet.add((id,turn))                           
                else:
                    self._detection_fn += 1#pred false, gold true
            else:
                if 'Yes' in pred:#pred true, gold false
                    self._detection_fp += 1
                    # print(tmp)
                    # print("pred: " + pred + ",id: " + id + ", turn: "+ turn +'\n' )   
                else:
                    self._detection_tn += 1#pred false, gold false
        except:
            print(tmp)
            print("id: " + id + ", turn: "+ turn +'\n' ) 

    def _compute(self, score_sum):
        if self._detection_tp + self._detection_fp > 0.0:
            score_p = score_sum/(self._detection_tp + self._detection_fp)
        else:
            score_p = 0.0

        if self._detection_tp + self._detection_fn > 0.0:
            score_r = score_sum/(self._detection_tp + self._detection_fn)
        else:
            score_r = 0.0

        if score_p + score_r > 0.0:
            score_f = 2*score_p*score_r/(score_p+score_r)
        else:
            score_f = 0.0

        return (score_p, score_r, score_f)
        

    def scores(self, gold):
        detection_p, detection_r, detection_f = self._compute(self._detection_tp)
              
        scores = {
            'detection': {
                'true positive': self._detection_tp,
                'prec': detection_p,
                'rec': detection_r,
                'f1': detection_f,
                'acc': self._detection_tp/gold
            },
        }

        return scores


def readFile(dirname):
    metric = Metric()
    dir_path = '/Users/jannatarameem/Desktop/Fall23/ChatGPT/output/gpt-4/'+ dirname + '/V2/'#alexaData/'#SGD'#MultiWoz'#alexaData'
    # dir_path = '/Users/jannatarameem/Desktop/Fall23/ChatGPT/output/gpt-4/alexaData'#'/Users/jannatarameem/Desktop/Fall23/ChatGPT/output/gpt-4' 
    23 + 22
    # Iterate directory
    print(dir_path)
    for file_path in os.listdir(dir_path):
        print(file_path)
        # check if current file_path is a file
        # print(file_path)
        if '.json' in os.path.join(dir_path, file_path):
            gold = 0
            pred = 0#
            # add filename to list
            with open(os.path.join(dir_path, file_path), 'r') as f:
                data = json.load(f)
            
            name = file_path.split('.')[0]
            
            print(name)
            # return
            # truth, correct_pred = checkAlexa(data)
            truth, correct_pred = check(data)
            for k, v in data.items():
                for turnID, instance in v.items():
                    # try:
                        metric.update(instance,k, turnID)
                    # except:
                        # print(f'id: {k}, turn: {turnID}')
            
            gold += truth
            pred += correct_pred

    # with open('/Users/jannatarameem/Desktop/Fall23/ChatGPT/GPT_output_dialog003.json', 'r') as f:
    #     data = json.load(f)
    # return data
            print(f'True: {gold}, correct pred: {pred}')
            x = pred/gold
            print(f'acc: {x}')

            scores = metric.scores(gold)

            with open(dir_path+'/scores/scoreV2_'+ name+ '.json', 'w') as out:
                json.dump(scores, out, indent=2)
            
            with open(dir_path+'/scores/tmpSetV2_'+ name+ '.json', 'w') as out:
                json.dump(list(metric.tmpSet), out, indent=2)




dirname = 'SGD'
readFile(dirname)
