# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from admin.py")
@auth.requires_membership('Administrador')
def ingresoalumno():
    name = request.vars.get('name')
    fecha = request.vars.get('nacimiento')
    direccion = request.vars.get('direccion')
    telefono = request.vars.get('telefono')
    encargado = request.vars.get('encargado')
    alumnoid = None
    if name:
            alumnoid = db.alumno.insert(nombre = name, fecha_nacimiento = fecha, direccion = direccion, telefono=telefono, nombre_encargado=encargado)
    return dict(alumnoid = alumnoid)
@auth.requires_membership('Administrador')
def Asignacion():
    gradoselec = request.vars.get('grado')
    seccionselec = request.vars.get('seccion')
    alumnoselec = request.vars.get('alumno')
    enviar = request.vars.get('Guardar')
    grado = db(db.seccionxgrado.idgrado == db.grado.id).select()
    seccion = db(db.seccionxgrado.idseccion == db.seccion.id).select(groupby=db.seccion.descripcion)
    existe = None
    idregistro = None
    if enviar:
        if gradoselec:
            existe = db((db.seccionxgrado.idgrado == gradoselec) & (db.seccionxgrado.idseccion == seccionselec)).select()
        for rows in existe:
            existeasig = db((db.asignacion.idalumno == alumnoselec)).select()
            if existeasig:
                for row in existeasig:
                    row.update_record(idalumno = alumnoselec, idgradoxseccion = rows.id)
            else:
                idregistro = db.asignacion.insert(idalumno = alumnoselec, idgradoxseccion = rows.id)
    return dict(grado = grado, seccion = seccion, idregistro = idregistro)
@auth.requires_membership('Catedratico')
def ingresonotas():
    alumno = request.vars.get('alumno')
    curso = request.vars.get('curso')
    nota = request.vars.get('nota')
    import datetime
    fechaingreso = datetime.datetime.now()
    idnota = None
    if nota:
        existe = db((db.calificacion.idalumno == alumno) & (db.calificacion.idcurso == curso)).select()
        if existe:
            for row in existe:
                row.update_record(descripcion = nota, idalumno = alumno, idcurso = curso, fechaingreso = fechaingreso)
        else:
            idnota = db.calificacion.insert(descripcion = nota, idalumno = alumno, idcurso = curso, fechaingreso = fechaingreso)
    return dict(idnota=idnota)
@auth.requires_membership('Catedratico')
def vernota():
    alumno = request.vars.get('alumno')
    Buscar = request.vars.get('Buscar')
    calificacion = db(db.calificacion.idalumno<0).select()
    if Buscar:
        calificacion = db((db.calificacion.idalumno == db.alumno.id) & (db.calificacion.idcurso == db.curso.id)).select()
    return dict(calificacion = calificacion)
@auth.requires_membership('Administrador')
def creargrado():
    grado = request.vars.get('grado')
    gradoid = None
    if grado:
            gradoid = db.grado.insert(descripcion = grado)
    return dict(gradoid = gradoid)
@auth.requires_membership('Administrador')
def crearseccion():
    seccion = request.vars.get('seccion')
    gradoid = None
    if seccion:
            gradoid = db.seccion.insert(descripcion = seccion)
    return dict(gradoid = gradoid)
@auth.requires_membership('Administrador')
def asignarsecgrad():
    grados = request.vars.get('grados')
    seccion = request.vars.get('seccion')
    gradoid = None
    if grados:
            gradoid = db.seccionxgrado.insert(idgrado = grados, idseccion = seccion)
    return dict(gradoid = gradoid)
@auth.requires_membership('Administrador')
def crearcurso():
    curso = request.vars.get('curso')
    catedratico = request.vars.get('catedratico')
    rows = db((db.empleado.id > 0) & (db.empleado.idtipo == 1)).select()
    cursoid = None
    if curso:
        cursoid = db.curso.insert(descripcion = curso, idempleado = catedratico)
    return dict(rows = rows, cursoid = cursoid)
@auth.requires_membership('Administrador')
def crearempleado():
    nombre = request.vars.get('nombre')
    nacimiento = request.vars.get('nacimiento')
    identificacion = request.vars.get('identificacion')
    tipo = request.vars.get('tipo')
    empleadoid = None
    if nombre:
        empleadoid = db.empleado.insert(nombre = nombre, fechanacimiento = nacimiento, identificacion = identificacion, idtipo = tipo)
    return dict(empleadoid = empleadoid)
@auth.requires_membership('Catedratico')
def alumnoasignado():
    alumno=db(
            (db.asignacion.idalumno == db.alumno.id) &
            (db.asignacion.idgradoxseccion == db.seccionxgrado.id) &
            (db.seccionxgrado.idgrado == db.grado.id) &
            (db.seccionxgrado.idseccion == db.seccion.id)).select()
    return dict(alumno = alumno)
def crearhorario():
    return dict(message = "hola")
@auth.requires_membership('Administrador')
def cursoxgrado():
    grado = request.vars.get('grado')
    curso = request.vars.get('curso')
    enviar = request.vars.get('Guardar')
    gradoid = None
    idregistro = None
    if enviar != None:
        existe = db((db.cursoxgrado.idcurso == curso) & (db.cursoxgrado.idgrado == grado)).select()
        if existe:
            gradoid = "Curso ya fue asignado a este grado"
        else:
            idregistro = db.cursoxgrado.insert(idcurso = curso, idgrado = grado)
            gradoid = "Curso Asignado Exitosamente!"
    fields = [db.curso.descripcion, db.grado.descripcion]
    left = [db.cursoxgrado.on((db.cursoxgrado.idcurso==db.curso.id) & (db.cursoxgrado.idgrado==db.grado.id))]
    items = SQLFORM.grid(db.cursoxgrado, left=left, orderby=[db.grado.id], fields=fields, create=False, editable=False, details=False, showbuttontext=False, paginate=20)
    return dict(items = items, gradoid = gradoid)
@auth.requires_membership('Administrador')
def crearproducto():
    producto = request.vars.get('producto')
    cantidad = 0
    invid = None
    if producto:
        invid = db.suministro.insert(Descripcion = producto, cantidad = cantidad)
    return dict(invid = invid)
@auth.requires_membership('Administrador')
def salidainv():
    cantidad = request.vars.get('cantidad')
    suministro = request.vars.get('suministro')
    invid = None
    if cantidad:
        producto = db(db.suministro.id == suministro).select()
        for row in producto:
            cantidadbd = int(row.cantidad)
            cantidadus = int(cantidad)
            if cantidadbd < cantidadus:
                invid = "La cantidad ingresada es mayor a la existente.. Cantidad Existente: " + str(row.cantidad)
            else:
                cantidadnueva = cantidadbd - cantidadus
                script = row.update_record(cantidad = cantidadnueva)
                invid = "producto acutalizado exitosamente"
    return dict(invid = invid)
@auth.requires_membership('Administrador')
def ingresoinv():
    producto = request.vars.get('suministro')
    cantidad = request.vars.get('cantidad')
    cantidadprod = None
    invid = None
    if cantidad:
        cantidadprod = db(db.suministro.id == producto).select()
        for rows in cantidadprod:
            cantidadus = int(cantidad)
            cantidadingreso = cantidadus + int(rows.cantidad)
            rows.update_record(cantidad = cantidadingreso)
            invid = "Producto cargado correctamente"
    return dict(invid = invid)
