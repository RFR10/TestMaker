import json
from create import TESTS
import random

def create_random_test(age_range, profession):
    db_test = TESTS.query.filter_by(age_range=age_range, profession=profession).first()
    test_data = {
        'questions': json.loads(db_test.questions),
        'answers': json.loads(db_test.answers),
        'keys': json.loads(db_test.keys),
        'questions_types': json.loads(db_test.questions_types)
    }
    if not db_test.selects_options:
        test_data['selects_options'] = False
    else:
        test_data['selects_options'] = json.loads(db_test.selects_options)
    random_keys = random.sample(test_data['keys'], 10)
    print(random_keys)
    random_test = {
        'questions': dict((k, test_data['questions'][str(k)]) for k in random_keys if str(k) in test_data['questions']),
        'answers': dict((k, test_data['answers'][str(k)]) for k in random_keys if str(k) in test_data['answers']),
        'keys': random_keys,
        'questions_types': dict((k, test_data['questions_types'][str(k)]) for k in random_keys if str(k) in test_data['questions_types']),
    }

    if not test_data['selects_options']:
        random_test['selects_options'] = None
    else:
        random_test['selects_options'] = dict((k, test_data['selects_options'][str(k)]) for k in random_keys if str(k) in test_data['selects_options'])
    if random_test['selects_options'] == {}:
        random_test['selects_options'] = None


    test_cont = ''
    for key in random_keys:
        question = random_test['questions'][key]
        answer = random_test['answers'][key]
        type = random_test['questions_types'][key]
        if type == 'SELECT':
            select_options = random_test['selects_options'][key]
        if type == 'SELECT':
            con = f'{question} {select_options} \n'
        else:
            con = f'{question}\n'
            test_cont += con
        with open('test_cont.txt', 'w') as f:
            f.write(test_cont)
            f.close()

    random_test['test_cont'] = test_cont

    return random_test


print('test_cont: ', create_random_test('9-10', 'math')['test_cont'].split('\n'))