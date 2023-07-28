# -*- coding: utf-8 -*-
from . import models
from . import wizard


def pre_init_hook(cr):
    cr.execute('CREATE EXTENSION IF NOT EXISTS cube')
    cr.execute('CREATE EXTENSION IF NOT EXISTS earthdistance')
