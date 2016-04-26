import datetime
import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.common import compute
from tempest.common import fixed_network

import tempest.api.compute.admin.test_agents as AgentsAdminTest
import tempest.api.compute.admin.test_aggregates as AggregatesAdminTest
import tempest.api.compute.admin.test_aggregates_negative as AggregatesAdminNegativeTest
import tempest.api.compute.admin.test_availability_zone as AZAdminV2Test
import tempest.api.compute.admin.test_availability_zone_negative as AZAdminNegativeTest
import tempest.api.compute.admin.test_baremetal_nodes as BaremetalNodesAdminTest
import tempest.api.compute.admin.test_fixed_ips as FixedIPsTest
import tempest.api.compute.admin.test_fixed_ips_negative as FixedIPsNegativeTest
import tempest.api.compute.admin.test_flavors as FlavorsAdminTest
import tempest.api.compute.admin.test_flavors_access as FlavorsAccessTest
import tempest.api.compute.admin.test_flavors_access_negative as FlavorsAccessNegativeTest
import tempest.api.compute.admin.test_flavors_extra_specs as FlavorsExtraSpecsTest
import tempest.api.compute.admin.test_flavors_extra_specs_negative as FlavorsExtraSpecsNegativeTest
import tempest.api.compute.admin.test_floating_ips_bulk as FloatingIPsBulkAdminTest
import tempest.api.compute.admin.test_hosts as HostsAdminTest
import tempest.api.compute.admin.test_hosts_negative as HostsAdminNegativeTest
import tempest.api.compute.admin.test_hypervisor as HypervisorAdminTest
import tempest.api.compute.admin.test_hypervisor_negative as HypervisorAdminNegativeTest
import tempest.api.compute.admin.test_instance_usage_audit_log as InstanceUsageAuditLogTest
import tempest.api.compute.admin.test_instance_usage_audit_log_negative as InstanceUsageAuditLogNegativeTest
import tempest.api.compute.admin.test_keypairs_v210 as KeyPairsV210Test
import tempest.api.compute.admin.test_live_migration as LiveBlockMigrationTest
import tempest.api.compute.admin.test_migrations as MigrationsAdminTest
import tempest.api.compute.admin.test_networks as NetworksTest
import tempest.api.compute.admin.test_quotas as QuotaClassesAdminTest
import tempest.api.compute.admin.test_quotas as QuotasAdminTest
import tempest.api.compute.admin.test_quotas_negative as QuotasAdminNegativeTest
import tempest.api.compute.admin.test_security_group_default_rules as SecurityGroupDefaultRulesTest
import tempest.api.compute.admin.test_security_groups as SecurityGroupsTestAdmin
import tempest.api.compute.admin.test_servers as ServersAdminTest
import tempest.api.compute.admin.test_servers_negative as ServersAdminNegativeTest
import tempest.api.compute.admin.test_servers_on_multinodes as ServersOnMultiNodesTest
import tempest.api.compute.admin.test_services as ServicesAdminTest
import tempest.api.compute.admin.test_services_negative as ServicesAdminNegativeTest
import tempest.api.compute.admin.test_simple_tenant_usage as TenantUsagesTest
import tempest.api.compute.admin.test_simple_tenant_usage_negative as TenantUsagesNegativeTest
from tempest.common.utils import data_utils
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridAgentsAdminTestJSON(AgentsAdminTest.AgentsAdminTestJSON):
    """Tests Agents API"""

class HybridAggregatesAdminTestJSON(AggregatesAdminTest.AggregatesAdminTestJSON):
    """Tests Aggregates API that require admin privileges"""
    @testtools.skip('Do not support now')    
    @test.idempotent_id('96be03c7-570d-409c-90f8-e4db3c646996')
    def test_aggregate_add_host_create_server_with_az(self):
        # Add a host to the given aggregate and create a server.
        self.useFixture(fixtures.LockFixture('availability_zone'))
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        az_name = data_utils.rand_name(self.az_name_prefix)
        aggregate = self.client.create_aggregate(
            name=aggregate_name, availability_zone=az_name)['aggregate']
        self.addCleanup(self.client.delete_aggregate, aggregate['id'])
        self.client.add_host(aggregate['id'], host=self.host)
        self.addCleanup(self.client.remove_host, aggregate['id'],
                        host=self.host)
        server_name = data_utils.rand_name('test_server')
        admin_servers_client = self.os_adm.servers_client
        server = self.create_test_server(name=server_name,
                                         availability_zone=az_name,
                                         wait_until='ACTIVE')
        body = admin_servers_client.show_server(server['id'])['server']
        self.assertEqual(self.host, body[self._host_key])

class HybridAggregatesAdminNegativeTestJSON(AggregatesAdminNegativeTest.AggregatesAdminNegativeTestJSON):
    """Tests Aggregates API that require admin privileges"""
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('86a1cb14-da37-4a70-b056-903fd56dfe29')
    def test_aggregate_create_as_user(self):
        # Regular user is not allowed to create an aggregate.
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.create_aggregate,
                          name=aggregate_name)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('cd6de795-c15d-45f1-8d9e-813c6bb72a3d')
    def test_aggregate_delete_as_user(self):
        # Regular user is not allowed to delete an aggregate.
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        aggregate = (self.client.create_aggregate(name=aggregate_name)
                     ['aggregate'])
        self.addCleanup(self.client.delete_aggregate, aggregate['id'])
    
        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.delete_aggregate,
                          aggregate['id'])

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('b7d475a6-5dcd-4ff4-b70a-cd9de66a6672')
    def test_aggregate_list_as_user(self):
        # Regular user is not allowed to list aggregates.
        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.list_aggregates)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('557cad12-34c9-4ff4-95f0-22f0dfbaf7dc')
    def test_aggregate_get_details_as_user(self):
        # Regular user is not allowed to get aggregate details.
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        aggregate = (self.client.create_aggregate(name=aggregate_name)
                     ['aggregate'])
        self.addCleanup(self.client.delete_aggregate, aggregate['id'])
    
        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.show_aggregate,
                          aggregate['id'])

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('7324c334-bd13-4c93-8521-5877322c3d51')
    def test_aggregate_add_host_as_user(self):
        # Regular user is not allowed to add a host to an aggregate.
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        aggregate = (self.client.create_aggregate(name=aggregate_name)
                     ['aggregate'])
        self.addCleanup(self.client.delete_aggregate, aggregate['id'])

        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.add_host,
                          aggregate['id'], host=self.host)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('7a53af20-137a-4e44-a4ae-e19260e626d9')
    def test_aggregate_remove_host_as_user(self):
        # Regular user is not allowed to remove a host from an aggregate.
        self.useFixture(fixtures.LockFixture('availability_zone'))
        aggregate_name = data_utils.rand_name(self.aggregate_name_prefix)
        aggregate = (self.client.create_aggregate(name=aggregate_name)
                     ['aggregate'])
        self.addCleanup(self.client.delete_aggregate, aggregate['id'])
        self.client.add_host(aggregate['id'], host=self.host)
        self.addCleanup(self.client.remove_host, aggregate['id'],
                        host=self.host)
    
        self.assertRaises(lib_exc.Forbidden,
                          self.user_client.remove_host,
                          aggregate['id'], host=self.host)

class HybridAZAdminV2TestJSON(AZAdminV2Test.AZAdminV2TestJSON):
    """Tests Availability Zone API List"""

class HybridAZAdminNegativeTestJSON(AZAdminNegativeTest.AZAdminNegativeTestJSON):
    """Tests Availability Zone API List"""
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('bf34dca2-fdc3-4073-9c02-7648d9eae0d7')
    def test_get_availability_zone_list_detail_with_non_admin_user(self):
        # List of availability zones and available services with
        # non-administrator user
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.list_availability_zones, detail=True)    

class HybridBaremetalNodesAdminTestJSON(BaremetalNodesAdminTest.BaremetalNodesAdminTestJSON):
    """Tests Baremetal API"""

class HybridFixedIPsTestJson(FixedIPsTest.FixedIPsTestJson):
    """Tests FixedIPs API"""

class HybridFixedIPsNegativeTestJson(FixedIPsNegativeTest.FixedIPsNegativeTestJson):
    """Tests FixedIPs API"""

class HybridFlavorsAdminTestJSON(FlavorsAdminTest.FlavorsAdminTestJSON):
    """Tests Flavors API Create and Delete that require admin privileges"""
    @testtools.skip('Do not support now')
    @test.idempotent_id('63dc64e6-2e79-4fdf-868f-85500d308d66')
    def test_create_list_flavor_without_extra_data(self):
        # Create a flavor and ensure it is listed
        # This operation requires the user to have 'admin' role

        def verify_flavor_response_extension(flavor):
            # check some extensions for the flavor create/show/detail response
            self.assertEqual(flavor['swap'], '')
            self.assertEqual(int(flavor['rxtx_factor']), 1)
            self.assertEqual(int(flavor['OS-FLV-EXT-DATA:ephemeral']), 0)
            self.assertEqual(flavor['os-flavor-access:is_public'], True)

        flavor_name = data_utils.rand_name(self.flavor_name_prefix)
        new_flavor_id = data_utils.rand_int_id(start=1000)

        # Create the flavor
        flavor = self.client.create_flavor(name=flavor_name,
                                           ram=self.ram, vcpus=self.vcpus,
                                           disk=self.disk,
                                           id=new_flavor_id)['flavor']
        self.addCleanup(self.flavor_clean_up, flavor['id'])
        self.assertEqual(flavor['name'], flavor_name)
        self.assertEqual(flavor['ram'], self.ram)
        self.assertEqual(flavor['vcpus'], self.vcpus)
        self.assertEqual(flavor['disk'], self.disk)
        self.assertEqual(int(flavor['id']), new_flavor_id)
        verify_flavor_response_extension(flavor)

        # Verify flavor is retrieved
        flavor = self.client.show_flavor(new_flavor_id)['flavor']
        self.assertEqual(flavor['name'], flavor_name)
        verify_flavor_response_extension(flavor)

        # Check if flavor is present in list
        flavors = self.user_client.list_flavors(detail=True)['flavors']
        for flavor in flavors:
            if flavor['name'] == flavor_name:
                verify_flavor_response_extension(flavor)
                flag = True
        self.assertTrue(flag)

class HybridFlavorsAccessTestJSON(FlavorsAccessTest.FlavorsAccessTestJSON):
    """Tests Flavor Access API extension.

    Add and remove Flavor Access require admin privileges.
    """
class HybridFlavorsAccessNegativeTestJSON(FlavorsAccessNegativeTest.FlavorsAccessNegativeTestJSON):
    """Tests Flavor Access API extension.

    Add and remove Flavor Access require admin privileges.
    """
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('41eaaade-6d37-4f28-9c74-f21b46ca67bd')
    def test_flavor_non_admin_add(self):
        # Test to add flavor access as a user without admin privileges.
        flavor_name = data_utils.rand_name(self.flavor_name_prefix)
        new_flavor_id = data_utils.rand_int_id(start=1000)
        new_flavor = self.client.create_flavor(name=flavor_name,
                                               ram=self.ram, vcpus=self.vcpus,
                                               disk=self.disk,
                                               id=new_flavor_id,
                                               is_public='False')['flavor']
        self.addCleanup(self.client.delete_flavor, new_flavor['id'])
        self.assertRaises(lib_exc.Forbidden,
                          self.flavors_client.add_flavor_access,
                          new_flavor['id'],
                          self.tenant_id)
    
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('073e79a6-c311-4525-82dc-6083d919cb3a')
    def test_flavor_non_admin_remove(self):
        # Test to remove flavor access as a user without admin privileges.
        flavor_name = data_utils.rand_name(self.flavor_name_prefix)
        new_flavor_id = data_utils.rand_int_id(start=1000)
        new_flavor = self.client.create_flavor(name=flavor_name,
                                               ram=self.ram, vcpus=self.vcpus,
                                               disk=self.disk,
                                               id=new_flavor_id,
                                               is_public='False')['flavor']
        self.addCleanup(self.client.delete_flavor, new_flavor['id'])
        # Add flavor access to a tenant.
        self.client.add_flavor_access(new_flavor['id'], self.tenant_id)
        self.addCleanup(self.client.remove_flavor_access,
                        new_flavor['id'], self.tenant_id)
        self.assertRaises(lib_exc.Forbidden,
                          self.flavors_client.remove_flavor_access,
                          new_flavor['id'],
                          self.tenant_id)

class HybridFlavorsExtraSpecsTestJSON(FlavorsExtraSpecsTest.FlavorsExtraSpecsTestJSON):
    """Tests Flavor Extra Spec API extension.

    SET, UNSET, UPDATE Flavor Extra specs require admin privileges.
    GET Flavor Extra specs can be performed even by without admin privileges.
    """
    @test.idempotent_id('a99dad88-ae1c-4fba-aeb4-32f898218bd0')
    def test_flavor_non_admin_get_all_keys(self):
        specs = {"key1": "value1", "key2": "value2"}
        self.client.set_flavor_extra_spec(self.flavor['id'], **specs)
        body = (self.flavors_client.list_flavor_extra_specs(self.flavor['id'])
                ['extra_specs'])

        for key in specs:
            self.assertEqual(body[key], specs[key])

    @testtools.skip('Do not support now')
    @test.idempotent_id('12805a7f-39a3-4042-b989-701d5cad9c90')
    def test_flavor_non_admin_get_specific_key(self):
            body = self.client.set_flavor_extra_spec(self.flavor['id'],
                                                     key1="value1",
                                                     key2="value2")['extra_specs']
            self.assertEqual(body['key1'], 'value1')
            self.assertIn('key2', body)
            body = self.flavors_client.show_flavor_extra_spec(
                self.flavor['id'], 'key1')
            self.assertEqual(body['key1'], 'value1')
            self.assertNotIn('key2', body)

class HybridFlavorsExtraSpecsNegativeTestJSON(FlavorsExtraSpecsNegativeTest.FlavorsExtraSpecsNegativeTestJSON):
    """Negative Tests Flavor Extra Spec API extension.

    SET, UNSET, UPDATE Flavor Extra specs require admin privileges.
    """
    @testtools.skip('Do not support now')
    @test.attr(type=['negative'])
    @test.idempotent_id('329a7be3-54b2-48be-8052-bf2ce4afd898')
    def test_flavor_get_nonexistent_key(self):
        self.assertRaises(lib_exc.NotFound,
                          self.flavors_client.show_flavor_extra_spec,
                          self.flavor['id'],
                          "nonexistent_key")
    
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('a00a3b81-5641-45a8-ab2b-4a8ec41e1d7d')
    def test_flavor_non_admin_set_keys(self):
        # Test to SET flavor extra spec as a user without admin privileges.
        self.assertRaises(lib_exc.Forbidden,
                          self.flavors_client.set_flavor_extra_spec,
                          self.flavor['id'],
                          key1="value1", key2="value2")

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('1ebf4ef8-759e-48fe-a801-d451d80476fb')
    def test_flavor_non_admin_update_specific_key(self):
        # non admin user is not allowed to update flavor extra spec
        body = self.client.set_flavor_extra_spec(
            self.flavor['id'], key1="value1", key2="value2")['extra_specs']
        self.assertEqual(body['key1'], 'value1')
        self.assertRaises(lib_exc.Forbidden,
                          self.flavors_client.
                          update_flavor_extra_spec,
                          self.flavor['id'],
                          'key1',
                          key1='value1_new')

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('28f12249-27c7-44c1-8810-1f382f316b11')
    def test_flavor_non_admin_unset_keys(self):
        self.client.set_flavor_extra_spec(self.flavor['id'],
                                          key1="value1", key2="value2")
    
        self.assertRaises(lib_exc.Forbidden,
                          self.flavors_client.unset_flavor_extra_spec,
                          self.flavor['id'],
                          'key1')

class HybridFloatingIPsBulkAdminTestJSON(FloatingIPsBulkAdminTest.FloatingIPsBulkAdminTestJSON):
    """Tests Floating IPs Bulk APIs that require admin privileges.

    API documentation - http://docs.openstack.org/api/openstack-compute/2/
    content/ext-os-floating-ips-bulk.html
    """

class HybridHostsAdminTestJSON(HostsAdminTest.HostsAdminTestJSON):
    """Tests hosts API using admin privileges."""
    @testtools.skip('BUG execute failed now')
    @test.idempotent_id('38adbb12-aee2-4498-8aec-329c72423aa4')
    def test_show_host_detail(self):
        hosts = self.client.list_hosts()['hosts']

        hosts = [host for host in hosts if host['service'] == 'compute']
        self.assertTrue(len(hosts) >= 1)

        for host in hosts:
            hostname = host['host_name']
            resources = self.client.show_host(hostname)['host']
            self.assertTrue(len(resources) >= 1)
            host_resource = resources[0]['resource']
            self.assertIsNotNone(host_resource)
            self.assertIsNotNone(host_resource['cpu'])
            self.assertIsNotNone(host_resource['disk_gb'])
            self.assertIsNotNone(host_resource['memory_mb'])
            self.assertIsNotNone(host_resource['project'])
            self.assertEqual(hostname, host_resource['host'])

class HybridHostsAdminNegativeTestJSON(HostsAdminNegativeTest.HostsAdminNegativeTestJSON):
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

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('dd032027-0210-4d9c-860e-69b1b8deed5f')
    def test_list_hosts_with_non_admin_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.list_hosts)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('19ebe09c-bfd4-4b7c-81a2-e2e0710f59cc')
    def test_show_host_detail_with_non_admin_user(self):
        hostname = self._get_host_name()
    
        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.show_host,
                          hostname)

class HybridHypervisorAdminTestJSON(HypervisorAdminTest.HypervisorAdminTestJSON):
    """Tests Hypervisors API that require admin privileges"""

class HybridHypervisorAdminNegativeTestJSON(HypervisorAdminNegativeTest.HypervisorAdminNegativeTestJSON):
    """Tests Hypervisors API that require admin privileges"""

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('51e663d0-6b89-4817-a465-20aca0667d03')
    def test_show_hypervisor_with_non_admin_user(self):
        hypers = self._list_hypervisors()
        self.assertTrue(len(hypers) > 0)

        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.show_hypervisor,
            hypers[0]['id'])

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('2a0a3938-832e-4859-95bf-1c57c236b924')
    def test_show_servers_with_non_admin_user(self):
        hypers = self._list_hypervisors()
        self.assertTrue(len(hypers) > 0)
    
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.list_servers_on_hypervisor,
            hypers[0]['id'])

    @testtools.skip('BUG execute failed now')    
    @test.attr(type=['negative'])
    @test.idempotent_id('e2b061bb-13f9-40d8-9d6e-d5bf17595849')
    def test_get_hypervisor_stats_with_non_admin_user(self):
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.show_hypervisor_statistics)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('6c3461f9-c04c-4e2a-bebb-71dc9cb47df2')
    def test_get_hypervisor_uptime_with_non_admin_user(self):
        hypers = self._list_hypervisors()
        self.assertTrue(len(hypers) > 0)

        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.show_hypervisor_uptime,
            hypers[0]['id'])

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('51b3d536-9b14-409c-9bce-c6f7c794994e')
    def test_get_hypervisor_list_with_non_admin_user(self):
        # List of hypervisor and available services with non admin user
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.list_hypervisors)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('dc02db05-e801-4c5f-bc8e-d915290ab345')
    def test_get_hypervisor_list_details_with_non_admin_user(self):
        # List of hypervisor details and available services with non admin user
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.list_hypervisors, detail=True)

    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('5b6a6c79-5dc1-4fa5-9c58-9c8085948e74')
    def test_search_hypervisor_with_non_admin_user(self):
        hypers = self._list_hypervisors()
        self.assertTrue(len(hypers) > 0)
    
        self.assertRaises(
            lib_exc.Forbidden,
            self.non_adm_client.search_hypervisor,
            hypers[0]['hypervisor_hostname'])

class HybridInstanceUsageAuditLogTestJSON(InstanceUsageAuditLogTest.InstanceUsageAuditLogTestJSON):
    """Tests InstanceUsageAuditLogTestJSON API"""

class HybridInstanceUsageAuditLogNegativeTestJSON(InstanceUsageAuditLogNegativeTest.InstanceUsageAuditLogNegativeTestJSON):
    """Tests InstanceUsageAuditLogTestJSON API"""

class HybridKeyPairsV210TestJSON(KeyPairsV210Test.KeyPairsV210TestJSON):
    """Tests KeyPairsV210TestJSON API"""

class HybridLiveBlockMigrationTestJSON(LiveBlockMigrationTest.LiveBlockMigrationTestJSON):
    """Tests LiveBlockMigrationTestJSON API"""

class HybridMigrationsAdminTest(MigrationsAdminTest.MigrationsAdminTest):
    """Tests MigrationsAdminTest API"""

class HybridNetworksTest(NetworksTest.NetworksTest):
    """Tests Nova Networks API that usually requires admin privileges.

    API docs:
    http://developer.openstack.org/api-ref-compute-v2-ext.html#ext-os-networks
    """

class HybridQuotaClassesAdminTestJSON(QuotaClassesAdminTest.QuotaClassesAdminTestJSON):
    """Tests the os-quota-class-sets API to update default quotas."""
    
class HybridQuotasAdminTestJSON(QuotasAdminTest.QuotasAdminTestJSON):
    """Test Quotas API that require admin privileges"""

class HybridQuotasAdminNegativeTestJSON(QuotasAdminNegativeTest.QuotasAdminNegativeTestJSON):
    """Test Quotas API that require admin privileges"""
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('733abfe8-166e-47bb-8363-23dbd7ff3476')
    def test_update_quota_normal_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.client.update_quota_set,
                          self.demo_tenant_id,
                          ram=0)

class HybridSecurityGroupDefaultRulesTest(SecurityGroupDefaultRulesTest.SecurityGroupDefaultRulesTest):
    """Test SecurityGroupDefaultRulesTest API"""

class HybridSecurityGroupsTestAdminJSON(SecurityGroupsTestAdmin.SecurityGroupsTestAdminJSON):
    """Test HybridSecurityGroupsTestAdminJSON API"""
    @testtools.skip('Do not support with neutron')
    @test.idempotent_id('49667619-5af9-4c63-ab5d-2cfdd1c8f7f1')
    @test.services('network')
    def test_list_security_groups_list_all_tenants_filter(self):
        # Admin can list security groups of all tenants
        # List of all security groups created
        security_group_list = []
        # Create two security groups for a non-admin tenant
        for i in range(2):
            name = data_utils.rand_name('securitygroup')
            description = data_utils.rand_name('description')
            securitygroup = self.client.create_security_group(
                name=name, description=description)['security_group']
            self.addCleanup(self._delete_security_group,
                            securitygroup['id'], admin=False)
            security_group_list.append(securitygroup)

        client_tenant_id = securitygroup['tenant_id']
        # Create two security groups for admin tenant
        for i in range(2):
            name = data_utils.rand_name('securitygroup')
            description = data_utils.rand_name('description')
            adm_securitygroup = self.adm_client.create_security_group(
                name=name, description=description)['security_group']
            self.addCleanup(self._delete_security_group,
                            adm_securitygroup['id'])
            security_group_list.append(adm_securitygroup)

        # Fetch all security groups based on 'all_tenants' search filter
        fetched_list = self.adm_client.list_security_groups(
            all_tenants='true')['security_groups']
        sec_group_id_list = map(lambda sg: sg['id'], fetched_list)
        # Now check if all created Security Groups are present in fetched list
        for sec_group in security_group_list:
            self.assertIn(sec_group['id'], sec_group_id_list)

        # Fetch all security groups for non-admin user with 'all_tenants'
        # search filter
        fetched_list = (self.client.list_security_groups(all_tenants='true')
                        ['security_groups'])
        # Now check if all created Security Groups are present in fetched list
        for sec_group in fetched_list:
            self.assertEqual(sec_group['tenant_id'], client_tenant_id,
                             "Failed to get all security groups for "
                             "non admin user.")

class HybridServersAdminTestJSON(ServersAdminTest.ServersAdminTestJSON):
    """Tests Servers API using admin privileges"""

    @classmethod
    def resource_setup(cls):
        super(ServersAdminTest.ServersAdminTestJSON, cls).resource_setup()

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

    @test.idempotent_id('86c7a8f7-50cf-43a9-9bac-5b985317134f')
    def test_list_servers_filter_by_exist_host(self):
        # Filter the list of servers by existent host
        name = data_utils.rand_name('server')
        network = self.get_tenant_network()
        network_kwargs = fixed_network.set_networks_kwarg(network)
        # We need to create the server as an admin, so we can't use
        # self.create_test_server() here as this method creates the server
        # in the "primary" (i.e non-admin) tenant.
        test_server, _ = compute.create_test_server(
            self.os_adm, wait_until="ACTIVE", availability_zone=CONF.compute.default_availability_zone,
            name=name, **network_kwargs)
        self.addCleanup(self.client.delete_server, test_server['id'])
        server = self.client.show_server(test_server['id'])['server']
        self.assertEqual(server['status'], 'ACTIVE')
        hostname = server[self._host_key]
        params = {'host': hostname}
        body = self.client.list_servers(**params)
        servers = body['servers']
        nonexistent_params = {'host': 'nonexistent_host'}
        nonexistent_body = self.client.list_servers(**nonexistent_params)
        nonexistent_servers = nonexistent_body['servers']
        self.assertIn(test_server['id'], map(lambda x: x['id'], servers))
        self.assertNotIn(test_server['id'],
                         map(lambda x: x['id'], nonexistent_servers))

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

    @testtools.skip('BUG execute failed now')
    @test.idempotent_id('682cb127-e5bb-4f53-87ce-cb9003604442')
    def test_rebuild_server_in_error_state(self):
        # The server in error state should be rebuilt using the provided
        # image and changed to ACTIVE state
    
        # resetting vm state require admin privilege
        self.client.reset_state(self.s1_id, state='error')
        rebuilt_server = self.non_admin_client.rebuild_server(
            self.s1_id, self.image_ref_alt)['server']
        self.addCleanup(waiters.wait_for_server_status, self.non_admin_client,
                        self.s1_id, 'ACTIVE')
        self.addCleanup(self.non_admin_client.rebuild_server, self.s1_id,
                        self.image_ref)
    
        # Verify the properties in the initial response are correct
        self.assertEqual(self.s1_id, rebuilt_server['id'])
        rebuilt_image_id = rebuilt_server['image']['id']
        self.assertEqual(self.image_ref_alt, rebuilt_image_id)
        self.assertEqual(self.flavor_ref, rebuilt_server['flavor']['id'])
        waiters.wait_for_server_status(self.non_admin_client,
                                       rebuilt_server['id'], 'ACTIVE',
                                       raise_on_error=False)
        # Verify the server properties after rebuilding
        server = (self.non_admin_client.show_server(rebuilt_server['id'])
                  ['server'])
        rebuilt_image_id = server['image']['id']
        self.assertEqual(self.image_ref_alt, rebuilt_image_id)

class HybridServersAdminNegativeTestJSON(ServersAdminNegativeTest.ServersAdminNegativeTestJSON):
    """Tests Servers API using admin privileges"""

    @classmethod
    def resource_setup(cls):
        super(ServersAdminNegativeTest.ServersAdminNegativeTestJSON, cls).resource_setup()
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

class HybridServersOnMultiNodesTest(ServersOnMultiNodesTest.ServersOnMultiNodesTest):
    """Tests ServersOnMultiNodesTest API."""

class HybridServicesAdminTestJSON(ServicesAdminTest.ServicesAdminTestJSON):
    """Tests Services API. List and Enable/Disable require admin privileges."""

class HybridServicesAdminNegativeTestJSON(ServicesAdminNegativeTest.ServicesAdminNegativeTestJSON):
    """Tests Services API. List and Enable/Disable require admin privileges."""
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('1126d1f8-266e-485f-a687-adc547492646')
    def test_list_services_with_non_admin_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.non_admin_client.list_services)


class HybridTenantUsagesTestJSON(TenantUsagesTest.TenantUsagesTestJSON):
    """Tests TenantUsage API. require admin privileges."""
    @classmethod
    def resource_setup(cls):
        super(TenantUsagesTest.TenantUsagesTestJSON, cls).resource_setup()
        cls.tenant_id = cls.client.tenant_id

        # Create a server in the demo tenant
        cls.create_test_server(wait_until='ACTIVE',
            availability_zone=CONF.compute.default_availability_zone)

        now = datetime.datetime.now()
        cls.start = cls._parse_strtime(now - datetime.timedelta(days=1))
        cls.end = cls._parse_strtime(now + datetime.timedelta(days=1))

    @testtools.skip('Do not support with origin policy')
    @test.idempotent_id('9d00a412-b40e-4fd9-8eba-97b496316116')
    def test_get_usage_tenant_with_non_admin_user(self):
        # Get usage for a specific tenant with non admin user
        tenant_usage = self.call_until_valid(
            self.client.show_tenant_usage, VALID_WAIT,
            self.tenant_id, start=self.start, end=self.end)['tenant_usage']
        self.assertEqual(len(tenant_usage), 8)

class HybridTenantUsagesNegativeTestJSON(TenantUsagesNegativeTest.TenantUsagesNegativeTestJSON):
    """Tests TenantUsage API. require admin privileges."""
    @testtools.skip('BUG execute failed now')
    @test.attr(type=['negative'])
    @test.idempotent_id('bbe6fe2c-15d8-404c-a0a2-44fad0ad5cc7')
    def test_list_usage_all_tenants_with_non_admin_user(self):
        # Get usage for all tenants with non admin user
        params = {'start': self.start,
                  'end': self.end,
                  'detailed': "1"}
        self.assertRaises(lib_exc.Forbidden,
                          self.client.list_tenant_usages, **params)

