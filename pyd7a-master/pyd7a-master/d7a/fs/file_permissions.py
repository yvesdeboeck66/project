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
from d7a.support.schema import Validatable, Types


class FilePermissions(Validatable):
  SCHEMA = [{
    "encrypted": Types.BOOLEAN(),
    "executable": Types.BOOLEAN(),
    "user_readable": Types.BOOLEAN(),
    "user_writable": Types.BOOLEAN(),
    "user_executable": Types.BOOLEAN(),
    "guest_readable": Types.BOOLEAN(),
    "guest_writable": Types.BOOLEAN(),
    "guest_executable": Types.BOOLEAN()
  }]

  def __init__(self, encrypted=False, executeable=False, user_readable=True, user_writeable=True, user_executeable=True,
               guest_readable= True, guest_writeable=True, guest_executeable=True):
    self.encrypted = encrypted
    self.executable = executeable
    self.user_readable = user_readable
    self.user_writeable = user_writeable
    self.user_executeable = user_executeable
    self.guest_readable = guest_readable
    self.guest_writeable = guest_writeable
    self.guest_executeable = guest_executeable

    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    encrypted = s.read("bool")
    executeable = s.read("bool")
    user_readable = s.read("bool")
    user_writeable = s.read("bool")
    user_executable = s.read("bool")
    guest_readable = s.read("bool")
    guest_writeable = s.read("bool")
    guest_executable = s.read("bool")
    return FilePermissions(encrypted=encrypted, executeable=executeable, user_readable=user_readable,
                      user_writeable=user_writeable, user_executeable=user_executable,
                      guest_readable=guest_readable, guest_writeable=guest_writeable, guest_executeable=guest_executable)

  def __iter__(self):
    byte = 0
    if self.encrypted: byte += 1 << 7
    if self.executable: byte += 1 << 6
    if self.user_readable: byte += 1 << 5
    if self.user_writeable: byte += 1 << 4
    if self.user_executeable: byte += 1 << 3
    if self.guest_readable: byte += 1 << 2
    if self.guest_writeable: byte += 1 << 1
    if self.guest_executeable: byte += 1
    yield byte

  def __str__(self):
    return "" #TODO

  def __eq__(self, other):
    if isinstance(other, FilePermissions):
      return self.__dict__ == other.__dict__

    return False

  def __ne__(self, other):
    return not self.__eq__(other)
