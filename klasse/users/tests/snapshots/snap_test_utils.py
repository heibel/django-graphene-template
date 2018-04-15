# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_send_activation_email 1'] = '''Dear John,

    Your account has been created for the site , and is
    available at /secret.

    See you there soon!


    The awesome  team'''

snapshots['test_send_welcome_email 1'] = '''Dear John,

    Welcome!

    The awesome  team'''

snapshots['test_send_password_reset_email 1'] = '''Dear John,

    Password reset!

    The awesome  team'''
