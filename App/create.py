from app import db
import json
import sys
import os

class TESTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_range = db.Column(db.String(10), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    questions = db.Column(db.String(1000), nullable=False)
    keys = db.Column(db.String(1000), nullable=False)
    selects_options = db.Column(db.String(1000), nullable=True)
    answers = db.Column(db.String(1000), nullable=False)
    questions_types = db.Column(db.String(1000), nullable=False)

    def __init__(self, age_range, profession, keys, questions, answers, questions_types, selects_options):
        self.age_range = age_range
        self.profession = profession
        self.keys = keys
        self.questions = questions
        self.answers = answers
        self.questions_types = questions_types
        self.selects_options = selects_options

db.create_all()
# LANGTH OF ARR IN THE PATHS ARR NEED TO BE THE LENGTH OF THE PARAMETERS


paths = [['9-10', 'math'], ['4-6', 'math']]

output = {}

def getkeysList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key)

    return list 

def create_json_file(questions, answer, questions_types, selects_options):
    print('selects_options: ', selects_options)
    keys = []
    dic = {
        'questions': {},
        'keys': [],
        'answers': {},
        'questions_types': {},
        'selects_options': {
            'have': False,
        }
    }

    selects_keys = []

    for question in range(len(questions)):
        dic['questions'][question] = questions[question]
        dic['keys'].append(question)

    for answer in range(len(questions)):
        dic['answers'][answer] = answers[answer]
        
    for type in range(len(questions)):
        dic['questions_types'][type] = questions_types[type]
        if questions_types[type] == 'SELECT':
            selects_keys.append(str(type))

    if not selects_options:
        dic['selects_options'] = False
    else:
        for select_options in range(len(selects_options)):
            selects_options[selects_keys[int(select_options)]] = selects_options.pop(str(select_options))
        dic['selects_options'] = selects_options

    

    return dic  


for path in paths:
    with open(f'{path[0]}/{path[1]}/data.json', 'r') as f:
        data = json.loads(f.read())
    questions = data['questions']
    answers = data['answers']
    questions_types = data['TYPE']
    try:
        selects_options = data['selects_options']
    except:
        selects_options = False
    json_dic = create_json_file(questions, answers, questions_types, selects_options)
    if path[0] in getkeysList(json_dic):
        output[path[0]][path[1]] = json_dic
    else:
        output[path[0]] = {}
        output[path[0]][path[1]] = json_dic


with open('output_data.json', 'w') as f:
    f.write(json.dumps(output))
    f.close()

for para in output:
    for spara in output[para]:
        current_dict = output[para][spara]
        questions = json.dumps(current_dict['questions'])
        answers = json.dumps(current_dict['answers'])
        questions_types = json.dumps(current_dict['questions_types'])
        keys = json.dumps(current_dict['keys'])
        if not current_dict['selects_options']:
            selects_options = None
        else:
            selects_options = json.dumps(current_dict['selects_options'])
        dtest = TESTS(para, spara, keys, questions, answers, questions_types, selects_options)
        db.session.add(dtest)
        db.session.commit()
