#
# Copyright (c) 2015-2019 University of Antwerp, Aloxy NV.
#
# This file is part of pyd7a
# (see https://github.com/MOSAIC-LoPoW/pyd7a).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import unittest

from bitstring import ConstBitStream

from d7a.fs.file_permissions import FilePermissions


class TestPermission(unittest.TestCase):

  def test_parsing(self):
    permission_bytes = [
      0xFC
    ]

    permission = FilePermissions.parse(ConstBitStream(bytes=permission_bytes))

    self.assertEqual(permission.encrypted, True)
    self.assertEqual(permission.executable, True)
    self.assertEqual(permission.user_readable, True)
    self.assertEqual(permission.user_writeable, True)
    self.assertEqual(permission.user_executeable, True)
    self.assertEqual(permission.guest_readable, True)
    self.assertEqual(permission.guest_writeable, False)
    self.assertEqual(permission.guest_executeable, False)

  def test_byte_generation(self):
    p = FilePermissions(encrypted=True, executeable=True, user_readable=True, user_writeable=True, user_executeable=True,
                   guest_readable=True, guest_writeable=False, guest_executeable=False)
    bytes = bytearray(p)
    self.assertEqual(bytes, bytearray([0xFC]))