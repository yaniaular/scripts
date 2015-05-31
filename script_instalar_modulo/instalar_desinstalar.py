import oerplib

user = 'admin' #admin
passwd = 'admin' #admin
port = 10000 #8069
name_db = 'cicsa'
module = 'cicsa_bdp_data'

oerp = oerplib.OERP(server='localhost',protocol='xmlrpc',port=port)
oerp.login(user, passwd, database=name_db)
module_obj = oerp.get('ir.module.module')
module_id = module_obj.search([('name', '=', module)])

band = True
while(band):
    resp = raw_input('Instalar modulo %s, Desinstalar modulo %s o Salir? i/d/s:'%(module,module))
    if resp == 'd':
        module_obj.button_immediate_uninstall(module_id)
    elif resp == 'i':
        module_obj.button_immediate_install(module_id)
    else:
        band = False
