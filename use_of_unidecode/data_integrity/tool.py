from data_integrity import * 

def main():
    print ' --- The script is running, wait a minute.'
    oerp_obj = server_config()
    oerp_obj.login_db()
    csv_list = read_config_file()
    for csv_file in csv_list:
        print ' --- Checking the \'%s\' file' % (csv_file,)
        csv_lines = read_csv_file(csv_file)   # [(xml_id, model)]
        imd_ids = check_loaded_data(oerp_obj, csv_lines)
        check_data_remains(oerp_obj, imd_ids)
    print ' --- Finish script. All the initial data is correct.'

main()
