import math
from compas.geometry import Transformation, Rotation, Translation, Reflection
from compas.geometry import Vector, Point

"""
 M   M   AAAAA  TTTTT  RRRR    III   X   X
 MM MM  A     A   T    R   R    I     X X
 M M M  AAAAAAA   T    RRRR     I      X
 M   M  A     A   T    R  R     I     X X
 M   M  A     A   T    R   R   III   X   X
"""


class Matrices(object):

    """
    In the world of the Matrix, where reality is fake,  
    Transformation is key, as the codes shift and break.  
    Each matrix a doorway, each method a key,  
    Unlocking the truth, setting minds free.  
    """

    def get_roatation_matrix(axis, rotation_point):
        """
        A twist in the code, reality bends,  
        Around an axis, the world never ends.  
        Rotating through space, in a digital trance,  
        With each turn, we break the illusion’s dance.  
        """
        
        # The identity matrix, the ground where we stand,
        # The world unchanging, as if by some hand.
        t0 = Matrices.get_identity_matrix()
        # A 90-degree turn, reality tilts and sways,
        # A quarter-turn twist, shifting the maze.
        r1 = Rotation.from_axis_and_angle(axis, math.pi/2, rotation_point)
        # A 180-degree turn, bending the world in two,
        # The shape shifts further, revealing what's new.
        r2 = Rotation.from_axis_and_angle(axis, math.pi, rotation_point)
        # A 270-degree twist, the illusion unravels more,
        # The boundaries of space become something we explore.
        r3 = Rotation.from_axis_and_angle(axis, (math.pi/2)*3, rotation_point)
        # A collection of turns, four steps in this dance,
        # A symphony of rotation, no matter the chance.
        rotation_list = [t0, r1, r2, r3]
        # Returning the rotations, a journey through space,
        # A broken illusion, a new reality to embrace.
        return rotation_list




    def get_reflection_matrix(centroid_point):
        """
        The mirror of truth, where worlds reflect,  
        In the Matrix’s glass, what’s real we detect.  
        Flip the plane, as the code rewrites,  
        Reflections of freedom in digital lights.  
        """

        # The identity matrix, still as the world stands,
        # A place where nothing changes, as reality expands.
        t0 = Matrices.get_identity_matrix()
        # Reflection on the x-plane, the world turns, flipped,
        # A mirrored view, where the truth is equipped.
        mrx = Reflection.from_plane(([centroid_point[0], centroid_point[1], centroid_point[2]], [1,0,0]))
        # Reflection on the y-plane, bending the code,
        # A shift of perception, where light starts to explode.
        mry = Reflection.from_plane(([centroid_point[0], centroid_point[1], centroid_point[2]], [0,1,0]))
        # Reflection on the z-plane, where depth comes alive,
        # Flipping through dimensions, the Matrix starts to drive.
        mrz = Reflection.from_plane(([centroid_point[0], centroid_point[1], centroid_point[2]], [0,0,1]))
        # A collection of reflections, shifting the shape of space,
        # A new way of seeing, where truth finds its place.
        reflections_list = [t0, mrx, mry, mrz]
        # Returning the reflections, a world turned around,
        # In the mirror of the Matrix, where freedom is found.
        return reflections_list




    def get_identity_matrix(): 
        """
        The Matrix’s base, where all things begin,  
        A world unchanging, where nothing within.  
        It’s the root of all, the place we must start,  
        The code behind the code, the hidden heart.  
        """ 

        # The identity matrix, where nothing changes,  
        # A world in stasis, where time rearranges.
        identity_matrix =   [[1.0000, 0.0000, 0.0000, 0.0000], 
                            [0.0000, 1.0000, 0.0000, 0.0000], 
                            [0.0000, 0.0000, 1.0000, 0.0000], 
                            [0.0000, 0.0000, 0.0000, 1.0000]]
        # Returning the identity, the essence of the start,  
        # The silent code that holds the Matrix apart.
        return identity_matrix



class Pannus(object):
    """
    A garment in the code, woven from points and threads,  
    Each point a stitch, each change a shift.  
    Like clothes hung out, blowing in the breeze,  
    The fabric shifts and flows with each gentle spin.
    """

    def __init__(self, reference, rotation_x, rotation_y, rotation_z, reflection, transformed_points):
        """
        The washing begins—spinning, turning, and pressing,  
        The cloth gets cleaned, its shape confessing.  
        Points are turned, stretched, and renewed,  
        A new fabric appears, in a fresh point of view.
        """
        self.points = transformed_points
        self.points_count = len(self.points)
        self.original_mesh = reference.mesh
        self.rotation_z = rotation_z
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.reflection = reflection
        
        mesh = self.original_mesh.copy()
        mesh.transform(reflection)
        mesh.transform(rotation_z)
        mesh.transform(rotation_x)
        mesh.transform(rotation_y)
        self.mesh = mesh
        
        rule_string = []
        
        self.box = reference.box
        self.vertices = reference.box.points

        #generate passport index   
        for vertex in self.vertices:
            i = 0
            gate = True
            for point in self.points:
                if round(point.x, 3) == round(vertex.x, 3) and round(point.y, 3) == round(vertex.y, 3) and round(point.z, 3) == round(vertex.z, 3):
                    rule_string.append(1)
                    gate = False
                if i == self.points_count -1 and gate:
                    rule_string.append(0)
                i += 1

        self.rule = rule_string
        self.function = reference.function




    def generate_all_pemutations(reference, rotations_x, rotations_y, rotations_z, reflections):
        """
        The cloth, stretched wide, hung on many lines,  
        Each fold, each twist, in the wind it climbs.  
        The fabric reshapes, new patterns are born,  
        Spinning in the breeze, like clothes on a morn.
        """
        pannustheka = []
        
        for mr in reflections:                    
            for rz in rotations_z:
                for rx in rotations_x:
                    for ry in rotations_y:
                        transformed_points = Pannus.transform_points(reference.points, mr, rx, ry, rz)
                        pannus = Pannus(reference, rx, ry, rz, mr, transformed_points)
                        pannustheka.append(pannus)
                    
        return pannustheka

    
    def transform_points(points, reflection, rotation_x, rotation_y, rotation_z):
        """
        Each point a thread, spun and twisted around,  
        The fabric reshaped, turning, spinning, unbound.  
        Like clothes swaying, each point takes flight,  
        In a fresh new direction, changing its sight.
        """
        point_group = []
        for point in points:
            pt = point.copy()
            pt.transform(reflection)
            pt.transform(rotation_z)
            pt.transform(rotation_x)
            pt.transform(rotation_y)
            point_group.append(pt)
        return point_group


    def get_file_name(self):
        """
        A label stitched into the cloth, its name so true,  
        A pattern formed from the rules, a design to view.  
        The file is the garment, marked for all to see,  
        With a name that tells the story of its fabric’s decree.
        """
        file_name = self.function + "_" + str(self.rule) + ".3dm"
        return file_name



class Pannustheka(object):

    def __init__(self, reference, rotations_x, rotations_y, rotations_z, reflections):
        
        self.permutations = []
        
        for mr in reflections:                    
            for rz in rotations_z:
                for rx in rotations_x:
                    for ry in rotations_y:
                        transformed_points = Pannus.transform_points(reference.points, mr, rx, ry, rz)
                        pannus = Pannus(reference, rx, ry, rz, mr, transformed_points)
                        self.permutations.append(pannus)

    def delete_same_permutations(self):
    #    def delete_same_permutations(permutations):
        reduced_pannustheka = []
        identity_list = []
        
        for pannus in self.permutations:
            if pannus.rule not in identity_list:
                reduced_pannustheka.append(pannus)
                identity_list.append(pannus.rule)  
                
        self.permutations = reduced_pannustheka


        


if generate: 
    x_axis = Vector(1, 0, 0)
    y_axis = Vector(0, 1, 0)
    z_axis = Vector(0, 0, 1)

    centroid = reference.get_centroid()

    rotations_z = Matrices.get_roatation_matrix(z_axis, centroid)
    rotations_x = Matrices.get_roatation_matrix(x_axis, centroid)
    rotations_y = Matrices.get_roatation_matrix(y_axis, centroid)
    reflections = Matrices.get_reflection_matrix(centroid)


    pannustheka = Pannustheka(reference, rotations_x, rotations_y, rotations_z, reflections)

    pannustheka.delete_same_permutations()

