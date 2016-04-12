import testtools
from oslo_log import log

from tempest.api.compute import base
from tempest.api.compute.flavors.test_absolute_limits import AbsoluteLimitsTestJSON
from tempest.api.compute.flavors.test_absolute_limits_negative import AbsoluteLimitsNegativeTestJSON
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest.lib import exceptions as lib_exc
from tempest.lib import decorators
from tempest import test
from tempest import config

CONF = config.CONF

LOG = log.getLogger(__name__)

class HybridAbsoluteLimitsTestJSON(AbsoluteLimitsTestJSON):
    """Test absolute limits"""

class HybridAbsoluteLimitsNegativeTestJSON(AbsoluteLimitsNegativeTestJSON):
    """Test absolute limits negative"""
