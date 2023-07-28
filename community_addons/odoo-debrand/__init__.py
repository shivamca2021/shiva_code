# -*- coding: utf-8 -*-

from . import controllers
from . import models

def _pre_init_partner(cr):
    """ Replace OdooBot Partner Name
    """
    
    cr.execute("""UPDATE res_partner
                     SET name='IC-KPI',display_name='IC-KPI',email='ICKPI@example.com' where name='OdooBot';""")

