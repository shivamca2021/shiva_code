import ast
import sys
import git
import pwd
import grp
import os
import shutil
import stat
import zipfile
# from odoo.http import request


class ApiCaller:
    def __init__(self, method_to_call, **kwargs):
        self._method = getattr(self, method_to_call)
        self.args = kwargs

    def call_chown(self):
        uid = pwd.getpwnam(self.args.get('user_name')).pw_uid
        gid = grp.getgrnam(self.args.get('user_name')).gr_gid
        os.chown(self.args.get('path'), uid, gid)
        return self.args.get('path')

    def create_log_file(self):
        log_fir = '/home/{user_name}/log'.format(user_name=self.args.get('user_name'))
        os.mkdir(log_fir)
        shutil.chown(log_fir, self.args.get('user_name'), self.args.get('user_name'))
        log_file = '/home/{user_name}/log/{user_name}.log'.format(user_name=self.args.get('user_name'))
        with open(log_file, 'w') as f:
            pass
        shutil.chown(log_file, self.args.get('user_name'), self.args.get('user_name'))
        # os.chmod(log_file, stat.S_IRWXG)
        return log_file

    def create_config_file(self):
        config_path = '/etc/default/{user_name}.conf'.format(user_name=self.args.get('user_name'))
        # addons='addons,/home/{user_name}/odoo14.0/addons,/home/{user_name}/odoo14.0/odoo/addons,/home/{user_name}/ic-kpi-prism/community_addons/theme_clarico_vega-14.0.2.6.0,/home/{user_name}/ic-kpi-prism/community_addons,/home/{user_name}/ic-kpi-prism/ic_kpi_addons'.format(user_name=self.args.get('user_name'))
        # addons='/home/{user_name}/ic-kpi-prism/base_addons/odoo/addons,/home/{user_name}/ic-kpi-prism/base_addons/addons,/opt/odoo_14/addons,/home/{user_name}/ic-kpi-prism/community_addons/theme_clarico_vega-14.0.2.6.0,/opt/odoo_14/custom_git/ic-kpi-prism/community_addons,/home/{user_name}/ic-kpi-prism/community_addons/,/home/{user_name}/ic-kpi-prism/ic_kpi_addons'.format(user_name=self.args.get('user_name'))
        addons='/home/{user_name}/ic-kpi-prism/base_addons/odoo/addons,/home/{user_name}/ic-kpi-prism/base_addons/addons,/home/{user_name}/ic-kpi-prism/community_addons/theme_clarico_vega-14.0.2.6.0,/home/{user_name}/ic-kpi-prism/community_addons/,/home/{user_name}/ic-kpi-prism/ic_kpi_addons/'.format(user_name=self.args.get('user_name'))
        with open(config_path, 'w') as f:
            f.write("[options] \n"
                    "; This is the password that allows database operations:\n"
                    "admin_passwd = admin@123 \n"
                    ";db_host = False \n"
                    ";db_port = 5432 \n"
                    "db_user = {db_user} \n"
                    "db_password = {db_user} \n"
                    "addons_path = {addons} \n"
                    "logfile = {log_file}\n"
                    "xmlrpc_port = {port}"
                    .format(db_user=self.args.get('user_name'),
                                                  log_file=self.args.get('log_file'),
                                                  port=self.args.get('port'),
                                                  addons=addons))

        shutil.chown(config_path, self.args.get('user_name'), self.args.get('user_name'))
        mode = os.stat(config_path).st_mode
        mode += stat.S_IXOTH
        os.chmod(config_path, 0o755)
        return config_path

    def create_access_log_file(self):
        access_log_file = '/var/log/nginx/{user_name}.access.log'.format(user_name=self.args.get('user_name'))
        with open(access_log_file, 'w') as f:
            pass
        shutil.chown(access_log_file, self.args.get('user_name'), self.args.get('user_name'))
        return access_log_file

    def create_error_log_file(self):
        error_log_file = '/var/log/nginx/{user_name}.error.log'.format(user_name=self.args.get('user_name'))
        with open(error_log_file, 'w') as f:
            pass
        shutil.chown(error_log_file, self.args.get('user_name'), self.args.get('user_name'))
        return error_log_file

    def create_nginx_file(self):
        upstreamuser = self.args.get('user_name')
        upstreamchat = self.args.get('user_name') + 'chat'
        proxyurlchat = 'http://' + self.args.get('user_name') + 'chat'
        proxyurl = 'http://' + self.args.get('user_name')
        domain = self.args.get('user_name') + '.ic-prism.com'
        access_log_path = self.args.get('access_log_file')
        error_log_path = self.args.get('error_log_file')
        port =self.args.get('port')
        chatport =str(int(self.args.get('port')) - 24)
        nginx_file = '/etc/nginx/sites-enabled/{user_name}_http.conf'.format(user_name=self.args.get('user_name'))
        query_string = ''
        query_string += "# dev server\n"
        query_string += "upstream "+upstreamuser+" {\n"
        query_string += "    server 127.0.0.1:"+port+";\n"
        query_string += "}\n"
        query_string += "upstream "+ upstreamchat+" {\n"
        query_string += "    server 127.0.0.1:"+chatport+";\n"
        query_string += "}\n"
        query_string += "\n"
        query_string += "# http -> https\n"
        query_string += " server {\n"
        query_string += "    listen 80;\n"
        query_string += "server_name " + domain+";\n"
        query_string += "if ($http_x_forwarded_proto = 'http') {\n"
        query_string += "return 301 https://$host$request_uri;\n"
        query_string += "}\n"
        query_string += "#   rewrite ^(.*) https://$host$1 permanent;\n"
        query_string += "\n"
        query_string += "# log\n"
        query_string += "access_log "+access_log_path+";\n"
        query_string += "error_log "+error_log_path+";\n"
        query_string += "\n"
        query_string += "# Redirect longpoll requests to odoo longpolling port\n"
        query_string += "location /longpolling {\n"
        query_string += "proxy_pass "+proxyurlchat+";\n"
        query_string += "}\n"
        query_string += "\n"
        query_string += "# Redirect requests to odoo backend server\n"
        query_string += "location / {\n"
        query_string += "#  proxy_redirect off;\n"
        query_string += "proxy_pass "+proxyurl+";\n"
        query_string += "}\n"
        query_string += "}"
        with open(nginx_file, 'w') as f:
            f.write(query_string)
        # shutil.chown(nginx_file, self.args.get('user_name'), self.args.get('user_name'))

        mode = os.stat(nginx_file).st_mode
        mode += stat.S_IXOTH
        os.chmod(nginx_file, 0o755)
        return nginx_file

    def create_server_file(self):
        server_file = '/usr/bin/{user_name}-server'.format(user_name=self.args.get('user_name'))
        with open(server_file, 'w') as f:
            f.write("#!/bin/bash\n"
                    "cd /home/{db_user}/odoo14.0\n"
                    "exec /usr/bin/python3 odoo-bin $@".format(db_user=self.args.get('user_name')))
        # shutil.chown(server_file, self.args.get('user_name'), self.args.get('user_name'))
        os.chmod(server_file, 0o755)
        return server_file

    def create_service_file(self):

        service_file = '/etc/systemd/system/{user_name}_odoo.service'.format(user_name=self.args.get('user_name'))
        with open(service_file, 'w') as f:
            f.write("[Unit]\n"
                    "Description={desc}\n"
                    "After=syslog.target\n"
                    "[Service]\n"
                    "User={user_name}\n"
                    "ExecStart={server} -c {config}\n"
                    "Restart=on-failure\n"
                    "RestartSec=5s\n"
                    "[Install]\n"
                    "WantedBy=multi-user.target".format(desc=self.args.get('user_name').upper() + '_odoo', server=self.args.get('server_file'), config=self.args.get('config_file'),user_name=self.args.get('user_name')))
        shutil.chown(service_file, self.args.get('user_name'), self.args.get('user_name'))
        return service_file

    def create_clone(self):
        # git_url = base_url = request.env['ir.config_parameter'].sudo().get_param('git.url')
        git.Git(self.args.get('dir')).clone(self.args.get('git_url'))
            # "https://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@github.com/bthakkar-ic-kpi/ic-kpi-prism.git")
        shutil.chown(self.args.get('dir')+'/ic-kpi-prism', self.args.get('user_name'), self.args.get('user_name'))

    def unzip_addons(self):
        with zipfile.ZipFile('/home/dev/odoo14.zip', 'r') as zip_ref:
            zip_ref.extractall(self.args.get('dir'))
        # shutil.chown(self.args.get('dir') + '/odoo14.0', self.args.get('user_name'), self.args.get('user_name'))
        return self.args.get('dir') + '/odoo14.0'

if __name__ == '__main__':
    args = sys.argv[1]
    dict = ast.literal_eval(sys.argv[2])
    cm = ApiCaller(method_to_call=args, **dict)
    resp = cm._method()
    print(resp)