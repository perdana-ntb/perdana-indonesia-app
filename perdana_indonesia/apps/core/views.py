import json
import operator
from functools import reduce

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import View

# Create your views here.


def list_to_dict(keys, values):
    if len(keys) != len(values):
        raise Exception("Keys and Values length not match")
    result = {}
    for i in range(len(keys)):
        result[keys[i]] = values[i]
    return result


class ColumnTranslator(object):
    def columns_translator(self, columns):
        translated_column = []
        for column in columns:
            if column in self.foreign_columns.keys():
                col = self.foreign_columns.get(column)
            elif column in self.computed_columns.keys():
                col = self.computed_columns.get(column)
            else:
                col = column

            translated_column.append(col)
        return translated_column

    def filter_transform(self, keyword):
        filtered_columns = []
        for column in self.columns_translator(self.filter_columns):
            filtered_columns.append(Q(**{'%s__icontains' % column: keyword}))
        return reduce(operator.or_, filtered_columns)

    def foreign_column_parser(self, column):
        if '__' in column:
            return column.replace('__', '.')
        return column

    def foreign_columns_translator(self):
        translated_foreign_columns = {}
        for k, v in self.foreign_columns.items():
            translated_foreign_columns[k] = self.foreign_column_parser(v)
        return translated_foreign_columns

    def computed_columns_translator(self):
        translated_computed_columns = {}
        for k, v in self.computed_columns.items():
            translated_computed_columns[k] = [self.foreign_column_parser(val) if '__' in val else val for val in v]
        return translated_computed_columns


class ServerSideDataTableView(ColumnTranslator, View):
    queryset = None
    columns = []
    foreign_columns = {}
    computed_columns = {}
    filter_columns = []

    def post(self, request):
        dataset = self._setup_datatables(request)
        return HttpResponse(json.dumps(dataset, cls=DjangoJSONEncoder), content_type='application/json')

    def _setup_datatables(self, request):
        datatables = request.POST
        # Ambil draw
        draw = int(datatables.get('draw'))
        # Ambil start
        start = int(datatables.get('start'))
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = self.queryset.count()
        # Set records filtered
        records_filtered = records_total
        # Ambil semua invoice yang valid
        queryset = self.queryset

        if search:
            queryset = self.queryset.filter(self.filter_transform(search))
            records_total = queryset.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(queryset, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = []
        fileds = self.columns_translator(self.columns)
        keyworded_fields = list_to_dict(self.columns, fileds)
        for i, obj in enumerate(object_list):
            new_obj = {'counter': i + 1}
            for k, field in keyworded_fields.items():
                if isinstance(field, (list, tuple)):
                    values = []
                    for val in field:
                        values.append(eval('obj.%s' % self.foreign_column_parser(val)))
                    new_obj[k] = ' '.join(values)
                else:
                    new_obj[k] = eval('obj.%s' % self.foreign_column_parser(field))
            data.append(new_obj)

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


# ServerSideDataTableView Usage
"""
class MemberLoadView(ServerSideDataTableView):
    queryset = Member.objects.all()
    columns = ['pk', 'username', 'full_name', 'phone', 'gender', 'address', 'club']
    foreign_columns = {
        'username': 'user__username',
        'club': 'club__name'
    }
    computed_columns = {
        'full_name': ['user__first_name', 'user__last_name']
    }
    filter_columns = ['username', 'phone', 'gender', 'club']
"""
