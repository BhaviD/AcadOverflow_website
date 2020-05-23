# Views are handlers that responds to requests from browsers and clients

# Handlers are written as Python Functions. 
# Each View Function is mapped to one or more request URLs.

from flask import render_template, flash, redirect, url_for, session, logging, request, json, jsonify
from app import app
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from operator import attrgetter
from flask_paginate import Pagination, get_page_args
import sys
import re

sys.path.insert(0, "./app")
sys.path.insert(0, "./")

# import tensorflow as tf
# import keras
import os
import numpy as np
# import spacy
import pandas as pd
# import keras.losses
# import pickle
# import keras.backend as K
import utils
import ipdb

# from keras.models import load_model
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from sklearn.preprocessing import MultiLabelBinarizer
# from search import searchresults
# from utils import preprocess_text

# EN = spacy.load('en_core_web_sm')

sys.path.append("./app")
sys.path.append("./app/gql_client")
sys.path.append("./app/session_data")

from session_data.data_handling import get_preprocessed_data
from session_data.data_handling import csv_register_user
from session_data.data_handling import csv_user_exists
from session_data.data_handling import csv_get_login_details
from session_data.data_handling import csv_post_question
from session_data.data_handling import csv_query_question_for_list
from session_data.data_handling import csv_query_question_for_page
from session_data.data_handling import csv_post_answer
from session_data.data_handling import csv_query_user_questions


# Custom loss function to handle multilabel classification task
# def multitask_loss(y_true, y_pred):
# 	# Avoid divide by 0
# 	y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
# 	# Multi-task loss
# 	return K.mean(K.sum(- y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred), axis=1))

# def load_tag_encoder(data):
# 	data.tags = data.tags.apply(lambda x: x.split('|'))
# 	tag_freq_dict = {}
# 	for tags in data.tags:
# 		for tag in tags:
# 			if tag not in tag_freq_dict:
# 				tag_freq_dict[tag] = 0
# 			else:
# 				tag_freq_dict[tag] += 1
# 	# Get most common tags
# 	tags_to_use = 600
# 	tag_freq_dict_sorted = sorted(tag_freq_dict.items(), key=lambda x: x[1], reverse=True)
# 	final_tags = tag_freq_dict_sorted[:tags_to_use]
# 	for i in range(len(final_tags)):
# 		final_tags[i] = final_tags[i][0]

# 	final_tag_data = []
# 	X = []
# 	for i in range(0, len(data)):
# 		temp = []
# 		for tag in data.iloc[i].tags:
# 			if tag in final_tags:
# 				temp.append(tag)
# 			if(temp != []):
# 				final_tag_data.append(temp)
# 				X.append(data.iloc[i].processed_title)
# 	tag_encoder = MultiLabelBinarizer()
# 	tags_encoded = tag_encoder.fit_transform(final_tag_data)
# 	return tag_encoder

# def predict_tags(text):
# 	# Tokenize text
# 	x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
# 	# Predict
# 	with graph.as_default():
# 		prediction = model.predict([x_test])[0]
# 	for i,value in enumerate(prediction):
# 		if value > 0.5:
# 			prediction[i] = 1
# 		else:
# 			prediction[i] = 0
# 	tags = tag_encoder.inverse_transform(np.array([prediction]))
# 	return tags

data = get_preprocessed_data()
# tag_encoder = load_tag_encoder(data)

# MAX_SEQUENCE_LENGTH = 300
# with open('./ML_Module/models/tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
# keras.losses.multitask_loss = multitask_loss
# global graph
# graph = tf.get_default_graph()
# model = load_model('./ML_Module/models/Tag_predictor.h5')


# Index
@app.route('/')
@app.route('/index')
def index():
	if 'logged_in' in session:
		return redirect(url_for('home'))
	return render_template('index.html')

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			# flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

# Register Form Class
class RegisterForm(Form):
	fname = StringField('FirstName', [validators.Length(min=1, max=50)])
	lname = StringField('LastName', [validators.Length(min=1, max=50)])
	emailId = StringField('EmailId', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match!! Try Again.')
	])
	confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	# form = RegisterForm(request.form)
	if request.method == 'POST':
		emailId = request.form['emailId']

		if csv_user_exists(emailId):
			flash ('Already registered with emailId: {}!!'.format(emailId), 'danger')
			return render_template('register.html')

		fname = request.form['fname']
		lname = request.form['lname']

		# check entered passwords
		password = sha256_crypt.encrypt(request.form['password'])
		confirm_password = request.form['confirm_password']

		if not sha256_crypt.verify(confirm_password, password):
			flash('Passwords do not match!!', 'danger')
			return redirect(url_for('register'))

		try:
			csv_register_user(emailId, fname, lname, password)
			flash('{} registered!! Please log in'.format(emailId), 'success')
			return redirect(url_for('login'))
		except Exception as e:
			print(e)
			flash('Something went wrong!! Please try again', 'danger')

	return render_template('register.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'logged_in' in session:
		return redirect(url_for('home'))

	if request.method != 'POST':
		return render_template('login.html')

	# Get Form Fields
	emailId = request.form['emailId']
	password_candidate = request.form['password']
	
	user = csv_get_login_details(emailId)
	if not user:
		error = 'EmailId: {} not registered!!'.format(emailId)
		return render_template('login.html', error=error)

	password = user["Password"]
	fname = user["FirstName"]
	lname = user["LastName"]

	# Compare Passwords
	if not sha256_crypt.verify(password_candidate, password):
		error = 'Incorrect Passord!!'
		return render_template('login.html', error=error)

	# Passed
	session['logged_in'] = True
	session['userId'] = int(user["Id"])
	session['emailId'] = emailId
	session['fname'] = fname
	session['lname'] = lname
	session['profile_img'] = fname + ".jpg"

	print (session)

	return redirect(url_for('home'))


# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))

@app.route('/home')
@is_logged_in
def home():
	return render_template('home.html')

@app.route('/ask_question')
def ask_question():
	return render_template('ask_question.html')

search_results = [
    {
      "Body": " comparaison two list python string like", 
      "similarity_score": "1.000", 
	  "Id": "30453",
      "Tags": "python|list", 
      "Title": "Comparaison of two list in python", 
      "url": "https://stackoverflow.com/questions/16295770", 
      "votes": "2.9678147352433087e-05"
    }, 
    {
      "Body": " compare two list list python two list", 
      "similarity_score": "0.945", 
	  "Id": "144809",
      "Tags": "python|python-2.7|python-3.x|list|append", 
      "Title": "Compare two list of list in python", 
      "url": "https://stackoverflow.com/questions/46621588", 
      "votes": "-0.0007734271932980822"
    }, 
    {
      "Body": " two different randomchoices list python complete python noob slowly wrapping head around making 1v1 halo 3 tournament style program randomly matches players picks map gametype etc", 
      "similarity_score": "0.941", 
	  "Id": "80715",
      "Tags": "python|random", 
      "Title": "Two different random.choices from a list (python)", 
      "url": "https://stackoverflow.com/questions/32492428", 
      "votes": "-0.00037187452297282456"
    }, 
    {
      "Body": " python concatenation two list new python need", 
      "similarity_score": "0.931", 
	  "Id": "45585",
      "Tags": "python|string|list|python-2.7|concatenation", 
      "Title": "Python, concatenation of two list", 
      "url": "https://stackoverflow.com/questions/21817132", 
      "votes": "-0.00010417274275598612"
    }, 
    {
      "Body": " combine two list list list python let say print c 10 0 14 1 16 2", 
      "similarity_score": "0.931", 
	  "Id": "97353",
      "Tags": "python|list|python-2.7", 
      "Title": "How combine two list into list of list at python?", 
      "url": "https://stackoverflow.com/questions/36695176", 
      "votes": "0.0008327834880029483"
    }
]

@app.route('/AddQuestionNext',methods=['GET','POST'])
def AddQuestionNext():
	# To find out the method of request, use 'request.method'
	if request.method == "GET":
		title = request.args.get("title")
		body = request.args.get("body")	
	elif request.method == "POST":
		title = request.form['title']
		body = str(request.form['body'])
	# search_results = searchresults(title, 5)
	# tags_list = list(predict_tags(title))
	tags = ["tag1", "tag2", "tag3"]
	clean = re.compile('<.*?>')
	body = re.sub(clean, '', body)
	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	total = len(search_results)
	p_questions = search_results[offset: offset + per_page]
	pagination = Pagination(page=page, per_page=per_page, total=total)
	return render_template('post_question_confirmation.html', similar_questions=p_questions, page=page, per_page=per_page, pagination=pagination, title = title, body = body, tags_list = tags)


@app.route('/SearchQuestionNext',methods=['GET','POST'])
def SearchQuestionNext():
	# To find out the method of request, use 'request.method'
	id_list = [75, 76, 77, 78, 79, 80]
	questions = []
	for item in id_list:
		question = csv_query_question_for_list(item)
		questions.append(question)
	print(questions)
	if request.method == "GET":
		title = request.args.get("question")
		
	elif request.method == "POST":
		title = request.form['question']
	# tags_list = ['tag1', 'tag2']
	print(title)
	# print(body)
	return render_template('search_questions.html',title = title, id_list = questions)

# Dummy Page to be deleted once the question link works
@app.route('/dummy')
def dummy():
	return render_template('dummy.html')

# Display question details
@app.route('/question_details', methods = ['GET', 'POST'])
def question_details():
	print(request.method)
	if request.method == 'POST':
		id = request.form['question_id']
	elif request.method == 'GET':
		id = request.args.get("question_id")
	print(id)
	try:
		print('trying to fetch the question...')
		question = csv_query_question_for_page(id)
		if question is None:
			flash('No such question found', 'warning')
			return render_template('dummy.html', question = question)
		print('Question received')
		flash('Question details received', 'success')
		return render_template('question_details.html', question = question)
	except Exception as e:
		print(e)
		flash('Something went wrong!! : Exception', 'danger')
	return "Something went wrong...!!!"

#Posting a new answer
@app.route('/post_new_answer', methods = ['GET', 'POST'])
def post_new_answer():
	if request.method == 'POST':
		aBody = str(request.form['aBody'])
		clean = re.compile('<.*?>')
		aBody = re.sub(clean, '', aBody)
		print(aBody)
		qId = request.form['qId']
		print(qId)
		userId = session['userId']
		print(userId)
		try:
			print('trying...')
			csv_post_answer(qId, aBody, userId)
			print('Answer added to the database')
			flash('New answer added', 'success')
			return redirect(url_for('question_details', question_id = qId))
		except Exception as e:
			print(e)
			flash('Something went wrong!! : Exception', 'danger')
	elif request.method == 'GET':
		flash('Something went wrong!! Please try again', 'danger')
	return "Something went wrong...!!!"

@app.route('/post_new_question', methods = ['GET', 'POST'])
def post_new_question():
	if request.method == 'POST':
		qtitle = request.form['qtitle']
		qbody = str(request.form['qbody'])
		clean = re.compile('<.*?>')
		qbody = re.sub(clean, '', qbody)
		tags_list = request.form['qtags']
		userId = session['userId']
		try:
			print('trying...')
			csv_post_question(qtitle, qbody, tags_list, userId)
			flash('New Question added', 'success')
			return redirect(url_for('home'))
		except Exception as e:
			print(e)
			flash('Something went wrong!! : Exception', 'danger')
	elif request.method == 'GET':
		flash('Something went wrong!! Please try again', 'danger')
	return "Something went wrong...!!!"

@app.route('/my_questions')
def my_questions():
	questions = csv_query_user_questions(session['userId'])

	# TODO: what if there are 0 questions by this user?
	# if not questions:
	#	?

	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	print ("page, per_page, offset: ", page, per_page, offset)
	total = len(questions)
	pagination_questions = questions[offset: offset + per_page]
	pagination = Pagination(page=page, per_page=per_page, total=total)
	for i in range (10):
		print ("Question {}: ".format(i), pagination_questions[i])
	return render_template('my_questions.html', questions=pagination_questions, page=page, per_page=per_page, pagination=pagination)
