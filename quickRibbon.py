import maya.cmds as cmds
import maya.mel as mel
import sys

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
        self.ctlCount = cmds.intFieldGrp(numberOfFields=1, label="# of controllers", value1=1)
        cmds.separator(height=30)
        
        #UI: buttons to finalize
        cmds.button(label="Finalize NURBS Plane", command= self.make_plane)
        cmds.separator(height=15, style='none')
        cmds.button(label="Finalize Ribbon", command= self.make_ribbon);#incomplete button. Main function isn't here yet
        
        #display new window
        cmds.showWindow()
        
    def make_plane(self, *args):
        #function to create the NURBS plane
        #find the axis
        self.axisChoice = cmds.radioButtonGrp(self.radioValue, q=True, sl=True)
        self.axisArray = [[1.0,0.0,0.0,], [0.0,1.0,0.0], [0.0,0.0,1.0]]
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
        #create and process follicle system
        ##find number of follicles to be created
        uvCompareList = [self.nurbsU, self.nurbsV]
        fol_i = max(uvCompareList)
        fol_uv_x = 0
        fol_uv_delta = 1/fol_i
        ##create follicles
        for everyItem in range(0, fol_i):
            fol_subfix = str(everyItem+1)
            while fol_uv_x <= 1:
                 fol_shp=cmds.createNode('follicle', n=self.nurbsN+'flc_Shape'+fol_subfix) #returns follicle shape node
                 cmds.setAttr(fol_shp+'.simulationMethod', 0)
                 ###find follicle transform node
                 fol_trns = cmds.pickWalk(d='up') #returns a list that contains follicle transform node
                 cmds.rename(self.nurbsN+'flc_'+fol_subfix, ignoreShape=True)
                 ###connect follicle shape and transform nodes
                 cmds.connectAttr(fol_shp+'.outRotate', fol_trns[0]+'.rotate')
                 cmds.connectAttr(fol_shp+'.outTranslate', fol_trns[0]+'.translate')
                 ###connect follicle to NURBS plane
                 cmds.connectAttr(self.ribbon[0]+'Shape.local', fol_shp+'.inputSurface')
                 cmds.connectAttr(self.ribbon[0]+'Shape.worldMatrix', fol_shp+'.inputWorldMatrix')
                 ###move follicles to to right place
                 if self.nurbsU >= self.nurbsV:
                    cmds.setAttr(fol_shp+'.parameterU', fol_uv_x)
                    cmds.setAttr(fol_shp+'.parameterV', 0.5)
                    fol_uv_x +=fol_uv_delta
                 else:
                    cmds.setAttr(fol_shp+'.parameterU', 0.5)
                    cmds.setAttr(fol_shp+'.parameterV', fol_uv_x)
                    fol_uv_x +=fol_uv_delta

        #create follicle joints

        #parent follicle joints under corresponding follicles

        #create controller joints

        #create controllers and parent-constrain controller joints

        #skinbind controller joints to the NURBS plane

        #point-constrain the middle controller

        #orient-constrain the group of controllers after the first and before the middle

        #orient-constrain the group of controllers after the middle and before the last
            
quickRibbon()