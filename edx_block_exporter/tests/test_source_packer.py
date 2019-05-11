from edx_block_exporter.source_packer import XBlockDecomposer, XBlockField
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory


class SourcePackerTest(ModuleStoreTestCase):

    def setUp(self):
        super(SourcePackerTest, self).setUp()
        self.xblock_type = "toy_xblock_with_fields_only"

        self.course = CourseFactory.create()
        with self.store.bulk_operations(self.course.id):
            self.chapter = ItemFactory.create(parent=self.course, category="chapter", display_name="chapter")
            self.sequence = ItemFactory.create(parent=self.chapter, category='sequential', display_name="chapter")
            self.vertical = ItemFactory.create(parent=self.sequence, category='vertical', display_name='vertical')
            self.problem = ItemFactory.create(parent=self.vertical, category=self.xblock_type, display_name="test")

    def test_decomposer(self):
        block_id = str(self.vertical.children[0])
        xblock_info = XBlockDecomposer(block_id).get_xblock_info()

        import pydevd_pycharm
        pydevd_pycharm.settrace('host.docker.internal', port=3758, stdoutToServer=True, stderrToServer=True)
        print('test')
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
        [self.assertIn(field, xblock_info.fields) for field in expected_fields]
        self.assertEqual(self.xblock_type, xblock_info.block_type)
        self.assertEqual('edx_block_exporter.tests.resource.toy_itemsToyXblockWithFieldsOnly', xblock_info.class_name)

        # Check that installation command contains correct prefix and suffix
        # NOTE (flyingpi): middle part with commit hash is omitted
        self.assertIn('-e git+git@github.com:flying-pi/edx_block_exporter.git@', xblock_info.pip_install_str)
        self.assertIn('#egg=edx_block_exporter', xblock_info.pip_install_str)
