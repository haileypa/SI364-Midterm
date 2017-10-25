## SI 364
## Fall 2017
## Midterm
## Hailey Patterson

from flask import Flask, request, render_template, redirect, url_for, flash, json, make_response
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'beermidtermapp'

app.debug = True 



class UserForm(FlaskForm):
	username =StringField('Enter your beer drinking alias:')
	submit = SubmitField('Submit')

class SearchBeerForm(FlaskForm):
    beer = StringField('Enter a beer:', validators=[ Required() ])
    submit = SubmitField('Submit')

class SearchBreweryForm(FlaskForm):
    brewery = StringField('Enter a brewery:', validators=[ Required() ])
    submit = SubmitField('Submit')


@app.route('/')
def hello_beer_world():
	userForm = UserForm()

	return render_template("home.html", userForm=userForm )

# @app.route('/setcookie', methods = ['POST', 'GET'])

@app.route('/search', methods= ['POST','GET'])
def search():
	beerForm = SearchBeerForm()
	breweryForm = SearchBreweryForm()
	if request.method == 'POST':
		if request.form['username']:
			username = request.form['username']
		else:
			username = "Beer Drinker with no Alias"
		resp = make_response(render_template("search_form.html", beerForm= beerForm, breweryForm=breweryForm, username=username))
		resp.set_cookie('username', username)

		return resp
	username = request.cookies.get('username')
	return render_template("search_form.html", beerForm= beerForm, breweryForm=breweryForm, username=username)


@app.route('/beerinfo', methods= ['POST','GET'])
def beer_info():
	base_url = "http://api.brewerydb.com/v2/beers"
	params = {}
	form = SearchBeerForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		name = form.beer.data
		params['name'] = name
		params['key'] = '01d35c18b7ed7936d4e01e7cb83eb0ee'
		r = requests.get(base_url, params= params).json()
		if 'data' in r.keys():
			data = r['data']
		else:
			data = 'NULL'
		username = request.cookies.get('username')
		now = datetime.now().time()
		today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
		return render_template("beer_info.html", data=data, name=name, current_time=datetime.now(), today5pm=today5pm, form=form, username=username)
	flash("ERROR:You didn't enter anything!")	
	return redirect(url_for('search'))


@app.route('/breweryinfo', methods= ['POST','GET'])
def brewery_info():
	base_url = "http://api.brewerydb.com/v2/search/"
	params = {}
	form = SearchBreweryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		name = form.brewery.data
		params['q'] = name
		params['type'] = 'brewery'
		params['key'] = '01d35c18b7ed7936d4e01e7cb83eb0ee'
		r = requests.get(base_url, params= params).json()
		if 'data' in r.keys():
			data = r['data']
		else:
			data = 'NULL'
		username = request.cookies.get('username')
		now = datetime.now().time()
		today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
		return render_template("brewery_info.html", data=data, name=name, current_time=datetime.now(), today5pm=today5pm, form=form, username=username)
	flash("ERROR:You didn't enter anything!")	
	return redirect(url_for('search'))	

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
