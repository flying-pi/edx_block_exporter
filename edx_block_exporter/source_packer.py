import inspect

import os
from collections import namedtuple
from importlib import  import_module

from xblock.fields import UserScope, Sentinel

from contentstore.views.helpers import usage_key_with_run
from xmodule.modulestore.django import modulestore

import numpy as np

import modulefinder

XBlockInfo = namedtuple("XBlockInfo", ['fields', 'xblock_class', 'instance_object'])
XBlockField = namedtuple("XBlockField", ['name', 'class_name', 'serializer', 'str_value', 'is_save_value'])


class XBlockDecomposer(object):
    def __init__(self, block_usage_key_str):
        """
        :param str block_usage_key_str: string representation of the block
        """
        super(XBlockDecomposer, self).__init__()
        self.block = self._get_block_by_string_id(block_usage_key_str)

    @staticmethod
    def _get_block_by_string_id(block_usage_key_str):
        block_key = usage_key_with_run(block_usage_key_str)
        store = modulestore()
        return store.get_item(block_key)

    def _get_fields_info(self, module):
        fields = []
        for name, value in module.fields.items():
            if isinstance(value.scope, Sentinel):
                continue
            field_info = {
                'name': value.name,
                'class_name': '.'.join([value.__class__.__module__, value.__class__.__name__]),
                'serializer': 'json', 'str_value': None, 'is_save_value': False
            }

            if value.scope.user == UserScope.NONE:
                field_info['str_value'] = module.fields['name'].to_json(getattr(self.block, name))
                field_info['is_save_value'] = True

            fields.append(XBlockField(**field_info))
        return fields

    def _get_dep_modules_name(self, module):

        package_to_discover = [ import_module(module.__module__.split('.')[0])]
        module_names = [module.__module__]

        while package_to_discover:
            iteration_module = package_to_discover.pop()
            for member_name in dir(iteration_module):
                try:
                    member = getattr(iteration_module, member_name)
                except:
                    # NOTE(flyingpi): Need to take decision, dies we need certain exception type
                    # FIXME(flyingpi): logs required
                    continue
                if not inspect.ismodule(member):
                    continue
                member_module_name = member.__name__
                if member_module_name in module_names:
                    continue
                module_names.append(member_module_name)
                package_to_discover.append(member)
                root_module = member_module_name.split('.')[0]
                if root_module == member_module_name:
                    continue
                module_names.append(root_module)
                package_to_discover.append(import_module(root_module))

        unique_root_modules_name = {name.split('.')[0] for name in module_names}
        return list(unique_root_modules_name)

    def _get_relative_pathes(self, dep_modules):
        c = 0
        for i in dep_modules:
            try:
                import_module(i).__file__
            except:
                print c
                print i
            c+=1
        imp.find_module('heapq')
        import pydevd_pycharm
        pydevd_pycharm.settrace('host.docker.internal', port=3758, stdoutToServer=True, stderrToServer=True)
        print('asasasasas')








    def get_xblock_info(self):
        module = self.block.unmixed_class
        fields = self._get_fields_info(module)
        dep_modules = self._get_dep_modules_name(module)
        dep_file_pathes = self._get_relative_pathes(dep_modules)

"""
import sys, traceback
try:
    
    self._get_recursive_root_path_dep(imported_module)
    
except:
    traceback.print_exc(file=sys.stdout)


"""