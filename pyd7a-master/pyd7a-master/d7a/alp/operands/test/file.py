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

# author: Christophe VG <contact@christophe.vg>
# unit tests for the D7 File {*} Operands

import unittest

from d7a.alp.operands.file import Data
from d7a.alp.operands.test.offset import TestOffset


class TestData(unittest.TestCase):
  def test_default_data_constructor(self):
    Data()

  def test_data_bad_offset(self):
    def bad(): Data(Data())
    self.assertRaises(ValueError, bad)

  def test_data_length(self):
    d = Data(data=[0xd7, 0x04, 0x00])
    self.assertEqual(d.length.value, 3)
    self.assertEqual(len(d),   3)

  def test_byte_generation(self):
    bytes = bytearray(Data())
    self.assertEqual(len(bytes), 3)
    self.assertEqual(bytes[0], int('00000000', 2)) # offset
    self.assertEqual(bytes[1], int('00000000', 2)) # offset
    self.assertEqual(bytes[2], int('00000000', 2))

    bytes = bytearray(Data(data=[0x01,0x02,0x03,0x04]))
    self.assertEqual(len(bytes), 7)
    self.assertEqual(bytes[0], int('00000000', 2)) # offset
    self.assertEqual(bytes[1], int('00000000', 2)) # offset
    self.assertEqual(bytes[2], int('00000100', 2)) # length = 4
    self.assertEqual(bytes[3], int('00000001', 2))
    self.assertEqual(bytes[4], int('00000010', 2))
    self.assertEqual(bytes[5], int('00000011', 2))
    self.assertEqual(bytes[6], int('00000100', 2))
    
if __name__ == '__main__':
  for case in [TestOffset, TestData]:
    suite = unittest.TestLoader().loadTestsFromTestCase(case)
    unittest.TextTestRunner(verbosity=2).run(suite)
