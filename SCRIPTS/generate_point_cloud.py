import rhinoscriptsyntax as rs
from compas.geometry import Point, Line, Curve
from compas_rhino.conversions import box_to_rhino, point_to_rhino, point_to_compas

"""
 FFFFF  U   U  N   N  CCCC  TTTTT  III   OOO   N   N  SSSS
 F      U   U  NN  N  C        T    I   O   O  NN  N  S
 FFFF   U   U  N N N  C        T    I   O   O  N N N  SSS
 F      U   U  N  NN  C        T    I   O   O  N  NN     S
 F       UUU   N   N  CCCC     T   III   OOO   N   N  SSSS
"""


def remove_duplicate_points(point_cloud):
    # A canvas of stars, waiting to shine bright
    new_point_cloud = []
    # For each star in the sky, let it find its place,
    # But only if it’s unique, not a duplicate trace
    [new_point_cloud.append(x) for x in point_cloud if x not in new_point_cloud]
    # Return the constellation, where only true stars remain in sight
    return new_point_cloud




def check_cell_distance(cell, point_cloud, dimension):
     # The heart of the cell, a center of light in the vast space
    cell_center_point = cell.draw_box().frame.point
    # For each point, like a wandering star in the night,
    # Measure the distance to the cell’s center, seeking a connection of light
    for point in point_cloud:
        if point.distance_to_point(cell_center_point) < dimension:
             # If the star is near, return the cell, a shared space they both embrace
            return cell




def get_intresting_cells(point_cloud, cells):   
    # A home for the intriguing, a place where something special resides
    intresting_cells = []
    # The dimensions, defining the size of the house on all axes
    dimension_x = cells[0].draw_box().xsize
    dimensinon_y = cells[0].draw_box().ysize
    dimensinon_z = cells[0].draw_box().zsize
    # Gather all dimensions and select the largest, like choosing the grandest house
    dimensions = [dimension_x, dimensinon_y, dimensinon_z]
    dimension = max(dimensions)   
    # For each cell, check if it can house something meaningful
    for cell in cells:
        # Check if this house can shelter a point from the cloud, close enough to notice
        checked_cell = check_cell_distance(cell, point_cloud, dimension)
        # If the house can indeed shelter something valuable, mark it as interesting
        if checked_cell != None:
            intresting_cells.append(checked_cell)
    # Return the list of houses where something meaningful can dwell
    return intresting_cells


"""
 M   M   AAAAA   III  N   N
 MM MM  A     A   I   NN  N
 M M M  AAAAAAA   I   N N N
 M   M  A     A   I   N  NN
 M   M  A     A  III  N   N
"""

# The organism grows, its cells divide, 
# Increasing their density with a factor in hand
organism.increase_cell_density(division_factor)
# Newborn cells emerge, small and delicate they are,
# The list of cells updates, like a growing star
organism.update_cells_list_with_small_cells()
# All the cells in the organism, gathered as one,
# A universe of life, where growth has begun
cells = organism.get_cells()
# The living cells, full of life and light,
# A shining constellation that brightens the night
alive_cells = organism.get_alive_cells()
# The dead cells, dim and still in their place,
# Awaiting their fate in this cosmic space
dead_cells = organism.get_dead_cells()
# Only keep the dead cells near life’s embrace,
# For those who are close, we’ll keep in this place
trimmed_dead_cells = []
for cell in dead_cells:
     # If a dead cell is near a living star,
    # It has the chance to stay, not to wander too far
    if organism.is_neighbour_cell_alive(cell):
        trimmed_dead_cells.append(cell)
# The list of the dead cells, trimmed and refined,
# Now only those near life will remain in kind
dead_cells = []
dead_cells = trimmed_dead_cells.copy()
# From the living cells, a point cloud we weave,
# Each vertex a star, each point a reprieve
point_cloud = []
for cell in alive_cells:
    # The vertices of life, scattered and bright,
    # We gather them all to create the night
    points = cell.get_vertices_points()
    for pt in points:
        point_cloud.append(pt)
# Remove the duplicates, keep only the pure,
# Like stars in the sky, let them endure
point_cloud = remove_duplicate_points(point_cloud)
# And now, we seek the cells of interest, near,
# Dead but close to life, they are drawn near
intresting_cells = get_intresting_cells(point_cloud, dead_cells)


