from arm.logicnode.arm_nodes import *

class GetLocationNode(ArmLogicTreeNode):
    """Returns the current location of the given object in world coordinates."""
    bl_idname = 'LNGetLocationNode'
    bl_label = 'Get Object Location'
    arm_section = 'location'
    arm_version = 1

    def arm_init(self, context):
        self.add_input('ArmNodeSocketObject', 'Object')

        self.add_output('ArmVectorSocket', 'Location')
