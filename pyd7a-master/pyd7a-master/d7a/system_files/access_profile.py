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
from d7a.dll.access_profile import AccessProfile
from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class AccessProfileFile(File, Validatable):
  SCHEMA = [{
    "access_specifier": Types.INTEGER(min=0, max=14),
    "access_profile": Types.OBJECT(AccessProfile, nullable=True)
  }]

  def __init__(self, access_specifier=0, access_profile=None):
    self.access_specifier = access_specifier
    self.access_profile = access_profile
    Validatable.__init__(self)
    File.__init__(self, SystemFileIds.ACCESS_PROFILE_0.value + access_specifier, 65)

  def __iter__(self):
    for byte in self.access_profile:
      yield byte

  @staticmethod
  def parse(s):
    return AccessProfileFile(access_specifier=0, access_profile=AccessProfile.parse(s)) # TODO access_specifier?

  def __str__(self):
    return "active_specifier={}, access_profile={}".format(self.access_specifier, self.access_profile)