# DEVOLD
 structureD blockEd conVersion tO non-bLocked griD

This python program will help you convert a structured, blocked grid (where the points are represented by i, j, k indices and the connectivity is thus implicit, usually also containing several different zones), to a unified, unstructured grid (with one zone and explicit connectivity). For now, this only works for 2D.

For this, an ASCII data file with the mesh information from Tecplot is needed. Open the structured, blocked mesh in Tecplot and write the data as ASCII (.dat extension), point-based. Then, this software can derive the point coordinate information and determine the connectivity. The flow data is not preserved.

The place where this code has to be personalised is the boundary condition detection and categorisation. The boundaries are detected from the boundary information (i, j and k max and min indices), but which boundary point corresponds to which boundary must be done manually since this is case-specific. 

The code is written in a relatively clear way where this is done (here, the boundaries were "inlet", "outlet", "wall", "upper" and "lower", with a set of conditions for each boundary), towards the end of the python script. If you experience problems, please contact the author of the code.

The code has usage as:

   python convert_general.py [pythoninfile] [pythonoutfile] [bodytype]

where the [bodytype] is a setting used to the current application of the code (selecting the shape of the immersed body). This can be easily modified.

The outfile has a native format. To convert this to a format that looks like the GAMBIT Neutral format, use:

   ./write.exe Wa [pythonoutfile] [NEUfile]

where the final outfile [NEUfile] has the correct format. In case the formatting needs modifying, one can do so in the write.f90 fortran script, under the "Wa" section.  


