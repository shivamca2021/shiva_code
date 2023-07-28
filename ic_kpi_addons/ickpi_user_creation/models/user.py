# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
import logging
import psycopg2
from psycopg2 import sql
_logger = logging.getLogger(__name__)
from odoo.http import request
import requests
import os
import subprocess
import random
import crypt
import shutil
import zipfile
import odoo
from odoo import SUPERUSER_ID

class Partner(models.Model):
    _inherit = 'res.partner'

    create_instance = fields.Boolean('Create Instance')
    create_instance_done = fields.Boolean('Create Instance Done')

    def common_subprocess(self, values=None, method_name=None):
        try:
            # create_file_location='/home/dev/ic-kpi-prism/ic_kpi_addons/ickpi_user_creation/models/create_file.py'
            create_file_location =os.path.join(os.path.dirname(__file__),'create_file.py')
            _logger.info(">>>>>>>>>>>>>>>>>>>create_file_location>>>>>>>>>>>>%s", create_file_location)
            # sudo_password = "@')U(WmY~EfD"
            sudo_password = request.env['ir.config_parameter'].sudo().get_param('user.creation')
            _logger.info(">>>>>>>>>>>>>>>>>>>sudo password>>>>>>>>>>>>%s", sudo_password)
            cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
            a = subprocess.Popen(['sudo', '-S', 'python3', create_file_location, method_name, str(values)],stdin=cmd1.stdout, stdout=subprocess.PIPE,stderr= subprocess.PIPE)
            path = a.stdout.read().decode().strip()
            error = a.stderr.read().decode()
            _logger.info("error config_path>>>>>>>>>>>>>>>>>>>>> error %s.", error)
            _logger.info("config_path>>>>>>>>>>>>>>>>>>>>> path %s.", path)
            return path
        except Exception as e:
            _logger.exception(e)

    def call_log_file(self,user_name=None):
        values = {'user_name': user_name}
        method_name = 'create_log_file'
        log_file = self.sudo().common_subprocess(values,method_name)
        return log_file

    def call_config_file(self, user_name=None,log_file=None,port=None):
        values = {'user_name': user_name, 'log_file': log_file, 'port':port}
        method_name = 'create_config_file'
        config_file = self.sudo().common_subprocess(values, method_name)
        return config_file
    # try:
    #         # create_file_location='/home/dev/ic-kpi-prism/ic_kpi_addons/ickpi_user_creation/models/create_file.py'
    #         create_file_location =os.path.join(os.path.dirname(__file__),'create_file.py')
    #
    #         sudo_password = "@')U(WmY~EfD"
    #         values = {'user_name': user_name, 'log_file': log_file}
    #         cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
    #         a = subprocess.Popen(['sudo', '-S', 'python3', create_file_location, 'create_config_file', str(values)], stdin=cmd1.stdout, stdout=subprocess.PIPE)
    #         _logger.info("subprocess>>>>>>>>>>>>>>>>>>>>> log file %s.", a)
    #         config_path = a.stdout.read().decode().strip()
    #         _logger.info("config_path>>>>>>>>>>>>>>>>>>>>> config_path %s.", config_path)
    #         return config_path
    #     except Exception as e:
    #         _logger.exception(e)




    def call_access_log_file(self,user_name=None):
        values = {'user_name': user_name}
        method_name = 'create_access_log_file'
        access_log_file = self.sudo().common_subprocess(values, method_name)
        return access_log_file

    def call_error_log_file(self,user_name=None):
        values = {'user_name': user_name}
        method_name = 'create_error_log_file'
        error_log_file = self.sudo().common_subprocess(values, method_name)
        return error_log_file



    def call_nginx_file(self,user_name=None,access_log_file=None,error_log_file=None,port=None):
        values = {'user_name': user_name,'access_log_file':access_log_file,'error_log_file':error_log_file,'port':port}
        method_name = 'create_nginx_file'
        nginx_file = self.sudo().common_subprocess(values, method_name)
        return nginx_file

    def call_server_file(self, user_name=None):
        values = {'user_name': user_name}
        method_name = 'create_server_file'
        server_file = self.sudo().common_subprocess(values, method_name)
        return server_file

    def call_service_file(self, user_name=None, server_file=None,config_file=None):
        values = {'user_name': user_name, 'server_file': server_file, 'config_file': config_file}
        method_name = 'create_service_file'
        service_file = self.sudo().common_subprocess(values, method_name)
        return service_file

    def _cron_to_create_instance(self):
        contacts = self.sudo().search([('create_instance', '=', True), ('create_instance_done', '=', False)])
        for line in contacts:
            seq=random.randrange(start=10 ** 5, stop=10 ** 6, step=1)
            user_name = line.name.replace(' ', '').lower() + str(seq)
            password = user_name
            port_id = self.env['instance.port'].sudo().search([('booked','=',False)],limit=1)
            if port_id:
                port = port_id.port_no
            if not port_id:
                vals = {
                    'name': str(line.id),
                    'user': user_name,
                    'password': user_name,
                    'log_file': '',
                    'config_file': '',
                    'nginx_file': '',
                    'service_file': '',
                    'server_file': '',
                    'domain_name': '',
                    'is_active': False,
                    'message': 'Port Not Available',
                    'partner_id' : line.id
                }
                _logger.info("Port not available %s", vals)
                instance_id = self.env['user.instance'].sudo().create(vals)
                _logger.info("Instance Create Id %s", instance_id)
                continue
            try:
                user_name, password = self.userCreation(user_name,password)
                sudo_password = request.env['ir.config_parameter'].sudo().get_param('user.creation')
                _logger.info(">>>>>>>>>>>>>>>>>>>sudo password>>>>>>>>>>>>%s",sudo_password)
                user_dir = '/home/'+user_name
                encpass = crypt.crypt(password,"22")
                cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
                cmd = ["sudo", "-S", "useradd", "-m", "-d", user_dir, "-U", "-r", "-s", "/bin/bash", user_name, "-p", encpass]
                z = subprocess.Popen(cmd, stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
                path = z.stdout.read().decode().strip()
                error = z.stderr.read().decode()
                _logger.info("error user creation>>>>>>>>>>>>>>>>>>>> error %s.", error)
                _logger.info("user creation>>>>>>>>>>>>>>>>>>>>> path %s.", path)
                cmd2 = ["sudo", "-S", "usermod", "-a", "-G", "sudo", user_name]
                f = subprocess.Popen(cmd2, stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                sudo_path = f.stdout.read().decode().strip()
                sudo_error = f.stderr.read().decode()
                _logger.info("error Sudo privillage>>>>>>>>>>>>>>>>>>>> sudo_error %s.", sudo_error)
                _logger.info("sudo Privillage>>>>>>>>>>>>>>>>>>>>> sudo_path %s.", sudo_path)

                git_url = request.env['ir.config_parameter'].sudo().get_param('git.url')
                values = {'dir':user_dir,'git_url':git_url, 'user_name':user_name}
                _logger.info("Git Clone direcory %s.", values)
                method_name = 'create_clone'
                self.sudo().common_subprocess(values, method_name)
                _logger.info("Git Clone created %s.", user_name)

                log_file=self.sudo().call_log_file(user_name)
                _logger.info("Created log file %s.", log_file)
                config_file=self.sudo().call_config_file(user_name,log_file,port)
                _logger.info("Created config file %s.", config_file)
                access_log_file=self.sudo().call_access_log_file(user_name)
                _logger.info("Created access log file %s.", access_log_file)
                error_log_file=self.sudo().call_error_log_file(user_name)
                _logger.info("Created error log file %s.", access_log_file)
                nginx_file=self.call_nginx_file(user_name,access_log_file,error_log_file,port)
                server_file=self.call_server_file(user_name)
                service_file=self.call_service_file(user_name,server_file,config_file)

                method_name = 'unzip_addons'
                values = {'dir': '/home/' + user_name, 'user_name': user_name}
                url = self.sudo().common_subprocess(values, method_name)
                _logger.info(">>>>>>>>>>>>>>>>addons>>>>>>>%s>>>>>", url)

                line.sudo().write({'create_instance_done': True})
                port_id.sudo().write({'booked': True})
                exist = self.env['user.instance'].sudo().search([('partner_id', '=', line.id)])
                vals={
                    'name':str(line.id),
                    'user':user_name,
                    'password':user_name,
                    'log_file':log_file,
                    'config_file':config_file,
                    'nginx_file':nginx_file,
                    'service_file':service_file,
                    'server_file':server_file,
                    'domain_name':user_name+'.ic-prism.com',
                    'is_active': True,
                    'message': 'Success',
                    'partner_id': line.id
                }
                _logger.info("Instance Create Vals %s", vals)
                if exist:
                    instance_id = exist.sudo().write(vals)
                else:
                    instance_id = self.env['user.instance'].sudo().create(vals)
                _logger.info("Instance Create Id %s", instance_id)

                conn = psycopg2.connect(
                    database="postgres", user=user_name, password=password, host='127.0.0.1', port='5432'
                )
                conn.autocommit = True
                master_pwd = request.env['ir.config_parameter'].sudo().get_param('master.instance.creation.password')
                # master_pwd = 'S-Q3gh^]'
                name = user_name
                url = "https://dev.ic-prism.com/web/database/restore"
                payload = {'master_pwd': master_pwd,
                           'copy': 'true',
                           'name': name}
                files = [
                    ('backup_file', ('falcontest_2022-05-10_08-33-30.zip',
                                     open('/home/dev/ic-kpi-prism/kpi_prism_adapt_nodemo_data_2022-06-28_16-18-27.zip', 'rb'),
                                     'application/zip'))
                ]
                headers = {
                    'Cookie': 'session_id=7a6878bff84565fab5f4abe29eab7bc1256da960'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)

                print(response.text)
                ownerdb = sql.SQL("Alter DATABASE {0} OWNER TO {1}").format(
                    sql.Identifier(user_name),
                    sql.Identifier(user_name),
                )
                cur = conn.cursor()
                cur.execute(ownerdb.as_string(conn))
                cur.execute("COMMIT")
                print("Database created successfully........")

                registry = odoo.modules.registry.Registry.new(name)
                with registry.cursor() as cr:
                    env = odoo.api.Environment(cr, SUPERUSER_ID, {})
                    env['res.partner'].sudo().create({'name': 'create from instance'})
                    _logger.info(">>>>>>>>>>>>>>>call registry env>>>>>>>>>>>>>>>>>")

                cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
                _logger.info(">>>>>>>>>>>>>>>instance_id.server_file.split('/')[3]>>>>>>>>>>>>>>>>>%s",
                             instance_id.server_file.split('/')[3])
                cmd = ["sudo", "-S", "systemctl", "restart", instance_id.server_file.split('/')[3]]

                subprocess.Popen(cmd,
                                     stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Closing the connection
                conn.close()



            except FileNotFoundError:
                print("The 'docs' directory does not exist")

    def userCreation(self, user_name=None, password=None):
        con = psycopg2.connect(
            user='dev',
            host='127.0.0.1',
            port='5432',
            password='dev',
        )
        query = sql.SQL("CREATE ROLE {0} LOGIN PASSWORD {1}").format(
            sql.Identifier(user_name),
            sql.Literal(password),
        )
        cur = con.cursor()
        cur.execute(query.as_string(con))
        cur.execute("COMMIT")
        createdb = sql.SQL("Alter user {0} CREATEDB").format(
            sql.Identifier(user_name),
        )
        cur.execute(createdb.as_string(con))
        cur.execute("COMMIT")
        superuser = sql.SQL("ALTER user {0} WITH SUPERUSER").format(
            sql.Identifier(user_name),
        )
        cur.execute(superuser.as_string(con))
        cur.execute("COMMIT")

        return user_name, password


class UserInstance(models.Model):
    _name = 'user.instance'

    name = fields.Char('Name')
    user = fields.Char('Login Instance')
    password = fields.Char('Password')
    log_file = fields.Char('Log File')
    config_file = fields.Char('Config File')
    nginx_file = fields.Char('Nginx File')
    server_file = fields.Char('Server File')
    service_file = fields.Char('Service File')
    domain_name = fields.Char('Domain Name')
    is_active = fields.Boolean('Is Active')
    message = fields.Char('Message')
    partner_id = fields.Many2one('res.partner', 'Contact')


    def add_addons(self):
        for record in self:
            method_name = 'unzip_addons'
            values = {'dir':'/home/'+record.user, 'user_name': record.user}
            url=self.env['res.partner'].sudo().common_subprocess(values, method_name)
            _logger.info(">>>>>>>>>>>>>>>>addons>>>>>>>%s>>>>>",url)

    def restart_user_service(self):
        for record in self:
            sudo_password = request.env['ir.config_parameter'].sudo().get_param('user.creation')
            cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
            _logger.info(">>>>>>>>>>>>>>>record.server_file.split('/')[3]>>>>>>>>>>>>>>>>>%s",record.server_file.split('/')[3])
            # cmd = ["sudo", "-S", "useradd", "-d", user_dir, "-m", user_name, "-p", encpass]
            cmd = ["sudo", "-S", "systemctl", "restart", record.server_file.split('/')[3]]

            z = subprocess.Popen(cmd,
                                 stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            path = z.stdout.read().decode().strip()
            error = z.stderr.read().decode()
            _logger.info("error Service>>>>>>>>>>>>>>>>>>>> error %s.", error)
            _logger.info("user Service>>>>>>>>>>>>>>>>>>>>> path %s.", path)

class InstancePort(models.Model):
    _name = 'instance.port'

    port_no = fields.Char('Port No.')
    booked = fields.Boolean('Booked')


