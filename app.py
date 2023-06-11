from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Frequencia(db.Model):
    id = db.Column('frequencia_id', db.Integer, primary_key=True, autoincrement=True)
    disciplina = db.Column(db.String(100))
    nome = db.Column(db.String(50))
    data = db.Column(db.Date())
    frequencia = db.Column(db.Boolean())

    def __init__(self, disciplina, nome, data, frequencia):
        self.disciplina = disciplina
        self.nome = nome
        self.data = data
        self.frequencia = frequencia

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        disciplina = request.form['disciplina']
        nome = request.form['nome']
        data = datetime.datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        frequencia = True if request.form.get('frequencia') else False

        nova_frequencia = Frequencia(disciplina, nome, data, frequencia)
        db.session.add(nova_frequencia)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('cadastrofrequencia.html')

@app.route("/listar")
def listar():
    frequencias = Frequencia.query.all()
    return render_template('listarfrequencias.html', frequencias=frequencias)

@app.route("/editar/<int:frequencia_id>", methods=['GET', 'POST'])
def editar(frequencia_id):
    frequencia = Frequencia.query.get(frequencia_id)

    if request.method == 'POST':
        frequencia.disciplina = request.form['disciplina']
        frequencia.nome = request.form['nome']
        frequencia.data = datetime.datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        frequencia.frequencia = True if request.form.get('frequencia') else False

        db.session.commit()
        return redirect(url_for('listar'))

    return render_template('editarfrequencia.html', frequencia=frequencia)

@app.route("/excluir/<int:frequencia_id>")
def excluir(frequencia_id):
    frequencia = Frequencia.query.get(frequencia_id)
    db.session.delete(frequencia)
    db.session.commit()
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)