import re
import os
import pandas as pd
import numpy as np
app = Flask(__name__)
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'6\xe9\xda\xead\x81\xf7\x8d\xbbH\x87\xe8m\xdd3%'
    MONGODB_SETTINGS = { 'db' : 'Team_Dynamics' }
app.config.from_object(Config)
db = MongoEngine()
db.init_app(app)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")
    def validate_email(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")
class Professional_RegisterForm(FlaskForm):
    name=StringField("Enter Full Name", validators=[DataRequired(),Length(min=2,max=55)])
    contact=StringField("Enter Contact", validators=[DataRequired(),Length(min=10,max=10)])
    office=StringField("Enter Office/Location", validators=[DataRequired(),Length(min=2,max=55)])
    designation=StringField("Enter Designation",validators=[DataRequired(),Length(min=2,max=55)])
    skills=StringField("Enter Skills",validators=[DataRequired(),Length(min=2,max=255)])
    email   = StringField("Enter Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register Now")
    def validate_email(self,email):
        user = Registered_Professionals.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")
    def validate_contact(self,contact):
        user = Registered_Professionals.objects(contact=contact.data).first()
        if user:
            raise ValidationError("Contact is already in use. Pick another one.")   class AdminLoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
class AdminRegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")
    def validate_email(self,email):
        user = Admin.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    password    =   db.StringField( )
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password, password class Admin(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    password    =   db.StringField( )
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password, password) class Registered_Professionals(db.Document):
    empid       =   db.IntField( unique=True )
    name        =   db.StringField( max_length=50 )
    contact     =   db.StringField( max_length=50,unique=True )
    office      =   db.StringField( max_length=50 )
    designation =   db.StringField( max_length =50 )
    skills      =   db.StringField( max_length =255 )
    email       =   db.StringField( max_length=30, unique=True )
def index():
    return render_template("index.html",index=True )
@app.route('/login', methods =['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"Employee {user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True ) @app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    if session.get('a_username'):
        return redirect(url_for('index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        user = Admin.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"Manager {user.first_name}, you are successfully logged in!", "success")
            session['a_user_id'] = user.user_id
            session['a_username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("adminlogin.html", title="Manager Login", form=form, adminlogin=True ) @app.route("/logout")
def logout():
        session['a_user_id']=False
        session.pop('a_username',None)
        session['user_id']=False
        session.pop('username',None)
        return redirect(url_for('index')) @app.route('/register', methods =['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        first_name  = form.first_name.data
        last_name   = form.last_name.data
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered in Employee class!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Employee Register", form=form, register=True) @app.route('/register_as_professional', methods =['GET', 'POST'])
def register_as_professional():
    form = Professional_RegisterForm()
    if form.validate_on_submit():
        empid       =  Registered_Professionals.objects.count()
        empid      +=  1
        name        =  form.name.data
        contact     =  form.contact.data
        office      =  form.office.data
        designation =  form.designation.data
        skills      =  form.skills.data
        email       =  form.email.data

        user = Registered_Professionals(empid=empid, name=name, contact=contact,office=office,designation=designation,skills=skills,email=email)
        user.save()
        flash("You are successfully registered as an Professional!","success")
        return redirect(url_for('index'))
    return render_template("register_as_professional.html", title="Register Professional", form=form, register_as_professional=True) @app.route('/project_allocation', methods =['GET', 'POST'])
def project_allocation():
    return  render_template('project_allocation.html',project_allocation=True) @app.route('/adminregister', methods =['GET', 'POST'])
def adminregister():
    if session.get('a_username'):
        return redirect(url_for('index'))
    form = AdminRegisterForm()
    if form.validate_on_submit():
        user_id     = Admin.objects.count()
        user_id     += 1
        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data
        user = Admin(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered in Manager class!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Manager Register", form=form)@app.route('/your_url',methods=['GET','POST'])
        d1=[]

        df=pd.DataFrame(d1)
        df_empid=df['empid']
        df_name=df['name']
        df_contact=df['contact']
        df_office=df['office']
        df_designation=df['designation']
        df_skills=df['skills']
        df_emails=df['email']
        userin_organization_name=request.form['organization_name']
        userin_phone=request.form['phone1']
        userin_email=request.form['email']
        userin_skill=request.form['requirements']
        userin_location=request.form['location']
        userin_number_of_employees=request.form['number_of_employees']
        project_info(userin_organization_name, userin_phone, userin_email, userin_skill, userin_location, userin_number_of_employees)
        l1=[]
        i=0
        userin_skilllist=userin_skill.split(',')
        for empid,skill,location in zip(df_empid,df_skills,df_office):
            empid=int(empid)
            skill_list=skill.split(',')
            ratio_skill=check_ratio(userin_skilllist,skill_list)
            ratio_location=SequenceMatcher(lambda x: x == " ",userin_location.upper(),location.upper()).ratio()
            if ratio_skill>0.65 and ratio_location>0.85:
                i+=1
                l1.append({"S.No":i,
                           "EMP ID": df_empid[empid-1] ,
                           "Name": df_name[empid-1],
                           "Contact": df_contact[empid-1],
                           "Location": df_office[empid-1],
                           "Designation": df_designation[empid-1] ,
                           "Skill" : df_skills[empid-1],
                           "Emails" : df_emails[empid-1]})
        if len(l1)<int(userin_number_of_employees):
            flash('Sorry for not meeting up your demands','danger')
        return render_template('selected.html',employee_data=l1,selected=True,project_info_for_store=userin_organization_name+'_'+userin_phone+'_'+userin_location)
    else:
        return redirect(url_for('project_allocation'))
def check_ratio(userin_skilllist,skill_list):
    i=0
    for userin_skill in userin_skilllist:
        userin_skill=re.sub(r'([++])+',"PP",userin_skill)
        userin_skill=re.sub(r'(\W)+',"",userin_skill)
        for skill in skill_list:
            skill=re.sub(r'([++])+',"PP",skill)
            skill=re.sub(r'(\W)+',"",skill)
            ration=SequenceMatcher(lambda x: x == " ",userin_skill.upper(),skill.upper()).ratio()
            if ration>0.6:
                i+=1
    percent=(i)/(len(userin_skilllist))
    return percent
def project_info(userin_organization_name, userin_phone, userin_email, userin_skill, userin_location, userin_number_of_employees):
    project_data=[]
    if os.path.exists('Projects\\Project_Info.json'):
        with open ('Projects\\Project_Info.json','r') as file:
            project_data=json.load(file)
            project_data.append({'Organization Name':userin_organization_name
            ,'Contact':userin_phone,'Email':userin_email
            ,'Skills Required':userin_skill,
            'Location':userin_location,
            'Number Required':userin_number_of_employees})
        with open ('Projects\\Project_Info.json','w') as file:
            json.dump(project_data,file)
    else :
        with open ('Projects\\Project_Info.json','w') as file:
            project_data.append({'Organization Name':userin_organization_name
            ,'Contact':userin_phone,'Email':userin_email
            ,'Skills Required':userin_skill,
            'Location':userin_location,
            'Number Required':userin_number_of_employees})
            json.dump(project_data,file) @app.route('/allocated',methods=['GET','POST'])
def allocated():
    if request.method == 'POST':
        files_list=os.listdir('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Employee_Allocated')
        file_name=request.form['project_info_for_store'].upper()+'.json'
        selected_list=request.form.getlist('selected_list')
        selected_list_converted=[]
        for emp in selected_list:
            emp=eval(emp)
            return redirect(url_for('index'))
        else:
            with open ('Employee_Allocated\\'+file_name,'w') as file:
                json.dump(selected_list_converted,file)
                flash('Give us a chance to serve gain your request is submitted. We will reach you out soon.',"success")
                return redirect(url_for('index'))
    return render_template('allocated.html', enrollment=True)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import PyPDF2
import pickle
@app.route('/cv_selection',methods=['GET','POST'])
def cv_selection():
        files_list=os.listdir('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Resumes')
        return render_template('cv_selection.html',files_list=files_list,cv_selection=True) @app.route('/cv_selection_evaluate',methods=['GET','POST'])
def cv_selection_evaluate():
    a=''
    resume_name=request.form['resume_name']
    if os.path.exists('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Resumes\\'+resume_name):
        with open('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Resumes\\'+resume_name,'rb') as file:
            line=file.readlines()
            pdfReader = PyPDF2.PdfFileReader(file)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                a+=pageObj.extractText()
            preprocess_text=preprocess(str(a))
            preprocess_text=[preprocess_text]
            vectorizer_model = pickle.load(open('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Machine Learning Models\\vectorizer', 'rb'))
            text_matrix=vectorizer_model.transform(preprocess_text)
            resume_selection_model=pickle.load(open('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Machine Learning Models\\resume_selection', 'rb'))
            predict_resume=resume_selection_model.predict(text_matrix)
            resume_name=resume_name.replace('.pdf','')
            resume_name=resume_name.split('_')
    else:
        flash('File Does not Exist','danger')
        return redirect(url_for('index'))
    return render_template('cv_selection_evaluate.html',resume_name=resume_name,predict_resume=predict_resume)
def preprocess(text):
    stop_words=stopwords.words('english')
    stop_words.extend(['from','subject','use','email','com','name','/' , '\\' ,'\r','/r','|','(',')',',','.'])
    result = []
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2 and token not in stop_words:
            result.append(token)
    return ' '.join(result)
UPLOAD_FOLDER_RESUMES = 'C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Resumes'
ALLOWED_EXTENSIONS = {'txt', 'pdf','docx'}
app.config['UPLOAD_FOLDER_RESUMES'] = UPLOAD_FOLDER_RESUMES @app.route('/job_application',methods=['GET','POST'])
def job_application():
    return render_template('job_application.html',job_application=True)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS @app.route('/job_application_submit',methods=['GET','POST'])
def job_application_submit():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file Part',"danger")
            return redirect(url_for('job_application'))
        if 'name' not in request.form:
            flash('Name field empty',"danger")
            return redirect(url_for('job_application'))
        if 'phone1' not in request.form:
            flash('Contact Number not entered',"danger")
            return redirect(url_for('job_application'))
        if 'email' not in request.form:
            flash('Email not entered',"danger")
            return redirect(url_for('job_application'))
        username=request.form['name']
        phone1=request.form['phone1']
        email=request.form['email']
        resume_file_name=username+"_"+phone1+"_"+email
        file=request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('job_application'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename=filename.split('.')
            file.save(os.path.join(app.config['UPLOAD_FOLDER_RESUMES'], resume_file_name+'.'+filename[1]))
    return render_template('submit.html',data={'name':username,'phone':phone1,'email':email,'filename':filename}) @app.route('/project_undertakings',methods=['GET','POST'])
def project_undertakings():
    project_list=[]
    if session.get('a_username') or session.get('username'):
        if os.path.exists('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Projects\\Project_Info.json'):
            with open ('Projects\\Project_Info.json','r') as file:
                project_list=json.load(file)
    return render_template('project_undertakings.html',project_undertakings=True,project_list=project_list) @app.route('/employee_project_details',methods=['GET','POST'])
def employee_project_details():
    project_list=[]
    if session.get('a_username'):
        if os.path.exists('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Employee_Allocated'):
            files_list=os.listdir('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Employee_Allocated')
            for file in files_list:
                file=file.replace('.json','')
                file=file.split('_')
                project_list.append(file)
        else:
            flash("No data available","danger")
            return redirect(url_for('index'))
    return render_template('employee_project_details.html',employee_project_details=True,project_list=project_list) @app.route('/display_employees',methods=['GET','POST'])
def display_employees():
    diplay_employee_list=[]
    if session.get('a_username'):
        if os.path.exists('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Employee_Allocated'):
            file=request.form['file_name']
            file=request.form.getlist('file_name[]')
            with open('C:\\Users\\Manish\\Desktop\\MANISH\\PROJECT\\Resource_Management\\Employee_Allocated\\IBM_8360-539-166_PUNE.json','r') as f:
                display_employee_list=json.load(f)
        else:
            flash("No data available","danger")
            return redirect(url_for('index'))
    return render_template('display_employees.html',display_employee_list=display_employee_list)
