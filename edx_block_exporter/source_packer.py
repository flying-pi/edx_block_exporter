from collections import namedtuple

import pip
import pkg_resources
from xblock.fields import UserScope, Sentinel

from contentstore.views.helpers import usage_key_with_run
from xmodule.modulestore.django import modulestore


def _named_tuple_to_dict(tuple):
    return {name: getattr(tuple, name) for name in tuple._fields}


XBlockField = namedtuple("XBlockField", ['name', 'class_name', 'serializer', 'str_value', 'is_save_value'])


class XBlockInfo(namedtuple("BaseXBlockInfo", ['fields', 'class_name', 'pip_install_str', 'block_type'])):

    def as_dict(self):
        result = {}
        for name, value in _named_tuple_to_dict(self).items():
            if name == 'fields':
                value = [_named_tuple_to_dict(field) for field in value]
            result[name] = value
        return result


class XBlockDecomposer(object):
    def __init__(self, block_usage_key_str):
        """
        :param str block_usage_key_str: string representation of the block
        """
        super(XBlockDecomposer, self).__init__()
        self.block_usage_key = usage_key_with_run(block_usage_key_str)
        self.block = modulestore().get_item(self.block_usage_key)

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
                # if isinstance(getattr(self.block, name), datetime):
                    # import pydevd_pycharm
                    # pydevd_pycharm.settrace('host.docker.internal', port=3758, stdoutToServer=True, stderrToServer=True)
                    # print ('asdasd')
                field_info['str_value'] = module.fields[name].to_json(getattr(self.block, name))
                field_info['is_save_value'] = True

            fields.append(XBlockField(**field_info))
        return fields

    def _get_setup_instruction(self, block_type):
        entrypoints = list(pkg_resources.iter_entry_points(self.block.entry_point, name=block_type))
        if len(entrypoints) != 1:
            return None
        requariment = pip.FrozenRequirement.from_dist(entrypoints[0].dist, [])
        return str(requariment).strip()

    def get_xblock_info(self):
        module = self.block.unmixed_class
        block_type = self.block_usage_key.block_type
        return XBlockInfo(
            fields=self._get_fields_info(module),
            class_name='.'.join([module.__module__, module.__name__]),
            pip_install_str=self._get_setup_instruction(block_type),
            block_type=block_type
        )
