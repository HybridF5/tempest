import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.api.compute.flavors.test_keypairs import KeyPairsV2TestJSON
from tempest.api.compute.flavors.test_keypairs_negative import KeyPairsNegativeTestJSON
from tempest.api.compute.flavors.test_keypairs_v22 import KeyPairsV22TestJSON
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridKeyPairsV2TestJSON(KeyPairsV2TestJSON):
    """Test Keypairs v2"""

class HybridKeyPairsNegativeTestJSON(KeyPairsNegativeTestJSON):
    """Test Keypairs negative"""

class HybridKeyPairsV22TestJSON(KeyPairsV22TestJSON):
    """Test Keypairs v22"""