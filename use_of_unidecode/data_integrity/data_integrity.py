import oerplib
import libxml2
import csv

class server_config(object):
    
    """
    This Objects save the server configuration 
    - XMLRPC server configuration.
    - Data base configuration.
    """

    def __init__(self):
        self.server = 'localhost'
        self.protocol = 'xmlrpc'
        self.port = 8069
        self.database = 'edima'
        self.user = 'admin'
        self.password = 'admin'

    def login_db(self):
        """
        This method create a oerplib object and login into to data base.
        @return the data base handle.
        """
        oerp = oerplib.OERP(
                server=self.server,
                database=self.database,
                protocol=self.protocol,
                port=self.port,
                )
        oerp.login(self.user, self.password)
        self.handle = oerp

def read_csv_file(cvs_name):

    """
    This method read the data of a csv file.
    """
    lines = list()
    csv_lines = csv.DictReader(open(cvs_name))
    for line in csv_lines:
        # ditionary with the {field name: field value,}
        lines += [(line.pop('id'), line.pop('model'))]
    return lines[1:]

def check_loaded_data(oerp_obj, csv_lines):
    """
    This method check in all the xml ids in the cvs files are loaded into
    the xml id in the openerp data base in table ir.model.data
        @param csv_lines: list of [ (xml_id, model), ... ]  
        @return: list of ir.model.data ids corresponding to the given cvs.
    """
    imd_ids = list()
    #'ir.model.data' model: (id, name, module, model, res_id)
    for line in csv_lines:
        record_xml_id = line[0].split('.')[-1]
        imd_id = oerp_obj.handle.search(
                'ir.model.data',
                [('model', '=', line[1]), ('name', '=', record_xml_id)])
        assert imd_id, ('This is and error. The record ( model %s, xml_id %s)'
        'was not loaded' % (line[1], line[0]))
        imd_ids += imd_id
    return imd_ids

def check_data_remains(oerp_obj, imd_ids):

    """
    This method takes the imd_ids and checks if the initial loaded records
    wee deleted or still remains in openerp.
        @param oerp_obj: the openerp handler.
        @param imd_ids: list of xml ids loaded in openerp.
        @return: always True

        note: it raise and assert if some record have been deleted.
    """
    for imd_id in imd_ids:
        imd_brw = oerp_obj.handle.browse('ir.model.data', imd_id)
        assert oerp_obj.handle.execute(
            imd_brw.model, 'exists', imd_brw.res_id), (
                'There is an integrity error. A Data record have been deleted.')
    return True

def read_config_file():

    """
    This method read the config file and returns the csv file names list to
    check.
        @return: a list of cvs file names to be checked.
    """
    print ' --- read config file.'
    f = open('config', 'r')
    csv_list = f.read().splitlines()
    f.close()
    print csv_list
    return csv_list
