# quickRibbon_riggingTool
A Python script to create a very simple ribbon setup in Autodesk Maya. 
Created by Linqi "Lyne" Sun under the supervision of Philippe Pasquier as an IAT 806 class project at Simon Fraser University.

Feel free to use it in your projects or develop your script based on it! However, this script is meant to be free for anyone to use, so please do not re-sell it for profit.

If you have any questions, feedback, or comments, please contact me at lsa172@sfu.ca
(Please keep all correspondence professional. Gratias.)

How to use:
-After importing the script into Maya, run it to summon a window that prompts your input for the prefix of your ribbon,
    its width, length, U patch count, V patch count, the axis of the ribbon and the number of controllers you want.
-Clicking the "Finalize NURBS Plane" button will create a NURBS plane, which will serve as the basis for the ribbon. Feel free to
    move it around and edit its vertecies in component mode to match it to your model.
-Clicing the "Finalize Ribbon" button will finalize the ribbon control set up. It will create a set of IK controllers in the amount
    designated by you, and a set of FK controllers if the IK controllers reach a certain amount. 

notes:
-sometimes the automatic skinweight assignment to controller joints on the NRUBS plane may not be ideal. If the ribbon setup does not
    deform ideally, please double-check the skinweight on its NURBS plane first

Bonus content! LoadQuickRibbon script:
If you downloaded or copied the quickRibbon.py script in Maya's default script folder (usually \Documents\maya\scripts) and import or copy
this script into Maya's script editor, it will run the quickRibbon tool for you. It's pretty handy if you want to develop upon the current
quickRibbon script.