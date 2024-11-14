import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th

"""
In a terrain vast, with chunks so wide,
The user's points in stillness bide.
Each cell awaits with space to fill,
To catch the points that lie at will.
"""

alive_scheme = []

# We traverse each branch, through the grid’s domain,  
# A map of chunks, each path we attain.  
for i in range(chunks.BranchCount):
    chunks_list = chunks.Branch(i)
    branchPath = chunks.Path(i)
    
    # For each cell in the list, we start our quest,  
    # Checking if points lie within, at their best.  
    for j in range(chunks_list.Count):
        
        # Now the points, scattered and free,  
        # Will find their place in the chunks, you’ll see.  
        for point in points:

            """
            Does the point lie within the chunk's form?
            """
            bool = rs.PointInPlanarClosedCurve(point, chunks_list[j]) 

            # If the point’s inside, we make it known,  
            # Record the position, its status shown.  
            if bool == 1:
                print (i, j, bool)                  # Print the status, where it belongs
                alive_chunk = [i, j]                 # A cell marked alive, as the scheme grows strong
                alive_scheme.append(alive_chunk)     # Add it to the scheme, the list prolongs

# Finally, the alive scheme, all laid out,  
# Points in chunks, without a doubt.  
print(alive_scheme)


