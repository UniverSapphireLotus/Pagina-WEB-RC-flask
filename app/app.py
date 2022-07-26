from contextlib import redirect_stderr
from urllib import request
from clases.pedido import Pedido
from clases.producto import Producto
from clases.detallePedido import DetallePedido
from clases.user import Usuario
from flask import  Flask, render_template, jsonify, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy import create_engine
import urllib
import pyodbc
from clases import producto
from clases import pedido
app= Flask(__name__)

#engine= sa.create_engine('mssql+pyodbc://user:password@server/database')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
carrito= []
carrito.clear()

login=False
admin=True
idUsuario=0

userLog= Usuario(0, 0, 0, 0)

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=DESKTOP-GATG0PQ\SAKINIKAIDO;"
                                 "DATABASE=DB_RECREO_WEB;"
                                 "UID=sa;"
                                 "PWD=saki")

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


@app.route('/')
def index():
    return render_template('index.html',  carrito= carrito, carrito_size= len(carrito), totalCompra= totalCarrtio(), log= login, admin=admin)

@app.route('/login.html/')
def login():
    return render_template('login.html',  carrito= carrito, carrito_size= len(carrito), totalCompra= totalCarrtio(), log= login, admin=admin)


@app.route('/nuestra-carta.html/')
def carta():
    menu={} 
    try:
        sql="select IdProducto, NombreProducto, DescripcionProducto, PrecioProducto, CategoriaProducto, ImagenProducto, FechaRegistroProducto from Producto;"
        result= engine.execute(sql)
        print(result)
        data_menu=[]
        for row in result:
            data_menu.append(Producto(row['IdProducto'], row['NombreProducto'], 
            row['DescripcionProducto'], row['PrecioProducto'], row['CategoriaProducto'], 
            row['ImagenProducto'], row['FechaRegistroProducto']))

        for r in data_menu:
            print(r)
        menu['mensaje']= 'Existo!!!'
    except Exception as ex:
        print('Error ...')
        menu['mensaje']= 'Error ...'
    return render_template('nuestra-carta.html', result= data_menu, carrito= carrito, carrito_size= len(carrito), totalCompra= totalCarrtio(), log= login, admin=admin)



@app.route('/menu/')
def menu():
    menu={} 
    try:
        sql="select IdProducto, NombreProducto, DescripcionProducto, PrecioProducto, CategoriaProducto, ImagenProducto, FechaRegistroProducto from Producto;"
        result= engine.engine.execute(sql)
        print(result)
        names = [row[1] for row in result]
        result= result.fetchall()
        menu['platillos']= result
        menu['mensaje']= 'Existo!!!'
        print(names)
    except Exception as ex:
        print('Error ...')
        menu['mensaje']= 'Error ...'
    return jsonify(menu)



@app.route('/nosotros.html/')
def nosotros():
    return render_template('nosotros.html',  carrito= carrito, carrito_size= len(carrito), totalCompra= totalCarrtio(), log= login, admin=admin)

@app.route('/shop-cart.html/')
def shopping():
    return render_template('shop-cart.html',  carrito= carrito, carrito_size= len(carrito), totalCompra= totalCarrtio(), log= login, admin=admin)
    #return redirect(url_for('nosotros'))

@app.route('/add', methods= ['POST'])
def add_producto_carrtio():
    _idProducto= request.form['idProducto']
    print(_idProducto)
    print("aaa")
    if request.method == 'POST':
        print("ooooooooooo") 
        #row= result.fetchone()
        #data_menu = { row['IdProducto'] : {'IdProducto' : row['IdProducto'], 'NombreProducto' : row['NombreProducto'], 'DescripcionProducto' : row['DescripcionProducto'], 'PrecioProducto' : row['PrecioProducto'], 'CategoriaProducto' : row['CategoriaProducto'], 'Cantidad':1, 'Total': row['PrecioProducto']}}
        data_menu=[]
        estado=True
        for sc in carrito:
            print("pppppp", sc.IdProducto)
            if sc.IdProducto ==int(_idProducto):
                estado= False
                sc.cantidad+=1
                break
        if estado:
            sql="select IdProducto, NombreProducto, DescripcionProducto, PrecioProducto, CategoriaProducto, ImagenProducto, FechaRegistroProducto from Producto Where IdProducto=" +_idProducto+";"
            result= engine.execute(sql)
            print(sql)
            for row in result:
                carrito.append(Producto(row['IdProducto'], row['NombreProducto'], 
                row['DescripcionProducto'], row['PrecioProducto'], row['CategoriaProducto'], 
                row['ImagenProducto'], row['FechaRegistroProducto']))
            print("[[[[[[[[[", carrito)
        for sc in carrito:
            print(">>>>>", sc)
        

    return redirect(url_for('carta'))

@app.route('/registrarse', methods= ['POST'])
def add_usuario():
    print("== ")
    if request.method == 'POST':
        _nombreUsuario= request.form['nombreUsuario']
        _email= request.form['email']
        _password= request.form['password']
        _password_2= request.form['password_2']
        print(_password, "--", _password_2)

        if _password==_password_2:
            sql= "insert into Usuario(NombreUsuario, EmailUsuario, ContraseñaUsuario) values('"+ _nombreUsuario+"', '"+ _email+"', '"+ _password+"');"
            result= engine.execute(sql)
            print("registarrrrrrrrrr")
            #flash("glorioso, usuario registrado")
    return redirect(url_for('login'))

@app.route('/ingresar', methods= ['POST'])
def verificar_usuario():
    print("== ")
    if request.method == 'POST':
        _email= request.form['email']
        _password= request.form['password']
        print(_email, "--", _password)
        sql="select idUsuario, NombreUsuario,ContraseñaUsuario, EmailUsuario from Usuario where ContraseñaUsuario ="+ _email +"and EmailUsuario= " +_password+" ;"
        result= engine.execute(sql)
        for row in result:
            Usuario=(row['idUsuario'], row['NombreUsuario'], row['ContraseñaUsuario'], row['EmailUsuario'])


        if _password==passs:
            print("ingresar")
            #flash("glorioso, usuario registrado")
    return redirect(url_for('index'))

@app.route('/pagar')
def pagar_cuenta():
    print("== ")
    if len(carrito)>0:
        _IdUsuario= 1
        sql="INSERT INTO Pedido (IdUsuario, FechaPedido,EstadoPedido) values ("+str(_IdUsuario)+ ", CURRENT_TIMESTAMP, 1);"
        for i in carrito:
            sql+= "INSERT INTO DetallePedido(IdPedido, IdProducto, CantidadProducto, TotalPrecio, Descuento) values (IDENT_CURRENT('Pedido'),"+str(i.IdProducto)+","+str(i.cantidad)+" ,"+str(i.PrecioProducto* i.cantidad)+",0);"
        print(sql)
        result= engine.execute(sql)

        if result:
            carrito.clear()
            #flash("glorioso, usuario registrado")
    return redirect(url_for('shopping'))


@app.route('/ADMIN/agregarPlatillo.html/')
def menuInsertarPlatillo():
    return render_template('/ADMIN/agregarPlatillo.html')


@app.route('/insertarProducto', methods= ['POST'])
def agregarPlatillo():
    connection = engine.connect()
    consult = connection.begin()
    if request.method == 'POST':
        print("==☺o☺♂☺♂o==")
        _nombrePlatillo= request.form['nombrePlatillo']
        _descripcionProducto= request.form['descripcionProducto']
        _precioProducto= request.form['precioProducto']
        _categoriaProducto= request.form['categoriaProducto']
        print('.◘◘', _categoriaProducto)
        sql="INSERT INTO Producto(NombreProducto, DescripcionProducto,PrecioProducto, CategoriaProducto, ImagenProducto, FechaRegistroProducto) SELECT '"+_nombrePlatillo+"', '"+_descripcionProducto+"', "+str(_precioProducto)+", '"+_categoriaProducto+"', BulkColumn, '2008-11-11'  FROM Openrowset( Bulk 'C://Users//Dark Wizard//Desktop//opencv//PYTHON FLASKy//Pagina-WEB-RC-flask//app//static//images//kobeni-logo.png', Single_Blob) as Imagen; "
        print(sql)
        connection.execute(sql)
        consult.commit()
        
        
            #flash("glorioso, usuario registrado")
    return redirect(url_for('menuInsertarPlatillo'))

@app.route('/ADMIN/gestionCarta.html/')
def gestionCarta():
    menu={} 
    try:
        sql="select IdProducto, NombreProducto, DescripcionProducto, PrecioProducto, CategoriaProducto, ImagenProducto, FechaRegistroProducto from Producto;"
        result= engine.execute(sql)
        print(result)
        data_menu=[]
        for row in result:
            data_menu.append(Producto(row['IdProducto'], row['NombreProducto'], 
            row['DescripcionProducto'], row['PrecioProducto'], row['CategoriaProducto'], 
            row['ImagenProducto'], row['FechaRegistroProducto']))

        for r in data_menu:
            print(r)
        menu['mensaje']= 'Existo!!!'
    except Exception as ex:
        print('Error ...')
        menu['mensaje']= 'Error ...'
    return render_template('/ADMIN/gestionCarta.html', result= data_menu)

@app.route('/ADMIN/listaPedidos.html/')
def listaPedidos():
    pedidos={} 
    print('listaPedidos')
    try:
        sql="SELECT DetallePedido.IdPedido, Usuario.NombreUsuario, DetallePedido.CantidadProducto, DetallePedido.TotalPrecio, Pedido.FechaPedido, Pedido.EstadoPedido  FROM Usuario INNER JOIN Pedido ON Usuario.IdUsuario = Pedido.IdUsuario INNER JOIN DetallePedido ON Pedido.IdPedido = DetallePedido.IdPedido"
        result= engine.execute(sql)
        
        data_pedido=[]
        for row in result:
            print("mediccccccccc")
            data_pedido.append(Pedido(row['IdPedido'], row['NombreUsuario'], row['CantidadProducto'], 
            row['TotalPrecio'], row['FechaPedido'], row['EstadoPedido']))

        for r in data_pedido:
            print(r)
        pedidos['mensaje']= 'Existo!!!'
    except Exception as ex:
        print('Error ...')
        pedidos['mensaje']= 'Error ...'

    return render_template('/ADMIN/listaPedidos.html', data_pedido= data_pedido)


@app.route('/verDetallePedido', methods= ['POST'])
def verDetallePedido():
    pedidos={} 
    IdPedido=request.form['IdPedido']
    print('listaPedidos ', IdPedido)
    try:
        sql="DECLARE @Pedido INT SET @Pedido = {} SELECT DetallePedido.CantidadProducto, Producto.NombreProducto, Producto.PrecioProducto,  (DetallePedido.CantidadProducto*Producto.PrecioProducto) AS TotalPorPlatillo FROM DetallePedido INNER JOIN Producto ON DetallePedido.IdProducto = Producto.IdProducto WHERE DetallePedido.IdPedido = @Pedido".format(IdPedido)
        result= engine.execute(sql)
        
        data_detallePedido=[]
        for row in result:
            print("mediccccccccc")
            data_detallePedido.append(DetallePedido(row['CantidadProducto'], row['NombreProducto'], row['PrecioProducto'], 
            row['TotalPorPlatillo']))

        for r in data_detallePedido:
            print(r)
        pedidos['mensaje']= 'Existo!!!'
    except Exception as ex:
        print('Error ...')
        pedidos['mensaje']= 'Error ...'

    return render_template('/ADMIN/detallePedido.html', data_detallePedido= data_detallePedido)

def totalCarrtio():
    total= 0
    for i in carrito:
        total+=i.PrecioProducto* i.cantidad
    return total


if __name__== '__main__':
    app.run(port= 3333, debug= True)

