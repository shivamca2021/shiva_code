
from odoo import SUPERUSER_ID, api
from odoo.tools import config


def post_init_hook(cr, registry):
    # This is here to not broke the tests. The idea:
    # - XML changes in website are made using 'customize_show=True'
    # - When Odoo is running in testing mode, we disable our changes
    # - When run our test, we enable the changes and test it. (see test file)
    #
    # For the user it has no impact (only more customizable options in the website)
    # For CI/CD avoids problems testing modules that removes/positioning elements
    # that other modules uses in their tests.
    if config["test_enable"] or config["test_file"]:
        with api.Environment.manage():
            env = api.Environment(cr, SUPERUSER_ID, {})
            env.ref("prism_odoo_rebranding.layout_footer_copyright").active = False
