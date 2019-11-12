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
from d7a.alp.action import Action
from d7a.alp.operands.indirect_interface_operand import IndirectInterfaceOperand
from d7a.alp.operations.indirect_forward import IndirectForward
from d7a.alp.operations.nop import NoOperation
from d7a.support.schema import Types


class IndirectForwardAction(Action):
  SCHEMA = [{
    "overload" : Types.BOOLEAN(),
    "resp"     : Types.BOOLEAN(),
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(IndirectForward),
    "operand"  : Types.OBJECT(IndirectInterfaceOperand)  # TODO for now only D7 interface is supported
  }]

  def __init__(self, overload=False, resp=False, operation=NoOperation()):
    self.overload = overload
    self.resp = resp
    super(IndirectForwardAction, self).__init__(operation)

  def __iter__(self):
    byte = 0
    if self.overload: byte |= 1 << 7
    if self.resp:  byte |= 1 << 6
    byte += self.op
    yield byte

    for byte in self.operation: yield byte
