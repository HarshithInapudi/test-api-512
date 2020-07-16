from flask import Flask, render_template, redirect, url_for, abort, flash, jsonify
from application import app, db, r
from application.forms import LoginForm, SMS
from application.models import Account, Phone
from flask_login import login_user, current_user, logout_user, login_required


#creates defined tables
db.create_all()
db.session.commit()

#function to convert byte type to str
def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data


#creating all the routes

@app.route("/")
def about():
    return render_template('about.html')



@app.route('/API')
@login_required
def API():
	return render_template('API.html', title='API')


#defining global variables for later use
a = None
t = None
c = None
usr = None
id_ = 0 
keys = []
values = []
dic = []



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('API'))
	form = LoginForm()
	if form.validate_on_submit():

		#assigning the values entered in the form to variables
		uname = form.username.data
		pas = form.password.data

		global a, usr, c
		c = Account.query.filter_by(username=uname).first()
		
		usr = uname

		#checking if the credentials entered are valid 
		logn = Account.query.filter_by(username=uname, auth_id=pas).first()
		if logn is not None:
			flash('You have been logged in', 'success')
			login_user(c, remember=form.remember.data)
			return redirect(url_for('API'))

		else:
			abort(403)
		log = Account.query.filter_by(username=uname).first()
		
	return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))



@app.route('/API/inbound/sms', methods=['GET', 'POST'])
@login_required
def inbound():
	form = SMS()
	if form.validate_on_submit():

		#assigning the values entered in the form to variables
		_from_ = form.from_.data
		_to_ = form.to.data
		_text_ = form.text.data
		task = {'from':_from_, 'to':_to_}


		global a, t, c, usr
		a = c.id
		t = _to_

		# defining conditions for respective JSON responses

		if len(_to_)<1 or len(_from_)<1 :
		 	return jsonify(message = 'Please enter all the parameters', error = 'parameter missing')
		
		elif t is not None:
			i = Phone.query.filter_by(number=t, account_id=a).first()
			if i is None:
				return jsonify(message = 'There is no such number present in current user\'s table', error = 'to parameter not found')
			
			else:
				if 'STOP' in _text_:
					global id_
					r.hmset(id_, task)
					r.expire(id_, 14400)
					id_ += 1 
					return jsonify(message = 'inbound sms ok', msg = 'values are cached', text= _text_)

				else:
					return jsonify(message = 'inbound sms ok', error = '', text= _text_)

	return render_template('inbound.html', form=form)



@app.route('/API/outbound/sms', methods=['GET', 'POST'])
@login_required
def outbound_sms():
	form = SMS()
	if form.validate_on_submit():
		#assigning the values entered in the form to variables
		_from_ = form.from_.data
		_to_ = form.to.data
		_text_ = form.text.data
		task = {'from':_from_, 'to':_to_}

		global a, t, usr
		t = _from_

		# defining conditions for respective JSON responses

		if len(_to_)<1 or len(_from_)<1 :
		 	return jsonify(message = 'Please enter all the parameters', error = 'parameter missing')

		elif t is not None:
			i = Phone.query.filter_by(number=t, account_id=a).first()
			if i is None:
				return jsonify(message = 'There is no such number present in current user\'s table', error = 'from parameter not found')
			
			else:
				for g in r.keys():
					keys.append(g)
				for h in keys:
					j = r.hgetall(h)
					values.append(j)
				for k in values:
					l = convert(k)
					dic.append(l)
				for m in dic:
					if (m['from'] == str(_from_) and m['to'] == str(_to_)):
						return jsonify(message= 'There was a request to block', error= "sms from " + str(_from_) + " to " + str(_to_) + " blocked by STOP request")
					else:
						return jsonify(message = 'outbound sms ok', error = '', text= _text_)

	return render_template('outbound.html', form=form)
