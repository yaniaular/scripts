# example: python busqueda.py /home/yanina/branches/instancias/7.0/addons/ "<\!--.*Start\ # Task.*-->"
import re 
import sys
import os

def body(name, exp):

    codigo = ' <!-- dfkgdsjgdklfjgskdgj\n --> aqui aqui <!-- alla alla -->'
    py = ' p = 5\np = p+ 2 #Suma\n #AQui se hace algo\n print p'

    comments = re.compile(r"<!--.*?-->", re.DOTALL)
    comments_py = re.compile(r"#.*?\n", re.DOTALL)

    #print re.sub(comments,'',codigo)
    #print re.sub(comments_py,'\n',py)


    if [o for o in exte if name.endswith(o)]:
        with open(name) as f1:
            data = f1.read()
            exec("match = re.findall(r'%s', data, re.DOTALL)" % exp)
            #match = re.findall(r'{.*hola.*}', data, re.DOTALL)
            if match:
                print name




if __name__ == '__main__':
    exte = ['md','py','xml','rst','js']
    if len(sys.argv) == 3:
        origin = sys.argv[1]
        if origin:
            if origin.startswith('/'):
                origin = origin
            else:
                origin = os.getcwd() + '/' + origin
            #print os.listdir(os.getcwd())

            archivos = [os.path.join(dp, f) for dp, dn, fn in \
                    os.walk(os.path.expanduser( origin  )) for f in fn\
                    if [o for o in exte if f.endswith(o)] ]

            for m in archivos:
                body( m, sys.argv[2])
