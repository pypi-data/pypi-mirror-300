# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.api import dd
from lino import mixins
from lino.utils import last_day_of_month
from lino.mixins.periods import DateRange
from lino.mixins import Referrable

from lino.modlib.office.roles import OfficeStaff


class PeriodStates(dd.Workflow):
    pass

add = PeriodStates.add_item
add('10', _("Open"), 'open')
add('20', _("Closed"), 'closed')


class StoredYear(DateRange, Referrable):

    class Meta:
        app_label = 'periods'
        verbose_name = _("Fiscal year")
        verbose_name_plural = _("Fiscal years")
        ordering = ['ref']

    preferred_foreignkey_width = 10

    state = PeriodStates.field(default='open')

    @classmethod
    def get_simple_parameters(cls):
        yield super().get_simple_parameters()
        yield "state"

    @classmethod
    def year2ref(cls, year):
        if dd.plugins.periods.fix_y2k:
            if year < 2000:
                return str(year)[-2:]
            elif year < 3000:
                return chr(int(str(year)[-3:-1]) + 65) + str(year)[-1]
            else:
                raise Exception("20180827")
            # elif year < 2010:
            #     return "A" + str(year)[-1]
            # elif year < 2020:
            #     return "B" + str(year)[-1]
            # elif year < 2030:
            #     return "C" + str(year)[-1]
            # else:
            # raise Exception(20160304)
        # return str(year)[2:]
        return str(year)

    @classmethod
    def from_int(cls, year, *args):
        ref = cls.year2ref(year)
        return cls.get_by_ref(ref, *args)

    @classmethod
    def create_from_year(cls, year):
        ref = cls.year2ref(year)
        return cls(ref=ref,
                   start_date=datetime.date(year, 1, 1),
                   end_date=datetime.date(year, 12, 31))
        # obj.full_clean()
        # obj.save()
        # return obj

    @classmethod
    def get_or_create_from_date(cls, date):
        obj = cls.from_int(date.year, None)
        if obj is None:
            obj = cls.create_from_year(date.year)
            obj.full_clean()
            obj.save()
        return obj

    def __str__(self):
        return self.ref


class StoredPeriod(DateRange, Referrable):

    class Meta:
        ordering = ['ref']
        app_label = 'periods'
        verbose_name = dd.plugins.periods.period_name
        verbose_name_plural = dd.plugins.periods.period_name_plural

    preferred_foreignkey_width = 10

    state = PeriodStates.field(default='open')
    year = dd.ForeignKey('periods.StoredYear', blank=True, null=True)
    remark = models.CharField(_("Remark"), max_length=250, blank=True)

    @classmethod
    def get_simple_parameters(cls):
        yield super().get_simple_parameters()
        yield "state"
        yield "year"

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super().get_request_queryset(ar)
        if (pv := ar.param_values) is None: return qs

        # if pv.start_date is None or pv.end_date is None:
        #     period = None
        # else:
        #     period = (pv.start_date, pv.end_date)
        # if period is not None:
        #     qs = qs.filter(dd.inrange_filter('start_date', period))
        if pv.start_date or pv.end_date:
            qs = qs.filter(dd.overlap_range_filter(
                pv.start_date, pv.end_date, "start_date", "end_date"))
        # if pv.start_date:
        #     qs = qs.filter(dd.range_filter(pv.start_date, 'start_date', 'end_date'))
        #     # qs = qs.filter(start_date__gte=pv.start_date)
        # if pv.end_date:
        #     qs = qs.filter(dd.range_filter(pv.end_date, 'start_date', 'end_date'))
            # qs = qs.filter(end_date__lte=pv.end_date)
        return qs

    @classmethod
    def get_available_periods(cls, today):
        """Return a queryset of periods available for booking."""
        if today is None:  # added 20160531
            today = dd.today()
        fkw = dict(start_date__lte=today, end_date__gte=today)
        return cls.objects.filter(**fkw)

    @classmethod
    def get_ref_for_date(cls, d):
        """Return a text to be used as :attr:`ref` for a new period.

        Alternative implementation for usage on a site with movements
        before year 2000::

            @classmethod
            def get_ref_for_date(cls, d):
                if d.year < 2000:
                    y = str(d.year - 1900)
                elif d.year < 2010:
                    y = "A" + str(d.year - 2000)
                elif d.year < 2020:
                    y = "B" + str(d.year - 2010)
                elif d.year < 2030:
                    y = "C" + str(d.year - 2020)
                return y + "{:0>2}".format(d.month)

        """
        y = StoredYear.year2ref(d.year)
        return "{}-{:0>2}".format(y, d.month)

        # if dd.plugins.periods.fix_y2k:
        #     return rt.models.periods.StoredYear.from_int(d.year).ref \
        #         + "{:0>2}".format(d.month)

        # return "{0.year}-{0.month:0>2}".format(d)

        # """The template used for building the :attr:`ref` of an
        # :class:`StoredPeriod`.
        #
        # `Format String Syntax
        # <https://docs.python.org/2/library/string.html#formatstrings>`_
        #
        # """

    @classmethod
    def get_periods_in_range(cls, p1, p2):
        return cls.objects.filter(ref__gte=p1.ref, ref__lte=p2.ref)

    @classmethod
    def get_period_filter(cls, fieldname, p1, p2, **kwargs):
        if p1 is None:
            return kwargs

        # ignore preliminary movements if a start_period is given:
        # kwargs[voucher_prefix + "journal__preliminary"] = False

        # accounting_period = voucher_prefix + "accounting_period"

        if p2 is None:
            kwargs[fieldname] = p1
        else:
            periods = cls.get_periods_in_range(p1, p2)
            kwargs[fieldname + '__in'] = periods
        return kwargs

    @classmethod
    def get_default_for_date(cls, d):
        ref = cls.get_ref_for_date(d)
        obj = cls.get_by_ref(ref, None)
        if obj is None:
            values = dict(start_date=d.replace(day=1))
            values.update(end_date=last_day_of_month(d))
            values.update(ref=ref)
            obj = StoredPeriod(**values)
            obj.full_clean()
            obj.save()
        return obj

    def full_clean(self, *args, **kwargs):
        if self.start_date is None:
            self.start_date = dd.today().replace(day=1)
        if not self.year:
            self.year = StoredYear.get_or_create_from_date(self.start_date)
        super().full_clean(*args, **kwargs)

    def __str__(self):
        if not self.ref:
            return dd.obj2str(self)
            # "{0} {1} (#{0})".format(self.pk, self.year)
        return self.ref


StoredPeriod.set_widget_options('ref', width=6)


class StoredYears(dd.Table):
    model = 'periods.StoredYear'
    required_roles = dd.login_required(OfficeStaff)
    column_names = "ref start_date end_date state *"
    # detail_layout = """
    # ref id
    # start_date end_date
    # """

class StoredPeriods(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = 'periods.StoredPeriod'
    order_by = ["ref", "start_date", "year"]
    column_names = "ref start_date end_date year state remark *"
