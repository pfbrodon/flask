from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemyb ,cvgb                                    
ma= Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino las tabla de Productos
class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    cantidad=db.Column(db.Integer)
    categoria=db.Column(db.String(50))
    codigo=db.Column(db.Integer)
    descripcion=db.Column(db.String(50))
    precioUnit=db.Column(db.Integer)
    precioVPublico=db.Column(db.Integer)
    
    def __init__(self,cantidad,categoria,codigo,descripcion,precioUnit,precioVPublico):   #crea el  constructor de la clase
        self.cantidad=cantidad  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.categoria=categoria
        self.codigo=codigo
        self.descripcion=descripcion
        self.precioUnit=precioUnit
        self.precioVPublico=precioVPublico
        
#Defino la tabla de Usuarios
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    nombre=db.Column(db.String(45), nullable=False)
    tipouser=db.Column(db.String(14), nullable=False)
    
    def __init__(self,email,password,nombre,tipouser):   #crea el  constructor de la clase
        self.email=email  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.password=password
        self.nombre=nombre
        self.tipouser=tipouser





class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','cantidad','categoria','codigo','descripcion','precioUnit','precioVPublico')


producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto



@app.route('/')
def index():
    return 'Hola Pablo'

@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
    jsonresult= jsonify(result)                                            # trae todos los registros de la tabla
    #return jsonresult
    return render_template('productos.html', jsonresult=jsonresult )                      # retorna un JSON de todos los registros de la tabla


##############login#################################
@app.route('/login', methods=['POST', 'GET'])
def login():    
    email = request.form['email']
    password = request.form['password']
   # tipouser= request.form['tipouser']
   
    #usuario_autenticado = Login.query.filter_by(email=email).first()
    usuario_autenticado = Login.query.filter_by(email=email, password=password).first()

    if usuario_autenticado: # and check_password_hash(usuario_autenticado.password, password):
        print(usuario_autenticado.tipouser)
        
        # Autenticación exitosa
        if usuario_autenticado.tipouser=='admin':
            return render_template('prueba.html', email=usuario_autenticado.nombre, producto=producto_schema)
        else:
            return render_template('cliente.html', email=usuario_autenticado.nombre, productos=ProductoSchema)

    else:
        # Credenciales incorrectas
        return render_template('index.html', mensaje="Usuario Incorrecto")




if __name__=='__main__':
    app.run(debug=True)