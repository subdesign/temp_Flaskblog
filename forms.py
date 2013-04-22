from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError

class ArticleForm(Form):
	title = TextField("Title", [validators.Required("Title field is missing")])
	content = TextAreaField("Content", [validators.Required("Content field is missing")])
	submit = SubmitField("Send")
