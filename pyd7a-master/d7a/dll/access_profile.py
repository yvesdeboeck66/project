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
from enum import Enum

from d7a.dll.sub_profile import SubProfile
from d7a.phy.channel_header import ChannelHeader
from d7a.phy.subband import SubBand
from d7a.support.schema           import Validatable, Types
from d7a.types.ct import CT


class CsmaCaMode(Enum):
  UNC = 0
  AIND = 1
  RAIND = 2
  RIGD = 3


class AccessProfile(Validatable):
  NUMBER_OF_SUB_PROFILES = 4
  MAX_NUMBER_OF_SUB_BANDS = 8

  # TODO update to D7AP v1.1
  SCHEMA = [{
    "channel_header": Types.OBJECT(ChannelHeader),
    "sub_profiles": Types.LIST(SubProfile, minlength=4, maxlength=4),
    "sub_bands": Types.LIST(SubBand, minlength=0, maxlength=8)
  }]

  def __init__(self, channel_header, sub_profiles, sub_bands):
    self.channel_header = channel_header
    self.sub_profiles = sub_profiles
    self.sub_bands = sub_bands
    super(AccessProfile, self).__init__()

  @staticmethod
  def parse(s):
    channel_header = ChannelHeader.parse(s)
    sub_profiles = []
    for _ in range(AccessProfile.NUMBER_OF_SUB_PROFILES):
      sub_profiles.append(SubProfile.parse(s))

    sub_bands = []
    for _ in range(AccessProfile.MAX_NUMBER_OF_SUB_BANDS):
      sub_bands.append(SubBand.parse(s))

    return AccessProfile(channel_header=channel_header,
                         sub_bands=sub_bands,
                         sub_profiles=sub_profiles
                         )

  def __iter__(self):
    for byte in self.channel_header: yield byte
    for sp in self.sub_profiles:
      for byte in sp: yield byte

    for sb in self.sub_bands:
      for byte in sb: yield byte

  def __str__(self):
    subprofiles_string = ""
    for subprofile in self.sub_profiles:
      subprofiles_string = subprofiles_string + str(subprofile)

    subbands_string = ""
    for subband in self.sub_bands:
      subbands_string = subbands_string + str(subband)

    return "channel_header={}, sub_profiles={}, sub_bands={}".format(
      self.channel_header,
      subprofiles_string,
      subbands_string
    )