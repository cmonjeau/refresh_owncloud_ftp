#!/usr/bin/env python

import os, json, re

def main():


    #get mounts info
    os.system('sudo -u apache php /var/www/html/owncloud/occ files_external:list -a --output json > /tmp/owncloud_mounts.json')

    # parse json
    with open('/tmp/owncloud_mounts.json') as data_file:    
        data = json.load(data_file)

   
    # for each mounts
    for mount in data:
        if mount['storage'] == '\\OCA\\Files_External\\Lib\\Storage\\FTP':
            user = mount['configuration']['user']
            storage_name = re.escape(mount['mount_point'])

            mess = "Refresh mount %s for user %s\n" % (storage_name, user)

            with open('/var/log/refresh_FTP.log', 'aw') as f:
                f.write(mess)

            os.system('sudo -u apache php /var/www/html/owncloud/occ files:scan --path %s/files/%s >> /var/log/refresh_FTP.log' % (user, storage_name))


    # remove tmp file
    os.remove('/tmp/owncloud_mounts.json')    

if __name__ == '__main__':
    main()
