from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import exc
import math
import sqlite3
import sympy as smp
from sympy import *
import time
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Inventorydata(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Class = db.Column(db.String(2),nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Inventorydata('{self.ID}', '{self.Name}', '{self.Quantity}', '{self.Cost}')"


class Homepagedata(db.Model):
    ID= db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100),nullable=False)   
    Email = db.Column(db.String(100),nullable=False)
    Subject = db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f"Homepagedata('{self.Name}','{self.Email}', '{self.Subject}')"


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class Vendor(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Vendor = db.Column(db.String(100), nullable=False)
    NumberSpecified = db.Column(db.Integer, nullable=False)
    NumberReceived = db.Column(db.Float, nullable=False)
    AcceptedLot = db.Column(db.Integer, nullable=False)
    UnderDeviation = db.Column(db.Integer, nullable=False)
    Inspected = db.Column(db.Integer, nullable=False)
    Rejected = db.Column(db.Integer, nullable=False)
    LineProblem = db.Column(db.Integer, nullable=False)
    CustomerLineProblem = db.Column(db.Integer, nullable=False)
    WarrantyProblem = db.Column(db.Integer, nullable=False)
    Response = db.Column(db.Integer, nullable=False)
    DeliveryDateSpecified = db.Column(db.String(10), nullable=False)
    Deliveredon = db.Column(db.String(10), nullable=False)
    PremiumFreight = db.Column(db.Integer, nullable=False)
    Courtesy = db.Column(db.Integer, nullable=False)
    Responsiveness = db.Column(db.Integer, nullable=False)
    QualityRating = db.Column(db.Integer)
    DeliveryRating = db.Column(db.Integer)
    ServiceRating = db.Column(db.Integer)
    OverallRating = db.Column(db.Integer)
    PartNumber = db.Column(db.String,nullable=False)


    def __repr__(self):
        return f"Inventorydata('{self.Vendor}', '{self.QualityRating}', '{self.DeliveryRating }', '{self.OverallRating}')"



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class inventorypage(FlaskForm):
     Name = StringField('Part Number', validators=[DataRequired()])
     Class = StringField('Class',validators=[DataRequired()])
     Quantity = IntegerField("Quantity", validators=[DataRequired()])
     Cost = DecimalField("Cost",validators=[DataRequired()])
     Submit = SubmitField('Add')

class demandpage(FlaskForm):
     Class = StringField('Class of Inventory', validators=[DataRequired()])
     Demand = DecimalField("Demand Rate", validators=[DataRequired()])
     SetCost = DecimalField("Setup Cost",validators=[DataRequired()])
     HoldCost = DecimalField("Holding Cost",validators=[DataRequired()])
     Submit = SubmitField("Calculate")

class datainvf(FlaskForm):
    ID = StringField('Part Number')
    Class=StringField('Class')
    B1=SubmitField("Get Record")
    B2=SubmitField("Update Record")

class demandpage1(FlaskForm):
    Class = StringField('Class of Inventory', validators=[DataRequired()])
    Demand = DecimalField("Average Demand", validators=[DataRequired()])
    Lead =   IntegerField("Lead Time", validators=[DataRequired()])
    Stock =  DecimalField("Safety Stock", validators=[DataRequired()])
    Submit=  SubmitField("Calculate")

class updatepage(FlaskForm):
    Class = StringField('Class',validators=[DataRequired()])
    Quantity = IntegerField("Quantity", validators=[DataRequired()])
    Cost = DecimalField("Cost",validators=[DataRequired()])
    Submit = SubmitField('Add')

class variabledemand(FlaskForm):
    SetCost = DecimalField('Set-up Cost', validators=[DataRequired()])
    HoldingCost = DecimalField('Holding Cost', validators=[DataRequired()])
    a = DecimalField('Value of Parameter a', validators=[DataRequired()])
    b = DecimalField('Value of Parameter b', validators=[DataRequired()])
    c = DecimalField('Value of Parameter c', validators=[DataRequired()])
    Submit = SubmitField('Evaluate for the case')

class staticcase(FlaskForm):
    alpha = DecimalField('Alpha', validators=[DataRequired()])
    Submit = SubmitField('Calculate')

class expcase(FlaskForm):
    alpha = DecimalField('Alpha', validators=[DataRequired()])
    lambd = DecimalField('Value of Lambda', validators=[DataRequired()])
    Submit = SubmitField('Calculate')

class vendor(FlaskForm):
    vendor = StringField('Vendor Name',validators=[DataRequired()])
    partnum = StringField("Part Number", validators=[DataRequired()])
    numspecified = IntegerField("Number Specified at Order", validators=[DataRequired()])
    numreceived= IntegerField("Number Received at order", validators=[DataRequired()])
    acceptedlot = IntegerField("Accepted Lot", validators=[DataRequired()])
    underdeviation = IntegerField("Under Deviation Lot", validators=[DataRequired()])
    inspected = IntegerField("Inspected lot", validators=[DataRequired()])
    rejected= IntegerField("Rejected Lot", validators=[DataRequired()])
    lineprob = IntegerField("Line Problem", validators=[DataRequired()])
    customerlineprob = IntegerField("Customer Line Problem", validators=[DataRequired()])
    warrantyprob = IntegerField("Warranty Problem", validators=[DataRequired()])
    response = IntegerField("Respose", validators=[DataRequired()])
    ddspecified= StringField('Delivery Date Specified',validators=[DataRequired()])    
    deliveredon = StringField('Delivery On',validators=[DataRequired()])  
    Freight = IntegerField("Premium Freight Charges", validators=[DataRequired()])
    courtesy = IntegerField("Courtesy", validators=[DataRequired()])
    responsiveness = IntegerField("Responsiveness", validators=[DataRequired()])
    Submit = SubmitField('Submit')


@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    if request.method=="POST":
        Name = request.form['name']
        Email = request.form['email']
        Subject = request.form['subject']
        query = Homepagedata(Name=Name, Email=Email, Subject=Subject)
        try:
            db.session.add(query)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Error", 'danger')
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/inventory", methods=['GET','POST'])
def inventory():
    form = inventorypage()
    if current_user.is_authenticated:
        if request.method=='POST':
            if form.validate_on_submit():
                Name = form.Name.data
                Class = form.Class.data
                Quantity = form.Quantity.data
                Cost = form.Cost.data
                inventory = Inventorydata(Name=form.Name.data, Quantity=form.Quantity.data, Cost = form.Cost.data, Class=form.Class.data)
                try:
                    db.session.add(inventory)
                    db.session.commit()
                    flash('Your Record has been added','success')
                except:
                     db.session.rollback()
                     flash('Error in Connection','danger')
            else:
                flash('Please check the entered information', 'danger')
    else:
        form1 = RegistrationForm()
        flash('Unauthorized access', 'danger')
        return render_template('register.html',form=form1)


    return render_template('inventory.html',form = form)
        

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/changepassword", methods=['GET',"POST"])
def changepassword():
    form = changepasswordform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        record = User.query.filter_by(username=current_user.username).first()
        record.password=hashed_password
        db.session.commit()
        flash("Password Changed", 'success')
        return redirect(url_for('account'))
    return render_template("changepass.html", form = form)


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    if request.form.get('pwd',None) == 'Change Password': 
        return redirect(url_for('changepassword'))
    return render_template('account.html', title='Account')


@app.route("/BOM")
def BOM():
    return render_template('BOM.html')
@app.route("/Report")
def report():
    return render_template('50113a02-9ea4-11eb-8b25-0cc47a792c0a_id_50113a02-9ea4-11eb-8b25-0cc47a792c0a.html')


@app.route("/Demand",methods=['GET','POST'])
def demand():
    if current_user.is_authenticated:
        if request.method=='POST':
            model=request.form['model']
            if model=='EOQ':
                return redirect(url_for("DemandEoq"))
            if model=='Fixed Order Quantity':
                return redirect(url_for("DemandFoq"))
    else:
        form1 = RegistrationForm()
        flash('Unauthorized access', 'danger')
        return render_template('register.html',form=form1)


    return render_template('Demand.html')

@app.route("/DemandEoq",methods = ['GET','POST'])
def DemandEoq():
    form = demandpage()
    if request.method=="POST":
        Class = form.Class.data
        Demand= form.Demand.data
        SetCost=form.SetCost.data
        HoldCost=form.HoldCost.data
        lot = math.sqrt((2*SetCost*Demand)/HoldCost)
        return render_template('DemandEoq.html',form=form,lot = lot)
    return render_template('DemandEoq.html', form=form)

@app.route("/DemandFoq",methods = ['GET','POST'])
def DemandFoq():
    form = demandpage1()
    if request.method=="POST":
        Class = form.Class.data
        Demand= form.Demand.data
        Lead=form.Lead.data
        Stock=form.Stock.data
        avg = Demand*Lead
        lot = avg + Stock
        return render_template('DemandFoq.html',form=form,lot = lot)
    return render_template('DemandFoq.html', form=form)

@app.route("/Database",methods = ['GET','POST'])
def datainv():
    form=datainvf()
    rows=[]
    if request.method=='POST':
        Part = form.ID.data
        Class = form.Class.data
        if Part=="":
            try:
                rows=Inventorydata.query.filter_by(Class=Class).all()
            except:
                flash("Connection Error",'danger')
        else:
            if request.form.get('Upd',None) == 'Update':
                flash("Update the details", 'danger')
                return redirect(url_for('updateform', part = Part))
            if request.form.get('Del',None) == 'Delete':
                Inventorydata.query.filter_by(Name = Part).delete()
                db.session.commit()
                flash(f'Record Deleted', 'danger')
            else:
                rows = Inventorydata.query.filter_by(Name=Part).all()
        if not rows:
            flash("NO RECORD FOUND",'danger')
    return render_template("view.html",form=form,rows = rows)

@app.route("/updateform/<part>", methods = ['GET','POST'])
def updateform(part):
    form = updatepage()
    if request.method=='POST':
        Class_form = form.Class.data
        Quantity_form = form.Quantity.data
        Cost_form = form.Cost.data
        try:
            record = Inventorydata.query.filter_by(Name=part).first()
            record.Class = Class_form
            record.Quantity=Quantity_form
            record.Cost = Cost_form
            db.session.commit()
            flash(f"Updated {part} Sucessfully",'success')
            return redirect(url_for("datainv"))
        except:
            db.session.rollback()
            flash("Failed to update", 'Danger')
    return render_template("update.html", form = form)

@app.route("/variabledeamand", methods = ['GET','POST'])
def stocastic():
    form=variabledemand()
    if current_user.is_authenticated:
        if request.method=='POST':
            demandtype=request.form['demandtype']
            setcost = form.SetCost.data
            holdcost = form.HoldingCost.data
            a = form.a.data
            b = form.b.data
            c = form.c.data
            if demandtype=='Static':
                return redirect(url_for("staticd", setcost = setcost, holdcost = holdcost, A=a, B=b, C=c))
            if demandtype=='Linear':
                return redirect(url_for("lineard", setcost = setcost, holdcost = holdcost, A=a, B=b, C=c))
            if demandtype=='Exp':
                return redirect(url_for("expd", setcost = setcost, holdcost = holdcost, A=a, B=b, C=c))

    else:
        form1 = RegistrationForm()
        flash('Unauthorized access', 'danger')
        return render_template('register.html',form=form1)
    return render_template('variabledemand.html', form = form)


def raphson(fnx,l):
    t1 = smp.symbols('t1')
    h = smp.diff(fnx,t1)
    l.append(1)
    l.append(1-fnx.subs(t1,1)/h.subs(t1,1))
    start = time.time()
    while(1):
        n = len(l)
        if round(l[n-1],4) == round(l[n-2], 4):
            break 
        l.append(l[n-1]-fnx.subs(t1,l[n-1])/h.subs(t1,l[n-1]))
        end = time.time()
        if end-start>5:
            print(end-start)
            break  

@app.route("/staticdemandcase/<setcost>/<holdcost>/<A>/<B>/<C>", methods=['GET', 'POST'])
def staticd(setcost, holdcost, A, B, C):
    form = staticcase()
    A = float(A)
    B = float(B)
    C = float(C)
    setcost = float(setcost)
    holdcost = float(holdcost)
    if request.method=='POST':
        Alpha = form.alpha.data
        Alpha = float(Alpha)
        a,b,c,alpha,t1 = smp.symbols('a b c alpha t1')
        t2 = ((a+(b-1)*alpha)/(c*alpha))*(1 - smp.exp(-c*t1))
        cs, ci = smp.symbols('cs ci')
        K = cs/(t1+t2) + (ci/(t1+t2))*((((a+(b-1)*alpha)/c)*(t1 + (smp.exp(-c*t1)-1)/c))+(alpha*t2**2)/2)
        K = K.subs(a,A).subs(b,B).subs(c,C).subs(alpha,Alpha).subs(cs,setcost).subs(ci,holdcost)
        h = smp.diff(K,t1)
        l = []
        raphson(h,l)
        n = len(l)
        finalt1 = l[n-1]
        t2 = t2.subs(t1,l[n-1]).subs(a,A).subs(alpha,Alpha).subs(b,B).subs(c,C)
        K = K.subs(t1,l[n-1])
        if K<0 or l[n-1]<0 or t2<0: 
            K = "No optimised solution"
            l[n-1] = "No optimized solution"
            t2 = "No optimised solution"
        return render_template("staticcase.html", form=form, t2=t2, K=K, t1 = l[n-1])

    return render_template('staticcase.html', form = form)

@app.route("/Expdemandcase/<setcost>/<holdcost>/<A>/<B>/<C>", methods=['GET', 'POST'])
def expd(setcost, holdcost, A, B, C):
    form = expcase()
    A = float(A)
    B = float(B)
    C = float(C)
    setcost = float(setcost)
    holdcost = float(holdcost)
    if request.method=='POST':
        Alpha = form.alpha.data
        Alpha = float(Alpha)
        L = form.lambd.data
        L = float(L)
        a,b,c,alpha,t1,l = smp.symbols('a b c alpha t1 l')
        cs, ci = smp.symbols('cs ci')
        t2 = (smp.log(1 - l*a/(c*alpha)*(1 - smp.exp(-c*t1)) + (b-1)*l/(l-c)*(smp.exp(-l*t1)-smp.exp(-c*t1))))/-l
        K = cs/(t1+t2) + (ci/(t1+t2))*(a/c*(t1 + (smp.exp(-c*t1) - 1)/c) - (b-1)*alpha/(l-c)*((smp.exp(-c*t1)-1)/c - (smp.exp(-l*t1)-1)/l) + alpha/l*((1 - smp.exp(-l*t2))/l - t2*smp.exp(-l*t2)))
        K = K.subs(a,A).subs(b,B).subs(c,C).subs(alpha,Alpha).subs(cs,setcost).subs(ci,holdcost).subs(l,L)
        h = smp.diff(K,t1)
        li=[]
        raphson(h,li)
        n = len(li)
        finalt1 = li[n-1]
        t2 = t2.subs(t1,li[n-1]).subs(a,A).subs(alpha,Alpha).subs(b,B).subs(c,C).subs(l,L)
        print(t2)
        K = K.subs(t1,li[n-1])
        if K<0 or li[n-1]<0 or t2<0: 
            K = "No optimised solution"
            li[n-1] = "No optimized solution"
            t2 = "No optimised solution"
        return render_template("expcase.html", form=form, t2=t2, K=K, t1 = li[n-1])
    return render_template("expcase.html", form = form)

@app.route("/VendorRating", methods = ["GET","POST"])
def vendorrating():
    form = vendor()
    if request.method=='POST':
        d = datetime.strptime(str(form.deliveredon.data), "%d/%m/%y") - datetime.strptime(str(form.ddspecified.data), "%d/%m/%y")
        delay = d.days
        slr = (int(form.acceptedlot.data) + 0.75*int(form.underdeviation.data) + 0.50*int(form.inspected.data)+ 0)/int(form.numreceived.data)
        Quality_Rating = (50*slr + int(form.lineprob.data)+ int(form.customerlineprob.data)+ int(form.warrantyprob.data)+ int(form.response.data))
        delaycheck = 1 if delay<=0 else 0
        freightcheck = 1 if int(form.Freight.data)<0 else 0
        Delivery_Rating = delaycheck*60 + freightcheck*10 + (int(form.numreceived.data)/int(form.numspecified.data))*30
        Service_Rating = int(form.courtesy.data) + int(form.responsiveness.data)
        Overall_Rating = (60 * Quality_Rating + 35*Delivery_Rating + 5*Service_Rating)/100
        vendordetails = Vendor(Vendor = form.vendor.data, NumberSpecified = form.numspecified.data, NumberReceived = form.numreceived.data, AcceptedLot = form.acceptedlot.data, UnderDeviation = form.underdeviation.data, Inspected = form.inspected.data, Rejected = form.rejected.data, LineProblem = form.lineprob.data, CustomerLineProblem = form.customerlineprob.data, WarrantyProblem = form.warrantyprob.data, Response = form.response.data, DeliveryDateSpecified = form.ddspecified.data, Deliveredon = form.deliveredon.data, PremiumFreight = form.Freight.data, Courtesy = form.courtesy.data, Responsiveness=form.responsiveness.data, QualityRating = Quality_Rating, ServiceRating = Service_Rating, OverallRating = Overall_Rating, PartNumber = form.partnum.data, DeliveryRating=Delivery_Rating)
        db.session.add(vendordetails)
        db.session.commit()
        flash("Vendor Rating Recorded", 'success')
        return redirect(url_for('grade', vendor = form.vendor.data))
    return render_template("vendor.html", form = form)

@app.route("/VendorGrade/<vendor>", methods = ['GET','POST'])
def grade(vendor):
    records = Vendor.query.filter_by(Vendor=vendor).all()
    if request.method == 'POST':
        records=[]
        vendorname = request.form.get("vendorname")
        records = Vendor.query.filter_by(Vendor=vendorname).all()
        return render_template('grade.html', records = records)
    return render_template('grade.html', records = records)


if __name__ == '__main__':
    app.run()
