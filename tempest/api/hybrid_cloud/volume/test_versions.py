
from oslo_log import log as logging

from tempest.api.hybrid_cloud.volume import base
from tempest import config
from tempest import test

CONF = config.CONF


LOG = logging.getLogger(__name__)

class TestVersions(base.BaseVolumeTest):

    def test_list_api_versions(self):
        """Test that a get of the unversioned url returns the choices doc.

        A key feature in OpenStack services is the idea that you can
        GET / on the service and get a list of the versioned endpoints
        that you can access. This comes back as a status 300
        request. It's important that this is available to API
        consumers to discover the API they can use.

        """
        result = self.base_versions_client.list_versions()
        versions = result['versions']
        # NOTE(sdague): at a later point we may want to loosen this
        # up, but for now this should be true of all Novas deployed.
        self.assertEqual(versions[0]['id'], 'v1.0',
                         "The first listed version should be v1.0")
	self.assertEqual(versions[1]['id'], 'v2.0',
                         "The second listed version should be v2.0")



    @test.idempotent_id('b953a29e-929c-4a8e-81be-ec3a7e03cb76')
    def test_get_version_details(self):
        """Test individual version endpoints info works.

        In addition to the GET / version request, there is also a
        version info document stored at the top of the versioned
        endpoints. This provides access to details about that
        endpoint, including min / max version if that implements
        microversions.

        This test starts with the version list, iterates all the
        returned endpoints, and fetches them. This will also ensure
        that all the version links are followable constructs which
        will help detect configuration issues when SSL termination
        isn't done completely for a site.

        """
        result = self.base_versions_client.list_versions()
        versions = result['versions']
        # iterate through all the versions that are returned and
        # attempt to get their version documents.
        for version in versions:
            links = [x for x in version['links'] if x['rel'] == 'self']
            self.assertEqual(
                len(links), 1,
                "There should only be 1 self link in %s" % version)
            link = links[0]
            # this is schema validated
            result = self.base_versions_client.get_version_by_url(link['href'])
            # ensure the new self link matches the old one
            newlinks = [x for x in result['version']['links']
                        if x['rel'] == 'self']
            self.assertEqual(links, newlinks)
