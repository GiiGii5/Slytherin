from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # Importamos la libreria de la base de datos 

db = SQLAlchemy() # Instanciamos la base de datos 
app = Flask(__name__) # Instanciamos la app Flask 

# Configurar la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# Inicializar la app con la extension 
db.init_app(app)
#Crear la primera tabla de la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String)

# Crear la ruta de acceso
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Crear login
@app.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form['user']
        password = request.form['pass']
        user = User.query.filter_by(usuario = usuario).first()
        if user and user.password == password:
            # Inicio de sesion exitoso
            return redirect("/")
        else:
            # Credenciales invalidas 
            return "Credenciales invalidas. Intenta de nuevo"
    return render_template("login.html")

# Crear registro
@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form['user']
        contra = request.form['pass']
        user = User(usuario = usuario, password = contra)
        db.session.add(user)
        db.session.commit()
        return "El registro se completo correctamente"
    return render_template("register.html")

# Editar id
@app.route("/editar/<id>", methods =["GET", "POST"])
def editar(id):
    if request.method == "POST":
        usuario = request.form['user']
        contra = request.form['pass']
        user = User.query.filter_by(id=id).first()
        user.usuario = usuario 
        user.password = contra
        db.session.commit()
    user = User.query.filter_by(id=id).first()
    return render_template("editar.html", usuario = user)

# Eliminar un dato
@app.route("/eliminar/<id>", methods =["POST"])
def eliminar(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return "Se elimino con exito"

@app.route("/info")
def info():
    nombre = "Penguin Academy"
    descripcion = "Lorem ipsum dolor sit amet"
    vision = "Lorem ipsum dolor sit amet"
    mision = "Lorem ipsum dolor sit amet"
    return render_template("info.html", nombre = nombre, descripcion = descripcion, vision = vision, mision = mision, nombres = db)

# Crea la base de datos (se ejecuta una sola vez para crear la base de datos y luego se deja como comentario pero no se elimina en caso de ser necesario, por si alguna vez se elimina la base de datos entonces solo vuelvo a ejecutar)
# with app.app_context():
#     db.create_all()

if __name__=="__main__":
    app.run(debug=True)