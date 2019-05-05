from xblock import plugin

from edx_block_exporter.source_packer import XBlockDecomposer, XBlockField
from edx_block_exporter.tests.resource.toy_items import ToyXblockWithFieldsOnly
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory


class SourcePackerTest(ModuleStoreTestCase):


    def setUp(self):
        super(SourcePackerTest, self).setUp()
        plugin.PLUGIN_CACHE[(u'xblock.v1', 'my_block')] = ToyXblockWithFieldsOnly

        self.course = CourseFactory.create()
        with self.store.bulk_operations(self.course.id):
            self.chapter = ItemFactory.create(parent=self.course, category="chapter", display_name="chapter")
            self.sequence = ItemFactory.create(parent=self.chapter, category='sequential', display_name="chapter")
            self.vertical = ItemFactory.create(parent=self.sequence, category='vertical', display_name='vertical')
            self.problem = ItemFactory.create(parent=self.vertical, category="my_block", display_name="test")

    def test_decomposer(self):
        block_id = str(self.vertical.children[0])
        XBlockDecomposer(block_id).get_xblock_info()
        expected_fields = [
            XBlockField(
                name='all_user_relative', class_name='xblock.fields.String', serializer='json', str_value=None,
                is_save_value=False
            ),
            XBlockField(
                name='settings_relative', class_name='xblock.fields.String', serializer='json',
                str_value=u'this is setting', is_save_value=True
            ),
            XBlockField(
                name='user_relative', class_name='xblock.fields.String', serializer='json', str_value=None,
                is_save_value=False)
        ]
