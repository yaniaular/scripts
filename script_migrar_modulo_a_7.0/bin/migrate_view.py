#!/bin/python
from xml.etree import ElementTree
from lxml import etree

class migrate_view():
    '''
    Migrate architecture view to use it in the verision 7 
    '''

    def __init__(self, l_file=None):
        '''
        Maiker to init path with the xml files
        @param l_file List with xml file path
        '''

        self.files = l_file and type(l_file) is list and l_file or l_file \
                                                                   and [l_file]
    def change_xpath(self, xml_f):
        '''
        Change the path from xpath using the relative rute 
        @param xml_f Type Object xpath from lxml.tree library
        '''
        xpath_list =  xml_f.xpath('//xpath')
        if xpath_list: 
            for xpaths in xpath_list:
                expr = xpaths.attrib.get('expr', False)
                if expr:
                    m = '//' in expr and expr or  expr.split('/') and \
                                                   '//%s' % expr.split('/')[-1]
                    xpaths.set('expxml_f',m)

        return True

    def remove_depreciated(self, xml_o):
        '''
        Remove depreceated methos in the architecture view
        @param xml_o Type Object xpath from lxml.tree library

        '''
        types =  xml_o.xpath('//field[@name="type"]')
        if types: 
            for line in types:
                parent = line.getparent()
                parent.remove(line)

        return True

    def version_7(self, xml_o):
        '''
        Add Version 7 in tags form 
        @param xml_o Type Object xpath from lxml.tree library

        '''
        x =  xml_o.xpath('//form')
        if x: 
            for i in x:
                i.set('version','7.0')

        return True

    def modify_arch(self, l_files,types='a'):
        '''
        Modifie architecture view to use in openerp V7
        Remove depreciate values and add version description view
        @param l_files List with file path xml
        @param types Type change
               'a' Change all include xpath rute with relative way
               't' Basicaly change to work with V7 standard
               'x' Only change xpath route to use the realative way
        '''
        l_files = self.files or l_files and type(l_files) is list or \
                                        l_files and [l_files]

        for files in l_files:

            filex = open(files)
            tree = etree.parse(filex)
            read = tree.xpath('//record[@model="ir.ui.view"]')
            for line in read:
                inherit = types in ('a','x') and \
                                      line.xpath('//field[@name="inherit_id"]')

                inherit and line.xpath('//xpath') and self.change_xpath(line)

                line.xpath('//field[@name="type"]') and \
                                                  self.remove_depreciated(line)
                line.xpath('//form') and self.version_7(line)

            out = open('%s' % files, 'w')
            tree.write(out)
            out.close()

            return True
