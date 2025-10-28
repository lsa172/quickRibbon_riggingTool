import maya.cmds as cmds;

class quickRibbon(object):
    
    #the constractor creates the UI
    def __init__(self):
        
        self.UIWindow = "quickRibbon_window";
        self.UITitle = "QuickRibbon Creator";
        self.UISize = (400, 400);
        
        #UI: close existing window if opened
        if cmds.window(self.UIWindow, exists = True):
            cmds.deleteUI(self.UIWindow, window = True);
    
        #UI: create new window
        cmds.window(self.UIWindow, title=self.UITitle, widthHeight=self.UISize);
        cmds.columnLayout(adjustableColumn = True);
        cmds.text(self.UITitle);
        cmds.separator(height=40);
        
        #UI: user input fields for customizing the ribbon's NURBS plane
        cmds.text("NURBS plane setup", align='left');
        self.prefix = cmds.textFieldGrp(label="Prefix_");
        self.w = cmds.floatFieldGrp(numberOfFields=1, label="Width", value1=1);
        self.l = cmds.floatFieldGrp(numberOfFields=1, label="Length", value1=1);
        self.UPatch = cmds.intFieldGrp(numberOfFields=1, label="U Patch count", value1=1);
        self.VPatch = cmds.intFieldGrp(numberOfFields=1, label="V Patch count", value1=1);
        self.radioValue = cmds.radioButtonGrp(label="Axis", labelArray3=['x', 'y', 'z'], numberOfRadioButtons=3);
        cmds.separator(height=30);
        
        #UI: user input fields for customizing the ribbon's controllers
        cmds.text("Ribbon controllers setup", align='left');
        self.ctlCount = cmds.intFieldGrp(numberOfFields=1, label="# of controllers", value1=1);
        cmds.separator(height=30);
        
        #UI: buttons to finalize
        cmds.button(label="Finalize NURBS Plane", command= self.make_plane);
        cmds.separator(height=15, style='none');
        cmds.button(label="Finalize Ribbon", command= self.make_ribbon);#incomplete button. Main function isn't here yet
        
        #display new window
        cmds.showWindow();
        
    def make_plane(self, *args):
        #function to create the NURBS plane
        #find the axis
        self.axisChoice = cmds.radioButtonGrp(self.radioValue, q=True, sl=True);
        self.axisArray = [[1.0,0.0,0.0,], [0.0,1.0,0.0], [0.0,0.0,1.0]];
        self.axis = self.axisArray[self.axisChoice-1];
        #find the width and length
        self.nurbsW = cmds.floatFieldGrp(self.w, query=True, value1=True);
        lValue = cmds.floatFieldGrp(self.l, query=True, v1=True);
        self.nurbsLr = lValue/self.nurbsW;
        #find name
        self.nurbsN = cmds.textFieldGrp(self.prefix, q=True, text=True);
        #find UV values
        self.nurbsU = cmds.intFieldGrp(self.UPatch, q=True, value1=True);
        self.nurbsV = cmds.intFieldGrp(self.VPatch, q=True, value1=True);
        
        #create NURBS plane
        cmds.nurbsPlane(d=1, axis=self.axis, w=self.nurbsW, lr=self.nurbsLr, n=self.nurbsN+'nurbsPlane', u=self.nurbsU, v=self.nurbsV);
    
    def make_ribbon(self, *args):
        #incomplete command. Main function isn't here yet
        print(":,(");
quickRibbon();