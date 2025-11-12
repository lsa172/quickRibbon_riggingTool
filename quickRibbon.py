'''
QuickRibbon: a tool to automate ribbon setups
Created by Linqi "Lyne" Sun under the supervision of Philippe Pasquier at Simon Fraser University 
for class IAT806: Interdisciplinary Design Approaches to Computing
'''

import maya.cmds as cmds
import maya.mel as mel
import sys
import statistics
import math


class quickRibbon(object):
    
    #the constractor creates the UI
    def __init__(self):
        
        self.UIWindow = "quickRibbon_window"
        self.UITitle = "QuickRibbon Creator"
        self.UISize = (400, 400)
        
        #UI: close existing window if opened
        if cmds.window(self.UIWindow, exists = True):
            cmds.deleteUI(self.UIWindow, window = True)
    
        #UI: create new window
        cmds.window(self.UIWindow, title=self.UITitle, widthHeight=self.UISize)
        cmds.columnLayout(adjustableColumn = True)
        cmds.text(self.UITitle)
        cmds.separator(height=40)
        
        #UI: user input fields for customizing the ribbon's NURBS plane
        cmds.text("NURBS plane setup", align='left')
        self.prefix = cmds.textFieldGrp(label="Prefix_")
        self.w = cmds.floatFieldGrp(numberOfFields=1, label="Width", value1=1)
        self.l = cmds.floatFieldGrp(numberOfFields=1, label="Length", value1=1)
        self.UPatch = cmds.intFieldGrp(numberOfFields=1, label="U Patch count", value1=1)
        self.VPatch = cmds.intFieldGrp(numberOfFields=1, label="V Patch count", value1=1)
        self.radioValue = cmds.radioButtonGrp(label="Axis", labelArray3=['x', 'y', 'z'], numberOfRadioButtons=3)
        cmds.separator(height=30)
        
        #UI: user input fields for customizing the ribbon's controllers
        cmds.text("Ribbon controllers setup", align='left')
        self.ctlCount = cmds.intFieldGrp(numberOfFields=1, label="# of controllers", value1=3)
        cmds.separator(height=30)
        
        #UI: buttons to finalize
        cmds.button(label="Finalize NURBS Plane", command= self.make_plane)
        cmds.separator(height=15, style='none')
        cmds.button(label="Finalize Ribbon", command= self.make_ribbon);#incomplete button. Main function isn't here yet

        #UI: user notice text
        cmds.separator(height=15, style='none')
        cmds.text("P.S. Please keep this window open while editing the NURBS plane for your ribbon", align='center')
        
        #display new window
        cmds.showWindow()
        
    def make_plane(self, *args):
        #function to create the NURBS plane
        #find the axis
        self.axisChoice = cmds.radioButtonGrp(self.radioValue, q=True, sl=True)
        self.axisArray = [[1.0,0.0,0.0], [0.0,1.0,0.0], [0.0,0.0,1.0]]
        self.axis = self.axisArray[self.axisChoice-1]
        #find the width and length
        self.nurbsW = cmds.floatFieldGrp(self.w, query=True, value1=True)
        lValue = cmds.floatFieldGrp(self.l, query=True, v1=True)
        self.nurbsLr = lValue/self.nurbsW
        #find name
        self.nurbsN = cmds.textFieldGrp(self.prefix, q=True, text=True)
        #find UV values
        self.nurbsU = cmds.intFieldGrp(self.UPatch, q=True, value1=True)
        self.nurbsV = cmds.intFieldGrp(self.VPatch, q=True, value1=True)
        
        #create NURBS plane
        self.ribbon = cmds.nurbsPlane(d=3, axis=self.axis, w=self.nurbsW, lr=self.nurbsLr, n=self.nurbsN+'nurbsPlane', u=self.nurbsU, v=self.nurbsV, ch=0)
    
    def make_ribbon(self, *args):
        self.ctlNum = cmds.intFieldGrp(self.ctlCount, q=True, value1=True)
        if self.ctlNum < 3:
            cmds.warning("Please enter at least 3 for number of controllers")
        else:
            #create and process follicles
            ##find number of follicles to be created
            uvCompareList = [self.nurbsU, self.nurbsV]
            fol_i = max(uvCompareList)
            fol_list = list(range(0, fol_i+1))
            fol_uv_x = 0
            fol_uv_delta = 1/fol_i
    
            for everyItem in fol_list:
                 fol_subfix = str(everyItem+1)
             
                 ##create a follicle
                 fol_shp=cmds.createNode('follicle', n=self.nurbsN+'ribbon_flc_Shape'+fol_subfix) #returns follicle shape node
                 cmds.setAttr(fol_shp+'.simulationMethod', 0)
                 ###find the follicle transform node
                 fol_trns = cmds.pickWalk(d='up') #returns a list that contains follicle transform node
                 ###connect the follicle's shape and transform nodes
                 cmds.connectAttr(fol_shp+'.outRotate', fol_trns[0]+'.rotate')
                 cmds.connectAttr(fol_shp+'.outTranslate', fol_trns[0]+'.translate')
                 ###connect the follicle to NURBS plane
                 cmds.connectAttr(self.ribbon[0]+'Shape.local', fol_shp+'.inputSurface')
                 cmds.connectAttr(self.ribbon[0]+'Shape.worldMatrix', fol_shp+'.inputWorldMatrix')
                 ###move the follicle to to right place
                 if self.nurbsU >= self.nurbsV:
                    cmds.setAttr(fol_shp+'.parameterU', fol_uv_x)
                    cmds.setAttr(fol_shp+'.parameterV', 0.5)
                    fol_uv_x +=fol_uv_delta
                 else:
                    cmds.setAttr(fol_shp+'.parameterU', 0.5)
                    cmds.setAttr(fol_shp+'.parameterV', fol_uv_x)
                    fol_uv_x +=fol_uv_delta
                 ###create an offset group beneath the follicle
                 fol_offset = cmds.group(em=True, n=self.nurbsN+'ribbon_flc_offset_'+fol_subfix)
                 cmds.parent(fol_offset, fol_trns[0], r=True)
                 ###create a follicle joint
                 cmds.joint(rad=0.3, n=self.nurbsN+'ribbon_flc_jnt_'+fol_subfix)#automatically parented under offset
        
            ##group all created follicles
            all_fol = cmds.ls(self.nurbsN+'ribbon_flc_*', type='follicle')
            cmds.group(all_fol, n=self.nurbsN+'ribbon_flc_grp')

            ##create controller joints and controllers
            
            ##define function to make ctls
            def make_ctl(ctName, ctjnt):
                mct_axisArray = [[0.0,0.0,1.0], [1.0,0.0,0.0], [1.0,0.0,0.0]]
                mct_axis = mct_axisArray[self.axisChoice-1]
                mct_loc = cmds.xform(ctjnt, q=True, t=True, ws=True)
                mct_proto = cmds.circle(nr=mct_axis, r=1.2, ch=False, n=self.nurbsN+ctName, c=mct_loc)
                cmds.matchTransform(mct_proto, ctjnt, piv=True)
                cmds.group(n=self.nurbsN+ctName+'offset')
                return mct_proto

            ##create ctl joint at the first follicle joint
            loc_folJnt_01 = cmds.xform(self.nurbsN+'ribbon_flc_jnt_1', q=True, t=True, ws=True)
            cmds.select(cl=True)
            ctJnt_01 = cmds.joint(rad=1.0, n=self.nurbsN+'ribbon_control_jnt_1', p=loc_folJnt_01)
            ##create the first ctl and parent-constrain the first ctl joint
            ct_01 = make_ctl('ribbon_ctl_1', ctJnt_01)
            cmds.parentConstraint(ct_01, ctJnt_01)
            
            ##create ctl joint at the last follicle joint
            ctJnt_count = cmds.intFieldGrp(self.ctlCount, q=True, value1=True)
            loc_folJnt_last = cmds.xform(self.nurbsN+'ribbon_flc_jnt_'+str(fol_i+1), q=True, t=True, ws=True)
            cmds.select(cl=True)
            ctJnt_end = cmds.joint(rad=1.0, n=self.nurbsN+'ribbon_control_jnt_'+str(ctJnt_count), p=loc_folJnt_last)
            ##create the last ctl and parent-constrain the last ctl joint
            ct_end = make_ctl('ribbon_ctl_'+str(ctJnt_count), ctJnt_end)
            cmds.parentConstraint(ct_end, ctJnt_end)
            
            ##define all the indexes needed for calculating middle ctl joint locations here
            ctJnt_pcDelta = 1/(ctJnt_count-1)#increments for point constraint weights from first and last joint on middle joints
            ctJnt_list = list(range(2, ctJnt_count))
            
            ##create ctl joints in the middle
            for everyJoint in ctJnt_list:
                ###Create offset group
                cmds.select(cl=True)
                ctJnt_mid_subfix = str(everyJoint)
                ###create the ctl joint
                ctJnt_mid = cmds.joint(rad=1.0, n=self.nurbsN+'ribbon_control_jnt_'+ctJnt_mid_subfix)
                ###place the joint with point constraint and then delete the point constraint
                cmds.pointConstraint(ctJnt_01, ctJnt_end, ctJnt_mid)
                ctJnt_pc1 = cmds.pointConstraint(ctJnt_01, ctJnt_mid, e=True, w=1-ctJnt_pcDelta*(everyJoint-1))
                ctJnt_pc2 = cmds.pointConstraint(ctJnt_end, ctJnt_mid, e=True, w=ctJnt_pcDelta*(everyJoint-1))
                cmds.delete(ctJnt_pc1,ctJnt_pc2)
                ###create the ctl and parent-constrain ctl joints
                ct_mid = make_ctl('ribbon_ctl_'+ctJnt_mid_subfix, ctJnt_mid)
                cmds.parentConstraint(ct_mid, ctJnt_mid)
            
            ##skinbind controller joints to the NURBS plane
            all_ctJnts = cmds.ls(self.nurbsN+'ribbon_control_jnt_*', type='joint')
            cmds.skinCluster(all_ctJnts, self.ribbon)

            


        #(automated ctl motions)
        ##group ctJnts
        ##create mid_ribbon_fk_ctl, up offset, and low offset (if ctls between first&median/median&last >=2, create fk_ctl too)
        ##parent coresponding ctls (between first&median; between median&last) under the corresponding offset

        #orient-constrain up offset and low offset to mid offset (aimVec1/-1,0,0, world up object rotation upVec&worldUpVec0,0,1)

        #orient-constrain the group of controllers after the middle and before the last

quickRibbon()