# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login_snapshot 1'] = {
    'login': {
        'errors': None,
        'success': True
    }
}

snapshots['test_logout_snapshot 1'] = {
    'logout': {
        'success': True
    }
}

snapshots['test_register_snapshot 1'] = {
    'register': {
        'errors': None,
        'success': True
    }
}

snapshots['test_register_snapshot 2'] = '[] Dear John, your account is created'

snapshots['test_activate_mutation_snapshot 1'] = {
    'activate': {
        'errors': None,
        'success': True
    }
}

snapshots['test_activate_mutation_snapshot 2'] = '[] Welcome John'
