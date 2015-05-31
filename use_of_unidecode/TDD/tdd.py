# -*- coding: utf-8 -*-
import oerplib
import os
import re

oerp = oerplib.OERP(port=8069)#
oerp.config['timeout']=4000
db_name = "edima"
proyecto = "EDIMA"

band = True

def _get_image( name):
    fil = open(name, 'rb')
    data = fil.read()
    fil.close()
    binary = data.encode('base64')
    return binary 

while(band):
    os.system('clear')
    resp = raw_input('Proyecto %s\n1. Borrar y Crear BD nueva\n2. Cargar data o realizar procesos \
desde webservice \n3. Instalar o desinstalar modulo\n4. Convertir imagen a \
formato binario\nS. Salir\n' % proyecto)

    if resp == '1':
        
        modules = [
                'stock',
                'stock_location',
                ]
        print "\n****Borrar la base de datos %s y crearla nuevamente.****\n" % db_name
        demo = raw_input("Con demo data escribir 'Si', sin demo data escribe cualquier cosa: ")

        if demo.lower() == 'si':
            demo_data = True
        else:
            demo_data = False

        print 'BORRANDO BASE DE DATOS VIEJA'
        oerp.db.drop('admin', db_name)
        
        print 'CREATING A NEW DATABASE'
        oerp.db.create_and_wait('admin', db_name, demo_data)
        oerp.login(database=db_name)
        
        print 'INSTALANDO MODULOS'
        module_obj = oerp.get('ir.module.module')

        for mod in modules:
            module_id = module_obj.search([('name', '=', mod)])
            module_obj.button_immediate_install(module_id)

        print 'ESTABLECIENDO PERMISOS TECNICOS'
        res_users_obj = oerp.get('res.users')
        user_id = res_users_obj.search([('login', '=', 'admin')])  
        user = res_users_obj.browse( user_id[0] )
        user.groups_id += [6]
        oerp.write_record(user)
        print 'READY TO USE'
        raw_input('Enter para continuar...')
    elif resp == '2':
        print "\n****Cargar data o realizar procesos desde el webservice****\n"
        oerp.login(database=db_name)
        #Cargar datos aqui
        raw_input('Enter para continuar...')
    elif resp == '3':
        print "\n****Instalar o desinstalar un módulo de la base de datos****\n"
        oerp.login(database=db_name)
        module = raw_input('Nombre del modulo: ')
        module_obj = oerp.get('ir.module.module')
        module_id = module_obj.search([('name', '=', module)])

        if module_id:
            resp = raw_input('Instalar modulo %s escribir "i", Desinstalar modulo %s escribir "d"\
, ENTER para salir:'%(module,module))
            if resp.lower() == 'd':
                module_obj.button_immediate_uninstall(module_id)
                print "Modulo %s desinstalado..." % module
            elif resp.lower() == 'i':
                module_obj.button_immediate_install(module_id)
                print "Modulo %s instalado..." % module
        else:
            print "\n***El modulo %s no existe***\n" % module
        raw_input('Enter para continuar...')
    elif resp == '4':
        print "\n****Escribir la ruta de la imagen para poder crear un txt****\n"
        img = raw_input('Nombre la imagen: ')
        img_b = _get_image(img)
        fl = open('%s.txt' % img, 'w')
        und = re.compile('\n')
        img_b = und.sub('', img_b)
        fl.write(img_b)
        fl.close()
        print "Se creo el archivo %s.txt con el binario de la imagen %s..." % (img,img)
        raw_input('Enter para continuar...')
    elif resp.lower() == 's':
        band = False




