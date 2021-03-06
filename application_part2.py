import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
from nocache import nocache


from app import app, cursor, db

application_part2 = Blueprint('application_part2', __name__, template_folder='templates', static_folder='static')   

'''This function handles the education form after information is entered. 
It fetches data from the database education table and displays it in the placeholders.'''

@application_part2.route('part2', methods=['GET'])       #on submission of login details
@nocache

def part2(): 	
	sql = "SELECT status FROM education WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()
	if rows[0][0] == "new" :
		return render_template('application_part2.html', email_=session['email'], application_number=session['application_number'])
	else:
		sql = "SELECT * FROM education WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows = cursor.fetchall()
		rows = list(rows[0])
		btech_list = rows[2][1:-1].split(",")
		btech_list2 = rows[3][1:-1].split(",")
		mtech_list = rows[4][1:-1].split(",")
		mtech_list2 = rows[5][1:-1].split(",")
		phd_list = rows[6][1:-1].split(",")
		phd_thesis = rows[7][1:-1].split(",")
		gate_list = rows[8][1:-1].split(",")
		# name_list = rows[3][1:-1].split(",")
		params_ = [btech_list,mtech_list,phd_list,phd_thesis,gate_list,rows[9],rows[10],btech_list2,mtech_list2]
		print "retrieved properly"
		sql = "SELECT freeze_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		freeze_rows = cursor.fetchall()

		if freeze_rows[0][0] == "true":					# if application is freezed there should be no option to submit
			return render_template('application_readonly_freezed_part2.html',email_=session['email'],params=params_, application_number=session['application_number'])		
		elif rows[1] == "submitted" :					# if application is submitted, the form should be read only
			return render_template('application_readonly_part2.html',email_=session['email'],params=params_, application_number=session['application_number'])
		return render_template('application_placeholders_part2_.html',params=params_,email_=session['email'], application_number=session['application_number'])
	

'''The function that handles insertion/update in the database education table, once data has been entered or updated in the education form.'''

@application_part2.route('insert_2', methods=['GET','POST'])       #on submission of login details
@nocache
def insert_2(): 
	if (request.method =='POST'):
		bachelors_date_studied = request.form.getlist('bachelors_date_studied[]')
		bachelors_university = request.form.getlist('bachelors_university[]')
		bachelors_institute = request.form.getlist('bachelors_institute[]')
		bachelors_specialization = request.form.getlist('bachelors_specialization[]')
		bachelors_cgpa = request.form.getlist('bachelors_cgpa[]')
		bachelors_scale = request.form.getlist('bachelors_cgpa_scale[]')

		bachelors_info = "("+bachelors_date_studied[0]+","+bachelors_university[0]+","+bachelors_institute[0]+","+bachelors_specialization[0]+","+bachelors_cgpa[0]+","+bachelors_scale[0]+")"

		bachelors_info2 = "("
		if len(bachelors_date_studied)==2:
			bachelors_info2 += bachelors_date_studied[1]+","+bachelors_university[1]+","+bachelors_institute[1]+","+bachelors_specialization[1]+","+bachelors_cgpa[1]+","+bachelors_scale[1]
		else:
			bachelors_info2+=",,,,,"
		bachelors_info2+=")"



		masters_date_studied = request.form.getlist('masters_date_studied[]')
		masters_university = request.form.getlist('masters_university[]')
		masters_institute = request.form.getlist('masters_institute[]')
		masters_specialization = request.form.getlist('masters_specialization[]')
		masters_cgpa = request.form.getlist('masters_cgpa[]')
		masters_scale = request.form.getlist('masters_cgpa_scale[]')


		masters_info = "("+masters_date_studied[0]+","+masters_university[0]+","+masters_institute[0]+","+masters_specialization[0]+","+masters_cgpa[0]+","+masters_scale[0]+")"

		masters_info2 = "("
		if len(masters_date_studied)==2:
			masters_info2 += masters_date_studied[1]+","+masters_university[1]+","+masters_institute[1]+","+masters_specialization[1]+","+masters_cgpa[1]+","+masters_scale[1]
		else:
			masters_info2+=",,,,,"
		masters_info2+=")"



		phd_date_studied = request.form['phd_date_studied']
		phd_university = request.form['phd_university']
		phd_institute = request.form['phd_institute']
		phd_specialization = request.form['phd_specialization']
		phd_cgpa = request.form['phd_cgpa']
		phd_scale = request.form['phd_cgpa_scale']
		phd_date_thesis = request.form['phd_date_thesis']
		phd_date_defence = request.form['phd_date_defence']
		phd_edu_info = "("+phd_date_studied+","+phd_university+","+phd_institute+","+phd_specialization+","+phd_cgpa+","+phd_scale+")"
		phd_info = "("+phd_date_thesis+","+phd_date_defence+")"



		gate_year = request.form['gate_year']
		gate_score = request.form['gate_score']
		gate_info = "("+gate_year+","+gate_score+")"

		research_specialization = request.form['research_specialization']
		research_interest = request.form.getlist('research_interest[]')
		research_interest = [r.encode("utf8") for r in research_interest]
		temp="{"+ ",".join(research_interest)+"}"
		research_interest_str=temp


		# post_doc = request.form.getlist('post_doc_spec[]')
		# post_doc = [p.encode('utf8') for p in post_doc]
		# temp="{"+ ",".join(post_doc)+"}"
		# post_doc_str=temp
		bachelors2_params = []
		if len(bachelors_date_studied)==2:
			bachelors2_params.append(bachelors_date_studied[1])
			bachelors2_params.append(bachelors_university[1])
			bachelors2_params.append(bachelors_institute[1])
			bachelors2_params.append(bachelors_specialization[1])
			bachelors2_params.append(bachelors_cgpa[1])
			bachelors2_params.append(bachelors_scale[1])
		else:
			for i in range(6):
				bachelors2_params.append("")

		masters2_params = []
		if len(masters_date_studied)==2:
			masters2_params.append(masters_date_studied[1])
			masters2_params.append(masters_university[1])
			masters2_params.append(masters_institute[1])
			masters2_params.append(masters_specialization[1])
			masters2_params.append(masters_cgpa[1])
			masters2_params.append(masters_scale[1])
		else:
			for i in range(6):
				masters2_params.append("")

		params = [[bachelors_date_studied[0],bachelors_university[0],bachelors_institute[0],bachelors_specialization[0],bachelors_cgpa[0],bachelors_scale[0]],
		[masters_date_studied[0],masters_university[0],masters_institute[0],masters_specialization[0],masters_cgpa[0],masters_scale[0]],[phd_date_studied,phd_university,phd_institute,phd_specialization,phd_cgpa,phd_scale],[phd_date_thesis,phd_date_defence],[gate_year,gate_score],research_specialization,research_interest,bachelors2_params,masters2_params]

		sql = "UPDATE education SET status='%s', bachelors='%s',bachelors2='%s',masters='%s',masters2='%s',phd='%s',phd_thesis='%s',gate='%s',research_specialization='%s',research_interest='%s' WHERE application_no='%d';" % ("modified", bachelors_info,bachelors_info2, masters_info,masters_info2, phd_edu_info, phd_info, gate_info,research_specialization,research_interest_str, int(session['application_number']))
		print sql

		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form education is stored"
		except:
			print "Info error"

		# return "Saved!"
	return render_template('application_placeholders_part2_.html',params=params, email_=session['email'], application_number=session['application_number'])
