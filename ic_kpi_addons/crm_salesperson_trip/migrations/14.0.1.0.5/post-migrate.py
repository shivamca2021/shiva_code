# -*- coding: utf-8 -*-
def migrate(cr, migrate):
    """
    Migrate to version
    """
    cr.execute(
        'ALTER TABLE crm_salesperson_trip_line DROP CONSTRAINT IF EXISTS crm_salesperson_trip_line_contact_unique'
    )
