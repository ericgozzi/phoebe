import System
import Rhino
import Grasshopper

import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
from compas_rhino.conversions import point_to_compas, mesh_to_compas
from compas.geometry import Transformation, Translation, Vector, Scale, Frame
import Rhino.FileIO



class MyComponent(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self,
            point_cloud: System.Collections.Generic.List[object],
            interesting_cells: System.Collections.Generic.List[object],
            library,
            start_marching):


        if point_cloud == None:
            ghenv.Component.Message = "Please provide point cloud"
            return
        elif interesting_cells == None:
            ghenv.Component.Message = "Please provide interesting_cells" 
            return
        elif library == None:
            ghenv.Component.Message = "Pleas provde file-path to the pannustheka"
            return
        elif not start_marching:
            ghenv.Component.Message = "All set up: start marching!"
            return   
        
        if start_marching:
            ghenv.Component.Message = "Marched!"

            """
            The call to arms is clear, the march begins,  
            With troops assembled, the battle we win..
            """
            
            marching_cube = MarchingCubes(interesting_cells, point_cloud)
            marching_cube.set_scale_factor()

            """
            The battlefield is surveyed, the scale is set,  
            The troops are measured, their positions are met.
            """

            marching_cube.run_marching_cubes(library)

            """
            The order is given, the troops advance,  
            Cells and cubes in perfect stance.
            """
            
            envelope = marching_cube.envelope
            
            """
            The march complete, the envelope now holds,  
            Victory secured, the story unfolds.
            """
        envelope = th.list_to_tree(envelope)
        return envelope





 
"""
                                                                                                      
   _____    ______  _____    __   __   _     _  _______   _____   _______  _______   _____    _     _ 
  (_____)  (______)(_____)  (__)_(__) (_)   (_)(__ _ __) (_____) (__ _ __)(_______) (_____)  (_)   (_)
  (_)__(_) (_)__   (_)__(_)(_) (_) (_)(_)   (_)   (_)   (_)___(_)   (_)      (_)   (_)   (_) (__)_ (_)
  (_____)  (____)  (_____) (_) (_) (_)(_)   (_)   (_)   (_______)   (_)      (_)   (_)   (_) (_)(_)(_)
  (_)      (_)____ ( ) ( ) (_)     (_)(_)___(_)   (_)   (_)   (_)   (_)    __(_)__ (_)___(_) (_)  (__)
  (_)      (______)(_)  (_)(_)     (_) (_____)    (_)   (_)   (_)   (_)   (_______) (_____)  (_)   (_)
                                                                                                      
                                                                                                      
"""
class Permutation(object):

    """
    In a world where geometry and logic weave,  
    A husband and wife, in harmony, believe.  
    Through layers and shapes, their journey flows,  
    Unlocking patterns that no one knows.  
    With rules in hand, they venture deep,  
    Revealing secrets that models keep.  
    One permutation at a time, they strive,  
    Bringing structure and form alive.
    """

    def __init__(self):
        self.mesh = None
        self.points = None
        self.bounding_box_points = None


    def import_from_pannustheka(self, cell, rule, library):

        function = cell.function
        if function == None: function = "default"


        # Wife:     "Does this rule fit, my dear?  
        #           Is it too small, or too big, I fear?"  

        # Husband:  "It must be eight, no more, no less,  
        #           For only then, the we will progress." 


        if len(rule) > 8 or len(rule) < 8: return None
        if rule == [0,0,0,0,0,0,0,0] or rule == [1,1,1,1,1,1,1,1]:
            return None

        i=0
        for index in rule:
            i = i+index


        # Wife:     "Shall we go left, or take the right?  
        #           Invert the rule, if the sum’s too bright?"  

        # Husband:  "If the sum’s too high, we must reverse,  
        #           Invert the bits, and try it inverse." 


        if i > 4:
            inverted_rule = []
            for index in rule:
                if index == 0:
                    inverted_rule.append(1)
                else:
                    inverted_rule.append(0)
            rule = inverted_rule
        file_path = library + function + "_" + str(rule) + ".3dm"


        # Wife:     "Let’s open the file, see what we’ve got,  
        #           Will it fit, or shall we not?"  

        # Husband:  "We’ll try our best, and test once more,  
        #           If it fails, we’ll open the next door."  


        try:
            model = Rhino.FileIO.File3dm.Read(file_path)
        except:          
            # Wife: "Oh no, the file’s not quite right,  
            #       But we’ll move on, and not lose sight."
            return


        objects = model.Objects
        

        # Wife:     "Now we check the layers, all must be clear,  
        #           For each one, we must draw near."  

        # Husband:  "I’ll sort them out, don’t you fear,  
        #           The geometry’s path will soon appear."

        layer_table = model.AllLayers

        geometries = []
        points_list = []
        bbpoints_list = []
        

        # Wife:     "Into the layers, we dive with care,  
        #           Meshes and points must be handled fair."  
        # Husband:  "Each one will fall in the right place,  
        #           So we can see the full design’s grace."


        for obj in objects:
                    
            if(obj.Attributes.LayerIndex == 0):
                mesh = obj.Geometry
            elif(obj.Attributes.LayerIndex == 1):
                points_list.append(obj.Geometry.Location)
            elif(obj.Attributes.LayerIndex == 2):
                bbpoints_list.append(obj.Geometry.Location)
                                

        # Wife:     "All in place, but now we must see,  
        #           The meshes and points, in compas they’ll be."  

        # Husband:  "Right you are, let’s make the shift,  
        #           So all aligns, and we’ll get the gift."
        

        mesh = mesh_to_compas(mesh)
        points_list = points_to_compas(points_list)
        bbpoints_list = points_to_compas(bbpoints_list)

        self.mesh = mesh
        self.points = points_list
        self.bounding_box_points = bbpoints_list


        # Wife:     "We’re done now, everything’s aligned,  
        #           The data’s set, in perfect bind."  

        # Husband:  "Yes, it’s done, and we can rest,  
        #           The permutation’s path was our best."


  
  
"""
        ___           ___           ___           ___           ___                       ___           ___     
       /\__\         /\  \         /\  \         /\  \         /\__\          ___        /\__\         /\  \    
      /::|  |       /::\  \       /::\  \       /::\  \       /:/  /         /\  \      /::|  |       /::\  \   
     /:|:|  |      /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/__/          \:\  \    /:|:|  |      /:/\:\  \  
    /:/|:|__|__   /::\~\:\  \   /::\~\:\  \   /:/  \:\  \   /::\  \ ___      /::\__\  /:/|:|  |__   /:/  \:\  \ 
   /:/ |::::\__\ /:/\:\ \:\__\ /:/\:\ \:\__\ /:/__/ \:\__\ /:/\:\  /\__\  __/:/\/__/ /:/ |:| /\__\ /:/__/_\:\__\
   \/__/~~/:/  / \/__\:\/:/  / \/_|::\/:/  / \:\  \  \/__/ \/__\:\/:/  / /\/:/  /    \/__|:|/:/  / \:\  /\ \/__/
         /:/  /       \::/  /     |:|::/  /   \:\  \            \::/  /  \::/__/         |:/:/  /   \:\ \:\__\  
        /:/  /        /:/  /      |:|\/__/     \:\  \           /:/  /    \:\__\         |::/  /     \:\/:/  /  
       /:/  /        /:/  /       |:|  |        \:\__\         /:/  /      \/__/         /:/  /       \::/  /   
       \/__/         \/__/         \|__|         \/__/         \/__/                     \/__/         \/__/    
        ___           ___           ___           ___           ___                                             
       /\  \         /\__\         /\  \         /\  \         /\  \                                            
      /::\  \       /:/  /        /::\  \       /::\  \       /::\  \                                           
     /:/\:\  \     /:/  /        /:/\:\  \     /:/\:\  \     /:/\ \  \                                          
    /:/  \:\  \   /:/  /  ___   /::\~\:\__\   /::\~\:\  \   _\:\~\ \  \                                         
   /:/__/ \:\__\ /:/__/  /\__\ /:/\:\ \:|__| /:/\:\ \:\__\ /\ \:\ \ \__\                                        
   \:\  \  \/__/ \:\  \ /:/  / \:\~\:\/:/  / \:\~\:\ \/__/ \:\ \:\ \/__/                                        
    \:\  \        \:\  /:/  /   \:\ \::/  /   \:\ \:\__\    \:\ \:\__\                                          
     \:\  \        \:\/:/  /     \:\/:/  /     \:\ \/__/     \:\/:/  /                                          
      \:\__\        \::/  /       \::/__/       \:\__\        \::/  /                                           
       \/__/         \/__/         ~~            \/__/         \/__/                                            
"""
  
class MarchingCubes(object):

    """
    The battle begins, the troops are in place,  
    We march forward, to conquer the space.  
    With cells of interest and points in the field,  
    Our march takes shape, the victory revealed.
    """

    def __init__(self, interesting_cells, point_cloud):

        """
        The command is set, the units are named,  
        Interesting cells, point clouds — our aim.  
        With factors of scale, ready for the task,  
        We prepare the troops, and await the ask
        """

        self.envelope = []                          # The formation is set, the envelope our shield.

        self.interesting_cells = interesting_cells  # The cells we command, our front line strong.
        self.point_cloud = point_cloud              # # The points of reference, where we belong.

        self.scale_x_factor = None                  # The width to be scaled, the ground we must cross.
        self.scale_y_factor = None                  # The height to be scaled, no room for loss.
        self.scale_z_factor = None                  # The depth to be scaled, through which we march.

        self.set_scale_factor()                     # The first order: Set the scale, our marching arch.




    def set_scale_factor(self):

        """
        The terrain is surveyed, the cells we inspect,  
        With boxes drawn, our first step to perfect.  
        The scale must be set, to match the size,  
        For the troops to advance, under careful eyes.
        """

        # Survey the land, the box must be drawn.
        cell_box = self.interesting_cells[0].draw_box()

        # The width of the battlefield is ours to command.
        self.scale_x_factor = cell_box.xsize 
        # The height is adjusted, we take our stand.
        self.scale_y_factor = cell_box.ysize
        # Depth is measured, our path is planned.
        self.scale_z_factor = cell_box.zsize 




    def add_permutation(self, permutation, destination_cell):
        
        """
        Now the battle begins, the forces move,  
        A permutation is placed, a strategic groove.  
        With translation and scale, we shift our might,  
        As soldiers are aligned, ready for the fight.
        """
        # Define the movement of the troops, as we prepare to advance.
        if permutation is not None:

            # Translation vector, the path to be walked,
            translation_vector = Vector.from_start_end(permutation.bounding_box_points[0], 
                                                        destination_cell.get_vertices_points()[0])
            translation_matrix = Translation.from_vector(translation_vector)
            
            # Transformation origin, we set our base,
            transformation_origin = Frame.from_points(permutation.bounding_box_points[0], 
                                                    permutation.bounding_box_points[1], 
                                                    permutation.bounding_box_points[3])
            
            # Scaling transformation, to match the size of our force,
            scale_transformation = Scale.from_factors([self.scale_y_factor, 
                                                        self.scale_x_factor, 
                                                        self.scale_z_factor], 
                                                        frame=transformation_origin)
            
            # The mesh is copied, to be transformed with care.
            tile = permutation.mesh.copy()
            # Scaling our force, for the next phase of war.
            tile.transform(scale_transformation)
            # Moving into position, with orders clear and fair.
            tile.transform(translation_matrix)



            # The troops are ready, within the envelope they stay.
            self.envelope.append(tile)



    def run_marching_cubes(self, library):

        """
        The campaign begins, the battle unfolds,  
        As we march across, the story is told.  
        We march through cells, with vertices in hand,  
        The marching cubes advance, to take the land.
        """
        
        for cell in self.interesting_cells:
            # The formation is drawn, the vertices placed,
            # Our strategic points, carefully traced.
            cell_vertices = []
            for i in range(0, 8):
                # Marking each corner, to ensure no mistake.
                cell_vertices.append(cell.draw_box().corner(i))
            
            # The passport is scanned, the rule must be known,
            cell_rule = cell.get_passport(self.point_cloud)
            # The rule to guide us, as we march alone.

            # A new permutation, ready to deploy.
            permutation = Permutation()
            permutation.import_from_pannustheka(cell, cell_rule, library)
            # The orders are sent, the cell is employed.

            if permutation.mesh is not None:
                # The force is ready, marching through the field,
                self.add_permutation(permutation, cell)
                # We add the permutation, our victory sealed.




  


def points_to_compas(points):

    """
    The point’s journey begins, small yet grand,  
    To Compas they travel, at the general’s command.  
    Each point, a hero, with a single quest,  
    To transform and align, and do their best.
    """

    compas_points = []
    for pt in points:
        compas_points.append(point_to_compas(pt))
    return compas_points
    


def meshes_to_compas(meshes):

    """
    The meshes prepare, their form set to change,  
    To Compas they travel, through the fields they range.  
    Each mesh, a warrior, both sturdy and wise,  
    Transformed and aligned, before our eyes.
    """
    
    mesh_compas = []
    for m in meshes:
        mesh_compas.append(mesh_to_compas(m))
    return mesh_compas




