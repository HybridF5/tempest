import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.api.compute.flavors.test_image_metadata import ImagesMetadataTestJSON
from tempest.api.compute.flavors.test_image_metadata_negative import ImagesMetadataTestJSON \
    as ImagesMetadataNegativeTestJSON
from tempest.api.compute.flavors.test_images import ImagesTestJSON
from tempest.api.compute.flavors.test_images_negative import ImagesNegativeTestJSON
from tempest.api.compute.flavors.test_images_oneserver import ImagesOneServerTestJSON
from tempest.api.compute.flavors.test_images_oneserver_negative import ImagesOneServerNegativeTestJSON
from tempest.api.compute.flavors.test_list_image_filters import ListImageFiltersTestJSON
from tempest.api.compute.flavors.test_list_image_filters_negative import ListImageFiltersNegativeTestJSON
from tempest.api.compute.flavors.test_list_images import ListImagesTestJSON
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridImagesMetadataTestJSON(ImagesMetadataTestJSON):
    """Test Imges Metadata"""

class HybridImagesMetadataNegativeTestJSON(ImagesMetadataNegativeTestJSON):
    """Test Images Metadata"""

class HybridImagesTestJSON(ImagesTestJSON):
    """Test Imges"""

    @testtools.skip('Change to two az versions')
    @test.idempotent_id('aaacd1d0-55a2-4ce8-818a-b5439df8adc9')
    def test_create_image_from_stopped_server(self):
        server = self.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.default_availability_zone)
        self.servers_client.stop_server(server['id'])
        waiters.wait_for_server_status(self.servers_client,
                                       server['id'], 'SHUTOFF')
        self.addCleanup(self.servers_client.delete_server, server['id'])
        snapshot_name = data_utils.rand_name('test-snap')
        image = self.create_image_from_server(server['id'],
                                              name=snapshot_name,
                                              wait_until='ACTIVE',
                                              wait_for_server=False)
        self.addCleanup(self.client.delete_image, image['id'])
        self.assertEqual(snapshot_name, image['name'])

    @test.idempotent_id('aaacd1d0-55a2-4ce8-818a-b5439df8adc8')
    def test_create_image_from_stopped_server_vcloud(self):
        server = self.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.vcloud_availability_zone)
        self.servers_client.stop_server(server['id'])
        waiters.wait_for_server_status(self.servers_client,
                                       server['id'], 'SHUTOFF')
        self.addCleanup(self.servers_client.delete_server, server['id'])
        snapshot_name = data_utils.rand_name('test-snap')
        image = self.create_image_from_server(server['id'],
                                              name=snapshot_name,
                                              wait_until='ACTIVE',
                                              wait_for_server=False)
        self.addCleanup(self.client.delete_image, image['id'])
        self.assertEqual(snapshot_name, image['name'])

    @test.idempotent_id('aaacd1d0-55a2-4ce8-818a-b5439df8adc7')
    def test_create_image_from_stopped_server_aws(self):
        server = self.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.aws_availability_zone)
        self.servers_client.stop_server(server['id'])
        waiters.wait_for_server_status(self.servers_client,
                                       server['id'], 'SHUTOFF')
        self.addCleanup(self.servers_client.delete_server, server['id'])
        snapshot_name = data_utils.rand_name('test-snap')
        image = self.create_image_from_server(server['id'],
                                              name=snapshot_name,
                                              wait_until='ACTIVE',
                                              wait_for_server=False)
        self.addCleanup(self.client.delete_image, image['id'])
        self.assertEqual(snapshot_name, image['name'])

class HybridImagesNegativeTestJSON(ImagesNegativeTestJSON):
    """Test Imges"""

    @test.attr(type=['negative'])
    @test.idempotent_id('6cd5a89d-5b47-46a7-93bc-3916f0d84973')
    def test_create_image_from_deleted_server(self):
        # An image should not be created if the server instance is removed
        server = self.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.default_availability_zone)

        # Delete server before trying to create server
        self.servers_client.delete_server(server['id'])
        waiters.wait_for_server_termination(self.servers_client, server['id'])
        # Create a new image after server is deleted
        name = data_utils.rand_name('image')
        meta = {'image_type': 'test'}
        self.assertRaises(lib_exc.NotFound,
                          self.create_image_from_server,
                          server['id'], name=name, meta=meta)

class HybridImagesOneVCloudServerTestJSON(ImagesOneServerTestJSON):
    """Test Imges"""

    @classmethod
    def resource_setup(cls):
        super(ImagesOneServerTestJSON, cls).resource_setup()
        server = cls.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.vcloud_availability_zone)
        cls.server_id = server['id']

class HybridImagesOneAwsServerTestJSON(ImagesOneServerTestJSON):
    """Test Imges"""

    @classmethod
    def resource_setup(cls):
        super(ImagesOneServerTestJSON, cls).resource_setup()
        server = cls.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.aws_availability_zone)
        cls.server_id = server['id']

class HybridImagesOneVCloudServerNegativeTestJSON(ImagesOneServerNegativeTestJSON):
    """Test Imges"""

    @classmethod
    def resource_setup(cls):
        super(ImagesOneServerNegativeTestJSON, cls).resource_setup()
        server = cls.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.vcloud_availability_zone)
        cls.server_id = server['id']

        cls.image_ids = []

class HybridImagesOneAwsServerNegativeTestJSON(ImagesOneServerNegativeTestJSON):
    """Test Imges"""

    @classmethod
    def resource_setup(cls):
        super(ImagesOneServerNegativeTestJSON, cls).resource_setup()
        server = cls.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.aws_availability_zone)
        cls.server_id = server['id']

        cls.image_ids = []

class HybridListImageFiltersTestJSON(ListImageFiltersTestJSON):
    """Test Imges"""

    @classmethod
    def resource_setup(cls):
        super(ListImageFiltersTestJSON, cls).resource_setup()

        def _create_image():
            name = data_utils.rand_name('image')
            body = cls.glance_client.create_image(name=name,
                                                  container_format='bare',
                                                  disk_format='raw',
                                                  is_public=False)['image']
            image_id = body['id']
            cls.images.append(image_id)
            # Wait 1 second between creation and upload to ensure a delta
            # between created_at and updated_at.
            time.sleep(1)
            image_file = six.StringIO(('*' * 1024))
            cls.glance_client.update_image(image_id, data=image_file)
            waiters.wait_for_image_status(cls.client, image_id, 'ACTIVE')
            body = cls.client.show_image(image_id)['image']
            return body

        # Create non-snapshot images via glance
        cls.image1 = _create_image()
        cls.image1_id = cls.image1['id']
        cls.image2 = _create_image()
        cls.image2_id = cls.image2['id']
        cls.image3 = _create_image()
        cls.image3_id = cls.image3['id']

        if not CONF.compute_feature_enabled.snapshot:
            return

        # Create instances and snapshots via nova
        cls.server1 = cls.create_test_server(availability_zone=CONF.compute.default_availability_zone)
        cls.server2 = cls.create_test_server(wait_until='ACTIVE',
                                             availability_zone=CONF.compute.default_availability_zone)
        # NOTE(sdague) this is faster than doing the sync wait_util on both
        waiters.wait_for_server_status(cls.servers_client,
                                       cls.server1['id'], 'ACTIVE')

        # Create images to be used in the filter tests
        cls.snapshot1 = cls.create_image_from_server(
            cls.server1['id'], wait_until='ACTIVE')
        cls.snapshot1_id = cls.snapshot1['id']

        # Servers have a hidden property for when they are being imaged
        # Performing back-to-back create image calls on a single
        # server will sometimes cause failures
        cls.snapshot3 = cls.create_image_from_server(
            cls.server2['id'], wait_until='ACTIVE')
        cls.snapshot3_id = cls.snapshot3['id']

        # Wait for the server to be active after the image upload
        cls.snapshot2 = cls.create_image_from_server(
            cls.server1['id'], wait_until='ACTIVE')
        cls.snapshot2_id = cls.snapshot2['id']

class HybridListImageFiltersNegativeTestJSON(ListImageFiltersNegativeTestJSON):
    """Test Imges"""

class HybridListImagesTestJSON(ListImagesTestJSON):
    """Test Imges"""
