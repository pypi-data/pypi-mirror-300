# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Stored periods")
    period_name = _("Accounting period")
    period_name_plural = _("Accounting periods")
    year_name = _("Fiscal year")
    year_name_plural = _("Fiscal years")
    fix_y2k = False
    start_year = 2012

    def setup_config_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action("periods.StoredYears")
        m.add_action("periods.StoredPeriods")
