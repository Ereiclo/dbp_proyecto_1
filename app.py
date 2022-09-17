#f
##



####si
###
###
'''



me gusta algo:
no
si
'''
from logging import error

# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask.wrappers import Response
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, migrate
import datetime
import json
import datetime

app = Flask(__name__) #uwuwuwu

# no se olviden de crear la base de datos en postgres proyecto1

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://grupo5:1234@localhost:5432/proyecto1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Rol(db.Model):
    __tablename__ = "rol"
    id_rol = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Rol: {self.id_rol}, {self.rol}>"


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(60), nullable=False)
    usuario = db.Column(db.String(70), nullable=False)
    contrasenia = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha_de_nacimiento = db.Column(db.Date, nullable=False)
    dinero_en_cuenta = db.Column(db.Float, nullable=False, default=0)
    ult_inicio_sesion = db.Column(db.DateTime, nullable=False)
    rol = db.Column(db.Integer, db.ForeignKey(
        "rol.id_rol"), nullable=False, default=1)

    def __repr__(self):
        return f'<Usuario: {self.id_persona}, {self.nombre}, {self.apellidos}, {self.usuario},{self.contrasenia}, {self.email},{self.rol}>'


class Tarjeta(db.Model):
    __tablename__ = 'tarjeta_de_credito'
    id_tarjeta = db.Column(db.Integer, primary_key=True)
    n_tarjeta = db.Column(db.String(1000), nullable=False)
    ccv = db.Column(db.Integer, nullable=False)
    titular = db.Column(db.String(1000), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id_persona'), nullable=False)

    def __repr__(self):
        return f'<Tarjeta: {self.id_tarjeta},{self.n_tarjeta},{self.id_usuario}>'


class Solicitud(db.Model):
    __tablename__ = "solicitudes"
    id_solicitud = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000), nullable=False)
    monto_solicitado = db.Column(db.Float, nullable=False)
    id_persona = db.Column(db.Integer, db.ForeignKey(
        'usuario.id_persona'), nullable=False)

    def __repr__(self):
        return f"<Solicitud: {self.id_solicitud}, {self.description}, {self.monto_solicitado},{self.id_persona}>"


class Equipos(db.Model):
    __tablename__ = "equipos"
    id_equipo = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(50), nullable=False)
    n_victorias = db.Column(db.Integer, nullable=False)
    n_derrotas = db.Column(db.Integer, nullable=False)
    n_empates = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Todo: {self.id_equipo},{self.pais},{self.n_derrotas},{self.n_victorias},{self.n_empates}>'


class Partidos(db.Model):
    __tablename__ = "partidos"
    id_partido = db.Column(db.Integer, primary_key=True)
    equipo_a = db.Column(db.Integer, db.ForeignKey(
        "equipos.id_equipo"), nullable=False)
    equipo_b = db.Column(db.Integer, db.ForeignKey(
        "equipos.id_equipo"), nullable=False)
    porcentaje_1 = db.Column(db.Float, nullable=False)
    porcentaje_2 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Todo: {self.id_partido},{self.equipo_a},{self.equipo_b}>'


class Apuestas(db.Model):
    __tablename__ = "apuestas"
    id_apuesta = db.Column(db.Integer, primary_key=True)
    id_partido = db.Column(db.Integer, db.ForeignKey(
        "partidos.id_partido"), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "usuario.id_persona"), nullable=False)

    def __repr__(self):
        return f'<Todo: {self.id_apuesta},{self.id_partido},{self.monto},{self.id_usuario}>'


def comprobar_si_hay_digitos(password):
    numeros_necesarios = [str(x) for x in range(0, 10)]
    for n in numeros_necesarios:
        if n in password:
            return True

    return False


def comprobar_si_solo_hay_numeros(cadena):

    for i in cadena:
        if (i.lower()).isalpha() or i.lower() in 'áéíóúñ@!#%&/()=?¿|°¬´"¨+*}{"[]`^~,;.:-_¡' + "'":
            return False
    return True


def comprobar_si_solo_hay_numeros2(cadena):

    for i in cadena:
        if (i.lower()).isalpha() or i.lower() in 'áéíóúñ@!#%&/()=?¿|°¬´"¨+*}{"[]`^~,;:_¡' + "'":
            return False
    return True


@app.route('/comprobar-credenciales', methods=['POST'])
def comprobar_credenciales():
    response = {}

    usuario = request.get_json()['usuario']
    password = request.get_json()['password']
    lista_usuarios = Usuario.query.all()
    
    print(usuario)
    if lista_usuarios==[]:
        response['resultado'] = "incorrect_username"
        return jsonify(response)

    for u in lista_usuarios:
        print(u.usuario == usuario)
        if usuario == u.usuario and password == u.contrasenia:
            response['resultado'] = "success"
            response['username'] = u.usuario
            response['password'] = u.contrasenia
            response['id'] = u.id_persona
            response['dinero_en_cuenta'] = u.dinero_en_cuenta

            u.ult_inicio_sesion = datetime.datetime.now()

            db.session.commit()
            break

        elif usuario == u.usuario and password != u.contrasenia:
            response['resultado'] = "incorrect_password"
            break
        else:
            response['resultado'] = "incorrect_username"

    return jsonify(response)


@app.route('/comprobar-credenciales-android', methods=['GET'])
def comprobar_credenciales_android():
    print("ksajdfklñ")
    response = ""
    dicc= request.args
    usuario = dicc.get('username')
    password = dicc.get('password')

    lista_usuarios = Usuario.query.all()
    
    print(usuario)
    if lista_usuarios==[]:
        response = "resultado:incorrect_username"
        return response

    for u in lista_usuarios:
        print(u.usuario == usuario)
        if usuario == u.usuario and password == u.contrasenia:
            response = "resultado:success,"
            response+= "username:" + u.usuario
            response+= ",password:"+ u.contrasenia
            response+= ",id:" + str(u.id_persona)
            response+= ",dinero_en_cuenta:"+ str(u.dinero_en_cuenta)

            u.ult_inicio_sesion = datetime.datetime.now()

            db.session.commit()
            break

        elif usuario == u.usuario and password != u.contrasenia:
            response= "resultado:incorrect_password"
            break
        else:
            response= "resultado:incorrect_username"

    return response
    


@app.route('/get-credit-card-number',methods=['GET'])
def get_credit_card_number():
    id= request.args.get("id")
    tarjetas = db.session.query(Tarjeta).filter(Tarjeta.id_usuario == id).all()
    print(str(tarjetas[0].n_tarjeta))

    return str(tarjetas[0].n_tarjeta)

   
   

@app.route('/cantidad-tarjetas',methods=['GET'])
def cantidad_tarjetas():
    id = request.args.get("id")
        
    tarjetas = db.session.query(Tarjeta).filter(Tarjeta.id_usuario == id).all()
    print(tarjetas)

    if tarjetas != None:
        return str(len(tarjetas))
    return "-1"



@app.route('/depositar', methods=['POST'])
def depositar():
    d = request.form
    print("Esto es depositar", d)

    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]  

    tarjetas = db.session.query(Tarjeta).filter(Tarjeta.id_usuario == id).all()
    nms = []
    for tarjeta in tarjetas:
        nms.append(tarjeta.n_tarjeta)

    leng = 0
    print(tarjetas)
    if tarjetas != None:
        leng = len(tarjetas)
    
    print(leng,"<- cantidad de tarjetas")

    return render_template('depositar.html', d=d, leng=leng, nms=nms, dinero_en_cuenta = u.dinero_en_cuenta)


@app.route("/todos/<card_id>/delete-card", methods=["DELETE"])
def delete_todo_by_id(card_id):

    tarjetas = db.session.query(Tarjeta).filter(Tarjeta.id_usuario == card_id).all()
    t = tarjetas[0]
    db.session.delete(t)
    db.session.commit()
    return jsonify({"success": True})



@app.route("/todos/<card_id>/delete-card",methods=['GET'])
def delete_todo_by_id2(card_id):

    tarjetas = db.session.query(Tarjeta).filter(Tarjeta.id_usuario == card_id).all()
    t = tarjetas[0]
    db.session.delete(t)
    db.session.commit()
    return "success"


@app.route('/partidos', methods=['POST'])
def partidos():
    d = request.form
    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]  


    print("Esto es partidos", d)

    return render_template('partidos.html', data2=Equipos.query.all(), data=Partidos.query.all(), d=d, dinero_en_cuenta = u.dinero_en_cuenta)


@app.route('/apuestas', methods=['POST'])
def apuestas():
    d = request.form
    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]  


    print("Esto es apuestas", d)

    return render_template('apuestas.html', data=Apuestas.query.all(), data2=Partidos.query.all(), data3=Usuario.query.all(), data4=Equipos.query.all(), d=d, dinero_en_cuenta = u.dinero_en_cuenta)



@app.route('/informacion', methods=['POST'])

def informacion():
    d = request.form
    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]
    print(u)

    print("Esto es informacion", d)
    print(u.usuario)
    print(u.nombre)
    print(u.apellidos)
    print(u.dinero_en_cuenta)
    print(u.email)
    print(u.fecha_de_nacimiento)
    print(u.contrasenia)

    return render_template('informacion.html', d=d , usuario = u.usuario, nombre=u.nombre, apellidos=u.apellidos, dinero_en_cuenta=u.dinero_en_cuenta,email=u.email,fecha= u.fecha_de_nacimiento,p = u.contrasenia)

@app.route('/ask_money',methods=['GET'])
def ask_money():
    d = request.args
    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]






    print(u.dinero_en_cuenta)




    return str(u.dinero_en_cuenta)




@app.route('/inf', methods=['GET'])
def inf():
    d = request.args
    id = d['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]
    print(u)

    
    print(u.usuario)
    print(u.nombre)
    print(u.apellidos)
    print(u.dinero_en_cuenta)
    print(u.email)
    print(u.fecha_de_nacimiento)
    print(u.contrasenia)

    return str(u.usuario) + "," + str(u.nombre) + "," + str(u.apellidos) + "," + str(u.fecha_de_nacimiento) + "," + str(u.dinero_en_cuenta) + "," + str(u.contrasenia) + "," + str(u.email)



@app.route('/register-verify', methods=['POST'])
def register_verify():
    response = {}
    dicc_respuesta = request.get_json()

    print(dicc_respuesta)

    usuario = dicc_respuesta['usuario']
    apellidos = dicc_respuesta['apellidos']

    password = dicc_respuesta['password']
    confirm_password = dicc_respuesta['confirm-password']

    longitud_necesaria = 8
    if(dicc_respuesta['fecha_nacimiento'] == ""):
        response['resultado'] = "null_birthdate"
        return response
    
    fecha_nacimiento = datetime.date.fromisoformat(
        dicc_respuesta['fecha_nacimiento'])
    fecha_actual = datetime.date.today()

    print(fecha_nacimiento)
    tabla_usuario = Usuario.query.all()
    lista_usuarios = []

    for i in tabla_usuario:
        lista_usuarios.append(i.usuario)
    print(tabla_usuario)
    print(lista_usuarios)

    if fecha_nacimiento.year > fecha_actual.year-18:
        response['resultado'] = "invalid_birthdate"
    elif fecha_nacimiento.month > fecha_actual.month and fecha_nacimiento.year == (fecha_actual.year-18):
        response['resultado'] = "invalid_birthdate"
    elif fecha_nacimiento.day > fecha_actual.day and fecha_nacimiento.month == fecha_actual.month and fecha_nacimiento.year == (fecha_actual.year-18):
        response['resultado'] = "invalid_birthdate"

    elif password != confirm_password:
        response['resultado'] = "different_password"
    elif len(password) < longitud_necesaria:
        response['resultado'] = "password_invalid_length"

    elif not comprobar_si_hay_digitos(password):
        response['resultado'] = "password_missing_digits"

    elif usuario in lista_usuarios:
        response['resultado'] = 'username_already_exists'

    else:
        response['resultado'] = "success"

    return jsonify(response)


@app.route('/register-verify-android', methods=['GET'])
def register_verify_android():
    response = ""
    dicc_respuesta = request.args

    print(dicc_respuesta)

    usuario = dicc_respuesta['usuario']
    apellidos = dicc_respuesta['apellidos']
    email = dicc_respuesta.get('email')
    nombre = dicc_respuesta.get('nombre')
    
    ult = datetime.datetime.now()
    password = dicc_respuesta['password']
    confirm_password = dicc_respuesta['confirm-password']

    longitud_necesaria = 8
    if(dicc_respuesta['fecha_nacimiento'] == ""):
        response = "resultado:null_birthdate"
        return response

    fecha_nacimiento = datetime.date.fromisoformat(
        dicc_respuesta['fecha_nacimiento'])
    fecha_actual = datetime.date.today()

    print(fecha_nacimiento)
    tabla_usuario = Usuario.query.all()
    lista_usuarios = []

    for i in tabla_usuario:
        lista_usuarios.append(i.usuario)
    print(tabla_usuario)
    print(lista_usuarios)

    if fecha_nacimiento.year > fecha_actual.year-18:
        response= "resultado:invalid_birthdate"
    elif fecha_nacimiento.month > fecha_actual.month and fecha_nacimiento.year == (fecha_actual.year-18):
        response = "resultado:invalid_birthdate"
    elif fecha_nacimiento.day > fecha_actual.day and fecha_nacimiento.month == fecha_actual.month and fecha_nacimiento.year == (fecha_actual.year-18):
        response= "resultado:invalid_birthdate"

    elif password != confirm_password:
        response = "resultado:different_password"
    elif len(password) < longitud_necesaria:
        response= "resultado:password_invalid_length"

    elif not comprobar_si_hay_digitos(password):
        response= "resultado:password_missing_digits"

    elif usuario in lista_usuarios:
        response= 'resultado:username_already_exists'

    else:
        u = Usuario(nombre=nombre, apellidos=apellidos, usuario=usuario, contrasenia=password,
                email=email, fecha_de_nacimiento=fecha_nacimiento, ult_inicio_sesion=ult)
        db.session.add(u)
        db.session.commit()
        response= "resultado:success"
    print(response)
    return response

    
    
    
      
    
    
    
@app.route('/change_data_android', methods=['GET'])
def change_data_android():
    response = ""
    dicc_respuesta = request.args
    print(dicc_respuesta)
    id = dicc_respuesta['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]  
        
    email = dicc_respuesta['email']
    password = dicc_respuesta['password']
    confirm_password = dicc_respuesta['confirm-password']

    longitud_necesaria = 8
    
        
        
    if email != u.email:
        u.email = email
        response= "success"
    


    if password != confirm_password:
        response= "different_password"
    elif len(password) < longitud_necesaria:
        response= "password_invalid_length"

    elif not comprobar_si_hay_digitos(password):
        response= "password_missing_digits"
    

    elif password!= u.contrasenia:
        u.contrasenia= password
        response= "success"

    db.session.commit()

    return response
    

    

    


@app.route('/change_data', methods=['POST'])
def change_data():
    response = {}
    dicc_respuesta = request.get_json()
    print(dicc_respuesta)
    id = dicc_respuesta['id']
    u = (db.session.query(Usuario).filter(Usuario.id_persona == id).all())[0]  
        
    email = dicc_respuesta['email']
    password = dicc_respuesta['password']
    confirm_password = dicc_respuesta['confirm-password']

    longitud_necesaria = 8
    
        
        
    if email != u.email:
        u.email = email
        response['resultado'] = "success"
    


    if password != confirm_password:
        response['resultado'] = "different_password"
    elif len(password) < longitud_necesaria:
        response['resultado'] = "password_invalid_length"

    elif not comprobar_si_hay_digitos(password):
        response['resultado'] = "password_missing_digits"

    

    elif password!= u.contrasenia:
        u.contrasenia= password
        response['resultado'] = "success"

    db.session.commit()

    return jsonify(response)

@app.route('/create-user', methods=['POST'])
def create_user():

    diccionario = request.form
    username = diccionario.get("username")
    password = diccionario.get("password")
    email = diccionario.get('email')
    nombre = diccionario.get('nombre')
    apellidos = diccionario.get('apellidos')
    fecha = datetime.date.fromisoformat((diccionario.get('fecha')))
    ult = datetime.datetime.now()

    u = Usuario(nombre=nombre, apellidos=apellidos, usuario=username, contrasenia=password,
                email=email, fecha_de_nacimiento=fecha, ult_inicio_sesion=ult)
    db.session.add(u)
    db.session.commit()

    print(diccionario)

    return redirect(url_for("index"))


@app.route('/comprobar-tarjeta', methods=['POST'])
def comprobar_tarjeta():
    respuesta = {}
    dicc_respuesta = request.get_json()
    parte1 = dicc_respuesta['parte1']
    parte2 = dicc_respuesta['parte2']
    parte3 = dicc_respuesta['parte3']
    ccv = dicc_respuesta['cvv']
    propietario = dicc_respuesta['titular']

    if len(parte1) != 4 or len(parte2) != 4 or len(parte3) != 4 or not comprobar_si_solo_hay_numeros(parte1+parte2+parte3):
        respuesta['resultado'] = "invalid_card_number"
    elif len(ccv) != 3 or not comprobar_si_solo_hay_numeros(ccv):
        respuesta['resultado'] = "invalid_ccv"
    elif comprobar_si_hay_digitos(propietario) or '@' in propietario or '!' in propietario or '"' in propietario or '#' in propietario or '%' in propietario or '&' in propietario or '/' in propietario or '(' in propietario or ')' in propietario or '=' in propietario or '?' in propietario or '¿' in propietario or '|' in propietario or '°' in propietario or '¬' in propietario or '´' in propietario or '¨' in propietario or '+' in propietario or '*' in propietario or '{' in propietario or '}' in propietario or '[' in propietario or ']' in propietario or '`' in propietario or '^' in propietario or '~' in propietario or ',' in propietario or ';' in propietario or '.' in propietario or ':' in propietario or '-' in propietario or '_' in propietario or '¡' in propietario or propietario == "":
        respuesta['resultado'] = "invalid_user"
    else:
        respuesta['resultado'] = "success"

    return jsonify(respuesta)

    
    
    
       
    
      
    
    

    



@app.route('/comprobar-tarjeta-android', methods=['GET'])
def comprobar_tarjeta2():
    respuesta = ""
    dicc_respuesta = request.args
    parte1 = dicc_respuesta['parte1']
    parte2 = dicc_respuesta['parte2']
    parte3 = dicc_respuesta['parte3']
    ccv = dicc_respuesta['cvv']
    propietario = dicc_respuesta['titular'].upper()
    id = dicc_respuesta['id']


    print(parte1,"\n",dicc_respuesta)    
    
    if len(parte1) != 4 or len(parte2) != 4 or len(parte3) != 4 or not comprobar_si_solo_hay_numeros(parte1+parte2+parte3):
        respuesta= "resultado:invalid_card_number"
    elif len(ccv) != 3 or not comprobar_si_solo_hay_numeros(ccv):
        respuesta = "resultado:invalid_ccv"
    elif comprobar_si_hay_digitos(propietario) or '@' in propietario or '!' in propietario or '"' in propietario or '#' in propietario or '%' in propietario or '&' in propietario or '/' in propietario or '(' in propietario or ')' in propietario or '=' in propietario or '?' in propietario or '¿' in propietario or '|' in propietario or '°' in propietario or '¬' in propietario or '´' in propietario or '¨' in propietario or '+' in propietario or '*' in propietario or '{' in propietario or '}' in propietario or '[' in propietario or ']' in propietario or '`' in propietario or '^' in propietario or '~' in propietario or ',' in propietario or ';' in propietario or '.' in propietario or ':' in propietario or '-' in propietario or '_' in propietario or '¡' in propietario or propietario == "":
        respuesta= "resultado:invalid_user"
    else:
        n_tarjeta = parte1+parte2+parte3
        t = Tarjeta(n_tarjeta=(n_tarjeta), ccv=ccv, titular=propietario, id_usuario=id)
        db.session.add(t)
        db.session.commit()

        respuesta = "resultado:success"

    return respuesta
    
    
    
    

    

@app.route("/create_credit_card", methods=['POST'])
def create_credit_card():
    print("skdfñj")
    dicc = request.get_json()
    n_tarjeta = dicc['parte1']+dicc['parte2']+dicc['parte3']
    ccv = int(dicc['ccv'])
    titular = dicc['titular'].upper()
    id = dicc['id']
    t = Tarjeta(n_tarjeta=(n_tarjeta), ccv=ccv, titular=titular, id_usuario=id)
    db.session.add(t)
    db.session.commit()
    print("hoal")

    return jsonify({})


@app.route('/monto', methods=['POST'])
def montos():
    response = {}
    print("esto es una prueba")

    monto = request.get_json()['monto']
    id_persona = request.get_json()['id_persona']
    usuario = Usuario.query.get(id_persona)
    porcentaje = request.get_json()['porcentaje']
    id_partido = request.get_json()['id_partido']

    if monto == " " or not comprobar_si_solo_hay_numeros2(monto) or monto=="-":
        response['resultado'] = "incorrect_input"

    elif monto == "":
        response['resultado'] = "null_bet"
    elif float(monto) < 0:
        response['resultado'] = "negative_bet"
    elif usuario.dinero_en_cuenta < float(monto):
        response['resultado'] = "insufficient_funds"
    else:
        response['resultado'] = "success"
        monto_total = float(porcentaje) * float(monto)
        print(monto_total, porcentaje)
        usuario.dinero_en_cuenta -= float(monto)
        apuesta = Apuestas(monto=monto_total,
                           id_partido=id_partido, id_usuario=id_persona)
        db.session.add(apuesta)
        db.session.commit()

    return jsonify(response)


@app.route('/monto2', methods=['GET'])
def montos2():
    response = {}
    print("esto es una prueba")
    print(request.args)

    monto = request.args['monto']
    id_persona = request.args['id_persona']
    usuario = Usuario.query.get(id_persona)
    porcentaje = request.args['porcentaje']
    id_partido = request.args['id_partido']

    if monto == " " or not comprobar_si_solo_hay_numeros2(monto) or monto == "-":
        response= "resultado:incorrect_input"

    elif monto == "":
        response= "resultado:null_bet"
    elif float(monto) < 0:
        response= "resultado:negative_bet"
    elif usuario.dinero_en_cuenta < float(monto):
        response= "resultado:insufficient_funds"
    else:
        response= "resultado:success"
        monto_total = float(porcentaje) * float(monto)
        print(monto_total, porcentaje)
        usuario.dinero_en_cuenta -= float(monto)
        apuesta = Apuestas(monto=monto_total,
                           id_partido=id_partido, id_usuario=id_persona)
        db.session.add(apuesta)
        db.session.commit()

    return response



@app.route('/agregar_dinero', methods=['POST'])
def agregar_dinero():
    response = {}

    dicc = request.get_json()
    print(dicc)
    dinero_agregado = dicc['dinero_agregado']
    print(dinero_agregado)
    u = Usuario.query.get(dicc['id'])

    if dinero_agregado == " " or not comprobar_si_solo_hay_numeros2(dinero_agregado):
        response['resultado'] = "incorrect_input"

    elif dinero_agregado == "":
        response['resultado'] = "null_deposit"
    elif float(dinero_agregado) < 0:
        response['resultado'] = "negative_deposit"

    else:
        response['resultado'] = "success"
        u.dinero_en_cuenta += float(dinero_agregado)

        db.session.commit()

    return jsonify(response)

@app.route('/agregar-dinero-android', methods=['GET'])
def agregar_dinero_android():
    response = ""

    dicc = request.args
    print(dicc)
    dinero_agregado = dicc['money']
    print(dinero_agregado)
    u = Usuario.query.get(dicc['id'])

    if dinero_agregado == " " or not comprobar_si_solo_hay_numeros2(dinero_agregado) or dinero_agregado=="-":
        response = "incorrect_input"

    elif dinero_agregado == "":
        response= "null_deposit"
    elif float(dinero_agregado) < 0:
        response= "negative_deposit"

    else:
        response= "success"
        u.dinero_en_cuenta += float(dinero_agregado)

        db.session.commit()

    return response




@app.route('/register')
def register():

    return render_template('register.html')


@app.route('/')
def index():

    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="192.168.1.34", port=5002,debug=True)
else:
    print('using global variables from FLASK')
