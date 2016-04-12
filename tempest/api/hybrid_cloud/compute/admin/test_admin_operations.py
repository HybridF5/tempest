import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.api.compute.admin.test_availability_zone import AZAdminV2TestJSON
from tempest.api.compute.admin.test_availability_zone_negative import AZAdminNegativeTestJSON
from tempest.api.compute.admin.test_hosts import HostsAdminTestJSON
from tempest.api.compute.admin.test_hosts_negative import HostsAdminNegativeTestJSON
from tempest.api.compute.admin.test_hypervisor import HypervisorAdminTestJSON
from tempest.api.compute.admin.test_hypervisor_negative import HypervisorAdminNegativeTestJSON
from tempest.api.compute.admin.test_quotas import QuotasAdminTestJSON
from tempest.api.compute.admin.test_quotas_negative import QuotasAdminNegativeTestJSON
from tempest.api.compute.admin.test_servers import ServersAdminTestJSON
from tempest.api.compute.admin.test_servers_negative import ServersAdminNegativeTestJSON
from tempest.api.compute.admin.test_services import ServicesAdminTestJSON
from tempest.api.compute.admin.test_services_negative import ServicesAdminNegativeTestJSON
from tempest.api.compute.admin.test_simple_tenant_usage import TenantUsagesTestJSON
from tempest.api.compute.admin.test_simple_tenant_usage_negative import TenantUsagesNegativeTestJSON
from tempest.common.utils import data_utils
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridAZAdminV2TestJSON(AZAdminV2TestJSON):
    """Tests Availability Zone API List"""

class HybridAZAdminNegativeTestJSON(AZAdminNegativeTestJSON):
    """Tests Availability Zone API List"""

class HybridHostsAdminTestJSON(HostsAdminTestJSON):
    """Tests hosts API using admin privileges."""

class HybridHostsAdminNegativeTestJSON(HostsAdminNegativeTestJSON):
    """Tests hosts API using admin privileges."""

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('e40c72b1-0239-4ed6-ba21-81a184df1f7c')
    def test_update_host_with_non_admin_user(self):
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.update_host,
                          hostname,
                          status='enable',
                          maintenance_mode='enable')

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('fbe2bf3e-3246-4a95-a59f-94e4e298ec77')
    def test_update_host_with_invalid_status(self):
        # 'status' can only be 'enable' or 'disable'
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.BadRequest,
                          self.client.update_host,
                          hostname,
                          status='invalid',
                          maintenance_mode='enable')

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('ab1e230e-5e22-41a9-8699-82b9947915d4')
    def test_update_host_with_invalid_maintenance_mode(self):
        # 'maintenance_mode' can only be 'enable' or 'disable'
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.BadRequest,
                          self.client.update_host,
                          hostname,
                          status='enable',
                          maintenance_mode='invalid')

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('0cd85f75-6992-4a4a-b1bd-d11e37fd0eee')
    def test_update_host_without_param(self):
        # 'status' or 'maintenance_mode' needed for host update
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.BadRequest,
                          self.client.update_host,
                          hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('23c92146-2100-4d68-b2d6-c7ade970c9c1')
    def test_update_nonexistent_host(self):
        nonexitent_hostname = data_utils.rand_name('rand_hostname')

        self.assertRaises(lib_exc.NotFound,
                          self.client.update_host,
                          nonexitent_hostname,
                          status='enable',
                          maintenance_mode='enable')

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('0d981ac3-4320-4898-b674-82b61fbb60e4')
    def test_startup_nonexistent_host(self):
        nonexitent_hostname = data_utils.rand_name('rand_hostname')

        self.assertRaises(lib_exc.NotFound,
                          self.client.startup_host,
                          nonexitent_hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('9f4ebb7e-b2ae-4e5b-a38f-0fd1bb0ddfca')
    def test_startup_host_with_non_admin_user(self):
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.startup_host,
                          hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('9e637444-29cf-4244-88c8-831ae82c31b6')
    def test_shutdown_nonexistent_host(self):
        nonexitent_hostname = data_utils.rand_name('rand_hostname')

        self.assertRaises(lib_exc.NotFound,
                          self.client.shutdown_host,
                          nonexitent_hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('a803529c-7e3f-4d3c-a7d6-8e1c203d27f6')
    def test_shutdown_host_with_non_admin_user(self):
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.shutdown_host,
                          hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('f86bfd7b-0b13-4849-ae29-0322e83ee58b')
    def test_reboot_nonexistent_host(self):
        nonexitent_hostname = data_utils.rand_name('rand_hostname')

        self.assertRaises(lib_exc.NotFound,
                          self.client.reboot_host,
                          nonexitent_hostname)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('02d79bb9-eb57-4612-abf6-2cb38897d2f8')
    def test_reboot_host_with_non_admin_user(self):
        hostname = self._get_host_name()

        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.reboot_host,
                          hostname)

class HybridHypervisorAdminTestJSON(HypervisorAdminTestJSON):
    """Tests Hypervisors API that require admin privileges"""

class HybridHypervisorAdminNegativeTestJSON(HypervisorAdminNegativeTestJSON):
    """Tests Hypervisors API that require admin privileges"""

class HybridQuotasAdminTestJSON(QuotasAdminTestJSON):
    """Test Quotas API that require admin privileges"""

class HybridQuotasAdminNegativeTestJSON(QuotasAdminNegativeTestJSON):
    """Test Quotas API that require admin privileges"""

class HybridServersAdminTestJSON(ServersAdminTestJSON):
    """Tests Servers API using admin privileges"""

    @classmethod
    def resource_setup(cls):
        super(ServersAdminTestJSON, cls).resource_setup()

        cls.s1_name = data_utils.rand_name('server')
        server = cls.create_test_server(name=cls.s1_name,
                                        wait_until='ACTIVE',
                                        availability_zone=CONF.compute.default_availability_zone)
        cls.s1_id = server['id']

        cls.s2_name = data_utils.rand_name('server')
        server = cls.create_test_server(name=cls.s2_name,
                                        wait_until='ACTIVE',
                                        availability_zone=CONF.compute.default_availability_zone)
        cls.s2_id = server['id']

    @test.idempotent_id('7a1323b4-a6a2-497a-96cb-76c07b945c71')
    def test_reset_network_inject_network_info(self):
        # Reset Network of a Server
        server = self.create_test_server(wait_until='ACTIVE', availability_zone=CONF.compute.default_availability_zone)
        self.client.reset_network(server['id'])
        # Inject the Network Info into Server
        self.client.inject_network_info(server['id'])

    @testtools.skip('Do not support host operation')
    @test.idempotent_id('fdcd9b33-0903-4e00-a1f7-b5f6543068d6')
    def test_create_server_with_scheduling_hint(self):
        # Create a server with scheduler hints.
        hints = {
            'same_host': self.s1_id
        }
        self.create_test_server(scheduler_hints=hints,
                                wait_until='ACTIVE')

class HybridServersAdminNegativeTestJSON(ServersAdminNegativeTestJSON):
    """Tests Servers API using admin privileges"""

    @classmethod
    def resource_setup(cls):
        super(ServersAdminTestJSON, cls).resource_setup()
        cls.tenant_id = cls.client.tenant_id

        cls.s1_name = data_utils.rand_name('server')
        server = cls.create_test_server(name=cls.s1_name,
                                        wait_until='ACTIVE',
                                        availability_zone=CONF.compute.default_availability_zone)
        cls.s1_id = server['id']

    @testtools.skip('Do not support host operation')
    @test.idempotent_id('28dcec23-f807-49da-822c-56a92ea3c687')
    @testtools.skipUnless(CONF.compute_feature_enabled.resize,
                          'Resize not available.')
    @test.attr(type=['negative'])
    def test_resize_server_using_overlimit_ram(self):
        # NOTE(mriedem): Avoid conflicts with os-quota-class-sets tests.
        self.useFixture(fixtures.LockFixture('compute_quotas'))
        flavor_name = data_utils.rand_name("flavor")
        flavor_id = self._get_unused_flavor_id()
        quota_set = (self.quotas_client.show_default_quota_set(self.tenant_id)
                     ['quota_set'])
        ram = int(quota_set['ram'])
        if ram == -1:
            raise self.skipException("default ram quota set is -1,"
                                     " cannot test overlimit")
        ram += 1
        vcpus = 8
        disk = 10
        flavor_ref = self.flavors_client.create_flavor(name=flavor_name,
                                                       ram=ram, vcpus=vcpus,
                                                       disk=disk,
                                                       id=flavor_id)['flavor']
        self.addCleanup(self.flavors_client.delete_flavor, flavor_id)
        self.assertRaises((lib_exc.Forbidden, lib_exc.OverLimit),
                          self.client.resize_server,
                          self.servers[0]['id'],
                          flavor_ref['id'])

    @testtools.skip('Do not support host operation')
    @test.idempotent_id('7368a427-2f26-4ad9-9ba9-911a0ec2b0db')
    @testtools.skipUnless(CONF.compute_feature_enabled.resize,
                          'Resize not available.')
    @test.attr(type=['negative'])
    def test_resize_server_using_overlimit_vcpus(self):
        # NOTE(mriedem): Avoid conflicts with os-quota-class-sets tests.
        self.useFixture(fixtures.LockFixture('compute_quotas'))
        flavor_name = data_utils.rand_name("flavor")
        flavor_id = self._get_unused_flavor_id()
        ram = 512
        quota_set = (self.quotas_client.show_default_quota_set(self.tenant_id)
                     ['quota_set'])
        vcpus = int(quota_set['cores'])
        if vcpus == -1:
            raise self.skipException("default cores quota set is -1,"
                                     " cannot test overlimit")
        vcpus += 1
        disk = 10
        flavor_ref = self.flavors_client.create_flavor(name=flavor_name,
                                                       ram=ram, vcpus=vcpus,
                                                       disk=disk,
                                                       id=flavor_id)['flavor']
        self.addCleanup(self.flavors_client.delete_flavor, flavor_id)
        self.assertRaises((lib_exc.Forbidden, lib_exc.OverLimit),
                          self.client.resize_server,
                          self.servers[0]['id'],
                          flavor_ref['id'])

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('e84e2234-60d2-42fa-8b30-e2d3049724ac')
    def test_get_server_diagnostics_by_non_admin(self):
        # Non-admin user can not view server diagnostics according to policy
        self.assertRaises(lib_exc.Forbidden,
                          self.non_adm_client.show_server_diagnostics,
                          self.s1_id)

    @testtools.skip('Do not support host operation')
    @test.attr(type=['negative'])
    @test.idempotent_id('46a4e1ca-87ae-4d28-987a-1b6b136a0221')
    def test_migrate_non_existent_server(self):
        # migrate a non existent server
        self.assertRaises(lib_exc.NotFound,
                          self.client.migrate_server,
                          str(uuid.uuid4()))

    @testtools.skip('Do not support host operation')
    @test.idempotent_id('b0b17f83-d14e-4fc4-8f31-bcc9f3cfa629')
    @testtools.skipUnless(CONF.compute_feature_enabled.resize,
                          'Resize not available.')
    @testtools.skipUnless(CONF.compute_feature_enabled.suspend,
                          'Suspend is not available.')
    @test.attr(type=['negative'])
    def test_migrate_server_invalid_state(self):
        # create server.
        server = self.create_test_server(wait_until='ACTIVE')
        server_id = server['id']
        # suspend the server.
        self.client.suspend_server(server_id)
        waiters.wait_for_server_status(self.client,
                                       server_id, 'SUSPENDED')
        # migrate a suspended server should fail
        self.assertRaises(lib_exc.Conflict,
                          self.client.migrate_server,
                          server_id)

class HybridServicesAdminTestJSON(ServicesAdminTestJSON):
    """Tests Services API. List and Enable/Disable require admin privileges."""

class HybridServicesAdminNegativeTestJSON(ServicesAdminNegativeTestJSON):
    """Tests Services API. List and Enable/Disable require admin privileges."""

class HybridTenantUsagesTestJSON(TenantUsagesTestJSON):
    """Tests TenantUsage API. require admin privileges."""

class HybridTenantUsagesNegativeTestJSON(TenantUsagesNegativeTestJSON):
    """Tests TenantUsage API. require admin privileges."""
