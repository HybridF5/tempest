import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.api.compute.flavors.test_flavors import FlavorsV2TestJSON
from tempest.api.compute.flavors.test_flavors_negative import FlavorsListWithDetailsNegativeTestJSON
from tempest.api.compute.flavors.test_flavors_negative import FlavorDetailsNegativeTestJSON
from tempest.common.utils import data_utils
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridFlavorsV2TestJSON(FlavorsV2TestJSON):
    """Test flavors"""

@test.SimpleNegativeAutoTest
class HybridFlavorsListWithDetailsNegativeTestJSON(FlavorsListWithDetailsNegativeTestJSON):
    """Test FlavorsListWithDetails"""

@test.SimpleNegativeAutoTest
class HybridFlavorDetailsNegativeTestJSON(FlavorDetailsNegativeTestJSON):
    """Test FlavorsListWithDetails"""