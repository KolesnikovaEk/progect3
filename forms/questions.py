from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class QuestionsForm(FlaskForm):
    #title = StringField('Заголовок', validators=[DataRequired()])
    #question1 = TextAreaField("Любите ли вы спорт?")
    que1 = SelectField("Любите ли вы достопримечательности?", choices=[('да', 'Да'), ('нет', 'Нет')])
    que2 = SelectField("Любите ли вы театр?", choices=[('да', 'Да'), ('нет', 'Нет')])
    que3 = SelectField("Любите ли вы природу?", choices=[('да', 'Да'), ('нет', 'Нет')])
    submit = SubmitField('Сдать')
