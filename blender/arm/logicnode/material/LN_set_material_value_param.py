from arm.logicnode.arm_nodes import *

class SetMaterialValueParamNode(ArmLogicTreeNode):
    """TO DO."""
    bl_idname = 'LNSetMaterialValueParamNode'
    bl_label = 'Set Material Value Param'
    arm_section = 'params'
    arm_version = 1

    def arm_init(self, context):
        self.add_input('ArmNodeSocketAction', 'In')
        self.add_input('ArmDynamicSocket', 'Material')
        self.add_input('ArmStringSocket', 'Node')
        self.add_input('ArmFloatSocket', 'Float')

        self.add_output('ArmNodeSocketAction', 'Out')
