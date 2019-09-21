"""
Copyright 2016 Jaehyun Park, 2017 Robin Verschueren

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import cvxpy.lin_ops.lin_op as lo
import cvxpy.lin_ops.lin_utils as lu


class InverseData(object):
    """Data useful for retrieving a solution from a problem."""

    def __init__(self, problem):
        variables = problem.variables()
        self.id_map, self.var_offsets, self.x_length, self.var_shapes = (
            self.get_var_offsets(variables))

        self.param_shapes = {}
        # Always start with CONSTANT_ID.
        self.param_to_size = {lo.CONSTANT_ID: 1}
        self.param_id_map = {}
        offset = 0
        for param in problem.parameters():
            self.param_shapes[param.id] = param.shape
            self.param_to_size[param.id] = param.size
            self.param_id_map[param.id] = offset
            offset += param.size
        self.param_id_map[lo.CONSTANT_ID] = offset

        self.id2var = {var.id: var for var in variables}
        self.real2imag = {var.id: lu.get_id() for var in variables
                          if var.is_complex()}
        constr_dict = {cons.id: lu.get_id() for cons in problem.constraints
                       if cons.is_complex()}
        self.real2imag.update(constr_dict)
        self.id2cons = {cons.id: cons for cons in problem.constraints}
        self.dv_id_map = dict()
        self.constraints = None

    def get_var_offsets(self, variables):
        var_shapes = {}
        var_offsets = {}
        id_map = {}
        vert_offset = 0
        for x in variables:
            var_shapes[x.id] = x.shape
            var_offsets[x.id] = vert_offset
            id_map[x.id] = (vert_offset, x.size)
            vert_offset += x.size
        return (id_map, var_offsets, vert_offset, var_shapes)
