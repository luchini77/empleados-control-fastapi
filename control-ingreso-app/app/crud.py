from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from .database import get_session
from .schemas import Empleado, EmpleadoCrear, EmpleadoActualizar
from .models import Empleado as EmpleadoModels


def fecha_actual():
    fecha = datetime.today()
    date = fecha.strftime("%d/%m/%Y")
    return date
    

def hora_actual():
    hora = datetime.now()
    time = hora.strftime("%H:%M:%S")
    return time


def get_empleados(db:Session=Depends(get_session)):
    empleados = db.query(EmpleadoModels).all()
    return empleados


def create_empleado(empleado:EmpleadoCrear,db:Session=Depends(get_session)):
    empleado = empleado.dict()

    new_empleado = EmpleadoModels(**empleado)
    # new_empleado = EmpleadoModels(
    #     nombre = empleado['nombre'],
    #     apellidos = empleado['apellidos'],
    #     rut = empleado['rut'],
    #     email = empleado['email']
    #     cargo = empleado['cargo'],
    #     empresa = empleado['empresa'],
    #     fecha = empleado['fecha'],
    #     hora = empleado['hora'],
    #     registrado = empleado['registrado'],
    # )

    db.add(new_empleado)
    db.commit()
    db.refresh(new_empleado)
    return new_empleado


def get_by_id(id:int,db:Session=Depends(get_session)):
    empleado = db.query(EmpleadoModels).filter(EmpleadoModels.id == id).first()

    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No se encuentra empleado con ese id: {id}')
    return empleado


def get_by_rut(rut:str,db:Session=Depends(get_session)):
    activo = db.query(EmpleadoModels).filter(EmpleadoModels.rut == rut).first()

    if not activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No se encuentra empleado con ese rut: {rut}')

    if activo.registrado == False:
        activo.registrado = True
    else:
        activo.registrado = False

    activo.fecha = fecha_actual()
    activo.hora = hora_actual()

    db.add(activo)
    db.commit()
    return activo

def get_by_registrado(db:Session=Depends(get_session)):
    empleados = db.query(EmpleadoModels).filter(EmpleadoModels.registrado == True).all()    
    return empleados


def update_empleado(id:int,empleado:EmpleadoActualizar,db:Session=Depends(get_session)):

    empleado_update = db.query(EmpleadoModels).filter(EmpleadoModels.id == id)
    if not empleado_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No se encuentra empleado con ese id: {id}')
    
    empleado_data = empleado.dict(exclude_unset=True)

    for key,value in empleado_data.items():
        setattr(empleado_update,key,value)

    db.add(empleado_update)
    db.commit()
    db.refresh(empleado_update)
    return empleado_update


def delete_empleado(id:int,db:Session=Depends(get_session)):
    empleado = db.query(EmpleadoModels).filter(EmpleadoModels.id == id)

    if empleado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No se encuentra empleado con ese id: {id}')
    
    db.delete(empleado)
    db.commit()
    return {"Empleado borrado": True}