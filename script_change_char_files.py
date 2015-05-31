from subprocess import call
import os

changes = [
        ('camacho','toro'),
        ('dj','dayamar'),
        ('ernesto','alejandra'),
        ('fernando','eduardo'),
        ('mantellini','ochoa'),
        ('porras','perozo'),
        ('leila','jeanmar'),
        ('veronica','cristina'),
        ('natasha','josefina'),
        ('paul','enrique'),
        ('ronald','francisco'),
        ('raj','daniel'),
        ('ja','adrian'),
        ('shalahb','joel'),
        ('campuzano','cordero'),
        ('abejon','alvarado'),
        ]

for item in changes:
    os.system('find . -name *.csv | xargs sed -i "s/%s/%s/g"' % (item[0],item[1]))
    os.system('find . -name *.csv | xargs sed -i "s/%s/%s/g"' % (item[0].capitalize(),item[1].capitalize()))
