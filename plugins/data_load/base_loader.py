import csv
from plugins.data_load.load_utils import (
    cast_date, match_to_choice_if_possible, get_from_ll
)
from django.utils.translation import gettext as _
from opal.models import Patient
from entrytool.models import Demographics
from opal.core.fields import ForeignKeyOrFreeText
import traceback as py_traceback


class Loader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.errors = []
        self.idx = 1
        self.row = None

    def add_error(self, column, value, short_description):
        """
        A utility method that adds an error row, it takes a column,
        value and short description and pulls the file and row number
        off the object. It populates the traceback from traceback.format_exc()
        """
        exception_stack = py_traceback.format_exc()
        if exception_stack:
            traceback = [i for i in exception_stack.split("\n") if i][1:]
        else:
            traceback = []
        self.errors.append(dict(
            file=self.file_name,
            row=self.idx,
            value=value,
            column=column,
            short_description=short_description,
            traceback=traceback
        ))

    def load_rows(self, data):
        rows = list(csv.DictReader(data))
        for row in rows:
            self.idx += 1
            self.row = row
            self.load_row(row)
        return self.errors

    def load_rows_from_file(self, file_name):
        with open(file_name, encoding="utf-8-sig") as f:
            self.load_rows_from_data(f)
        return self.errors

    def check_and_get_date(self, column):
        value = self.row.get(column)
        some_dt = None
        try:
            some_dt = cast_date(value)
        except Exception:
            description = _("Unable to parse %s into a date with the formats dd/mm/yyyy or yyyy-mm-dd") % value
            self.add_error(column, value, description)
        return some_dt

    def _check_fk_or_ft(self, model, field_name, value):
        field = getattr(model, field_name)
        result = get_from_ll(value, field.foreign_model)
        if result:
            return result
        if not result:
            field = model._get_field(f"{field_name}_ft")
            max_length = field.max_length
            if len(value) > max_length:
                raise ValueError(
                    _('Field is %(len_value)d long and should be less than %(max_length)d' % {
                        "len_value": len(value),
                        "max_length": max_length
                    })
                )
        return value

    def check_and_get_string(self, model, field_name, column):
        value = self.row.get(column)
        result = None
        if not value:
            return ""
        try:
            field = getattr(model, field_name)
            if isinstance(field, ForeignKeyOrFreeText):
                result = self._check_fk_or_ft(model, field_name, value)
            else:
                field = model._meta.get_field(field_name)
                if field.choices:
                    result = match_to_choice_if_possible(value, field.choices)
            if not result:
                result = value
                max_length = field.max_length
                if len(result) > max_length:
                    raise ValueError(
                        _('Field is %(len_value)d long and should be less than %(max_length)d') % {
                            "len_value": len(result),
                            "max_length": max_length
                        })

        except Exception as err:
            self.add_error(column, value, str(err))
        return result

    def check_and_get_patient_from_external_identifier(self, column):
        value = self.row.get(column)
        try:
            if not value:
                raise ValueError(
                    _("No external identifier found")
                )
        except Exception as err:
            self.add_error(column, value, str(err))
            return
        hospital_number = self.check_and_get_string(
            Demographics, 'hospital_number', column
        )
        patient = None
        try:
            patient = Patient.objects.get(
                demographics__hospital_number=hospital_number
            )
        except Exception:
            self.add_error(
                column,
                value,
                _('Unable to find a patient with external identifier %s') % value
            )
        return patient

    def check_and_get_float(self, column):
        value = self.row.get(column)
        result = None
        try:
            result = float(value)
        except Exception:
            self.add_error(column, value, _('Unable to parse %s to a float') % value)
        return result

    def format_traceback(self, traceback):
        if traceback:
            return [i for i in traceback.split("\n") if i][1:]
        return []

    def load_row(self, row):
        raise NotImplementedError('Please implement this')
