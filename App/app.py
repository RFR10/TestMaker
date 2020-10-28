from flask import *
from flask_restful import Api, Resource
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import datetime
from fpdf import FPDF 

app = Flask(__name__)
app.secret_key = 'codejamsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=60)

API = Api(app)
db = SQLAlchemy(app)

accountsys_responses = {
    'SIGNUP': {
        'OK': {'WORK': 'SIGNUP'},
        'USERNAME_TAKEN': {'ERR': 'USERNAME_TAKEN'}
    },
    'LOGIN': {
        'OK': {'WORK': 'LOGIN'},
        'WRONG_PASSWORD': {'ERR': 'WRONG_PASSWORD'},
        'ACCOUNT_DONT_EXIST': {'ERR': 'ACCOUNT_DONT_EXIST'}
    }
}

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class user_history(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    USERID = db.Column(db.Integer)
    USERPASS = db.Column(db.String(100))
    TEST_NAME = db.Column(db.String(20))
    TEST_KEYS = db.Column(db.String(1000))
    TEST_QUESTIONS = db.Column(db.String(1000))
    TEST_ANSWERS = db.Column(db.String(1000))
    TEST_SELECTS_OPTIONS = db.Column(db.String(1000))
    TEST_QUESTIONS_TYPES = db.Column(db.String(1000))
    TEST_CONT = db.Column(db.String(1000))
    TEST_MAKEDATE = db.Column(db.DateTime)

    def __init__(self, USERID, USERPASS, TEST_NAME, TEST_KEYS, TEST_QUESTIONS, TEST_ANSWERS, TEST_SELECTS_OPTIONS, TEST_QUESTIONS_TYPES, TEST_CONT, TEST_MAKEDATE):
        self.USERID = USERID
        self.USERPASS = USERPASS
        self.TEST_NAME = TEST_NAME
        self.TEST_KEYS = TEST_KEYS
        self.TEST_QUESTIONS = TEST_QUESTIONS
        self.TEST_ANSWERS = TEST_ANSWERS
        self.TEST_SELECTS_OPTIONS = TEST_SELECTS_OPTIONS
        self.TEST_QUESTIONS_TYPES = TEST_QUESTIONS_TYPES
        self.TEST_CONT = TEST_CONT
        self.TEST_MAKEDATE = TEST_MAKEDATE

# db.create_all()
# quit()
# test = TESTS(1,'test','tf')
# db.session.add(test)
# db.session.commit()
# quit()

# db.create_all()
# temp.query.filter_by()

class AccountSys(Resource):
    def post(self, username, password):
        found_user = users.query.filter_by(username=username).first()
        if found_user:
            return {
                'ERR': 'USERNAME_TAKEN'
            }
        if not found_user:
            user = users(username, password)
            db.session.add(user)
            db.session.commit()
            return {
                'WORK': 'SIGNUP'
            }
    def get(self, username, password):
        found_user = users.query.filter_by(username=username).first()
        if found_user:
            if found_user.password == password:
                return {
                    'WORK': 'LOGIN'
                }
            else:
                return {
                    'ERR': 'WRONG_PASSWORD'
                }
        if not found_user:
                    return {
                        'ERR': 'ACCOUNT_DONT_EXIST'
                    }

class CreateTestSys(Resource):
    def post(self, test_name):
        return {'create': test_name}

API.add_resource(AccountSys, '/API/accountsys/<string:username>/<string:password>')
API.add_resource(CreateTestSys, '/API/createtest/<string:test_name>')

ACCOUNT_API_URL = 'http://127.0.0.1:5000/API/accountsys/{username}/{password}'
CREATETEST_API_URL = 'http://127.0.0.1:5000/API/createtest/{test_name}'

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/about')
def About():
    return redirect('https://github.com/RFR10/TestMaker/blob/master/README.md')


@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == '' and password == '':
            flash('You dont enter username and password.', 'info')
            return render_template("signup.html")
        if username == '':
            flash('You dont enter username.', 'info')
            return render_template("signup.html")
        if password == '':
            flash('You dont enter password.', 'info')
            return render_template("signup.html")

        print('username: ', username, ' password: ', password)
        req = requests.get(ACCOUNT_API_URL.format(username=username, password=password))
        print(req.json())
        
        if req.json() == accountsys_responses['LOGIN']['OK']:
            userid = users.query.filter_by(username=username).first()._id
            userpass = users.query.filter_by(username=username).first().password
            session['USER_ID'] = int(userid)
            session['USER_PASSWORD'] = userpass
            print('_id: ', users.query.filter_by(username=username).first()._id)
            return redirect(url_for('Dashboard'))
        elif req.json() == accountsys_responses['LOGIN']['WRONG_PASSWORD']:
            flash('Wrong password, try again.', 'info')
        elif req.json() == accountsys_responses['LOGIN']['ACCOUNT_DONT_EXIST']:
            flash('Account dont exist, check if again or click on Sign Up', 'info')

        print('log in req: ', req.json())
        return render_template("login.html")
    else:
	    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']


        if username == '' and password == '':
            flash('You dont enter username and password.', 'info')
            return render_template("signup.html")
        if username == '':
            flash('You dont enter username.', 'info')
            return render_template("signup.html")
        if password == '':
            flash('You dont enter password.', 'info')
            return render_template("signup.html")

        print('username: ', username, ' password: ', password)
        req = requests.post(ACCOUNT_API_URL.format(username=username, password=password))
        if req.json() == accountsys_responses['SIGNUP']['OK']:
            userid = users.query.filter_by(username=username).first()._id
            userpass = users.query.filter_by(username=username).first().password
            session['USER_ID'] = int(userid)
            session['USER_PASSWORD'] = userpass
            print('_id: ', users.query.filter_by(username=username).first()._id)
            return redirect(url_for('Dashboard'))
        elif req.json() == accountsys_responses['SIGNUP']['USERNAME_TAKEN']:
            flash('Username already taken, please enter diffrent username', 'info')
        print('sign up req: ', req.json())

        return render_template("signup.html")
    else:
	    return render_template("signup.html")

@app.route('/logout')
def Logout():
    session.pop('USER_ID', None)
    return redirect(url_for('Home'))

@app.route('/dashboard')
def Dashboard():
    try:
        session['USER_ID']
    except:
        return redirect(url_for('Home'))
    have_tests = user_history.query.filter_by(USERID=session['USER_ID'], USERPASS=session['USER_PASSWORD']).all()
    if not have_tests:
        have_tests = False
        tests = False
    else: 
        have_tests = True
        tests = user_history.query.filter_by(USERID=session['USER_ID'], USERPASS=session['USER_PASSWORD']).all()
    return render_template('dashboard.html', have_tests=have_tests, tests=tests)

@app.route('/create-test', methods=['GET', 'POST'])
def CreateTest():
    try:
        session['USER_ID']
    except:
        return redirect(url_for('Home'))
    if request.method == 'POST':
        session['USER_TEST'] = {}
        session['USER_TEST']['USER_ID'] = session['USER_ID']
        session['USER_TEST']['USER_PASSWORD'] = session['USER_PASSWORD']
        test_name = request.form['test_name']
        name_exist = user_history.query.filter_by(USERID=session['USER_ID'], USERPASS=session['USER_PASSWORD'], TEST_NAME=test_name).first()
        if name_exist:
            flash('You already created a test with this name, try another one')
            return render_template('create-test.html')
        session['USER_TEST']['TEST_NAME'] = test_name
        # req = requests.post(CREATETEST_API_URL.format(test_name=test_name))
        return redirect(url_for('TestQuiz'))
    else:
        return render_template('create-test.html')

@app.route('/test-quiz', methods=['GET', 'POST'])
def TestQuiz():
    from create_random_test import create_random_test
    try:
        session['USER_TEST']
    except:
        return redirect(url_for('Home'))
    if request.method == 'POST':
        age_range = request.form['age-range']
        profession = request.form['profession']
        user_rtest = create_random_test(age_range, profession)
        user_test_h = user_history(int(session['USER_TEST']['USER_ID']), session['USER_TEST']['USER_PASSWORD'], session['USER_TEST']['TEST_NAME'], json.dumps(user_rtest['keys']), json.dumps(user_rtest['questions']), json.dumps(user_rtest['answers']), json.dumps(user_rtest['selects_options']), json.dumps(user_rtest['questions_types']), user_rtest['test_cont'], datetime.datetime.today())
        db.session.add(user_test_h)
        db.session.commit()
        return redirect(url_for('Dashboard'))
    else:
        return render_template('test_quiz.html')

@app.route('/select-test/<uid>/<upass>/<tname>/<aurl>')        
def select_test(uid, upass, tname, aurl):
    test = user_history.query.filter_by(USERID=session['USER_ID'], USERPASS=session['USER_PASSWORD'], TEST_NAME=tname).first()
    session['USER_CURRENT_TEST'] = {
        'USERID': test.USERID,
        'USERPASS': test.USERPASS,
        'TEST_NAME': test.TEST_NAME,
        'TEST_KEYS': json.loads(test.TEST_KEYS),
        'TEST_QUESTIONS': json.loads(test.TEST_QUESTIONS),
        'TEST_ANSWERS': json.loads(test.TEST_ANSWERS),
        'TEST_SELECTS_OPTIONS': json.loads(test.TEST_SELECTS_OPTIONS),
        'TEST_QUESTIONS_TYPES': json.loads(test.TEST_QUESTIONS_TYPES),
        'TEST_CONT': test.TEST_CONT
    }
    return redirect('/'+aurl)

@app.route('/view-test')
def ViewTest():
    try:
        session['USER_CURRENT_TEST']
    except:
        return redirect(url_for('Home'))

    print(session['USER_CURRENT_TEST']['TEST_CONT'].split('\n'))
    user_test_cont = session['USER_CURRENT_TEST']['TEST_CONT'].split('\n')
    return render_template('view-test.html', test_cont=user_test_cont)

@app.route('/export/basic', methods=['GET', 'POST'])
def ExportBasic():
    try:
        session['USER_CURRENT_TEST']
    except:
        return redirect(url_for('Home'))

    if request.method == 'POST':
        EXPORT_PATH = request.form['export_path']
        try:
            with open(EXPORT_PATH, 'w') as f:
                f.write(session['USER_CURRENT_TEST']['TEST_CONT'])
                f.close()
            flash('write succsesfuly')
            return redirect(url_for('Dashboard'))
        except:
            flash('Wrong path try again.')
            return redirect(url_for('ExportBasic'))
    else:
        return render_template('export-test.html')

@app.route('/export/pdf', methods=['GET', 'POST'])
def ExportPdf():
    try:
        session['USER_CURRENT_TEST']
    except:
        return redirect(url_for('Home'))

    if request.method == 'POST':
        EXPORT_PATH = request.form['export_path']
        try:
            pdf = FPDF() 
            pdf.add_page() 
            pdf.set_font("Arial", size = 25) 
            pdf.cell(200, 10, txt =session['USER_CURRENT_TEST']['TEST_NAME'], ln = 1, align = 'C') 
            pdf.set_font("Arial", size = 15) 

            for letter in range(len(session['USER_CURRENT_TEST']['TEST_CONT'][:-1].split('\n'))): 
                type = session['USER_CURRENT_TEST']['TEST_QUESTIONS_TYPES'][str(session['USER_CURRENT_TEST']['TEST_KEYS'][letter])] 
                if type == 'SELECT':
                    letter = session['USER_CURRENT_TEST']['TEST_CONT'].split('\n')[letter]
                    pdf.cell(200, 20, txt = letter, ln = 1, align = 'L') 
                else:
                    letter = session['USER_CURRENT_TEST']['TEST_CONT'].split('\n')[letter]
                    pdf.cell(200, 10, txt = letter, ln = 1, align = 'L') 
            pdf.output(EXPORT_PATH)
            flash('write succsesfuly')
            return redirect(url_for('Dashboard'))
        except Exception as err:
            flash(f'Wrong path try again, ERR: {err}')
            return redirect(url_for('ExportBasic'))
    else:
        return render_template('export-test.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)