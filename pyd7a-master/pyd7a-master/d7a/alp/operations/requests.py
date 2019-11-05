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

from d7a.alp.operations.operation import Operation
from d7a.alp.operands.file import DataRequest, FileIdOperand


class ReadFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 1
    self.operand_class = DataRequest
    super(ReadFileData, self).__init__(*args, **kwargs)


class ReadFileHeader(Operation):
  def __init__(self, *args, **kwargs):
    self.op = 2
    self.operand_class = FileIdOperand
    super(ReadFileHeader, self).__init__(*args, **kwargs)

