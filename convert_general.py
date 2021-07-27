import math
import sys
import copy
import datetime


import sys

#the first argument is input
#second the output
#third the bodytype

infile = str(sys.argv[1])
outfile = str(sys.argv[2])
bodytype = int(sys.argv[3])


print("Using ", infile, " to produce ", outfile, " with a body type ", bodytype)
if len(sys.argv) < 4:
	print("You forgot some of the input arguments. Input file, output file and bodytype.")
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)



def writeMesh(path, name, block_type, elements, nodes, boundaries, ngrps, nbsets, ndfcd, ndfvl):
        SUCCESS = 0

        filename = path + name
        print("Writing to: ", filename)
        #The fist line is the control info data
        f = open(filename, "w")
        line = "        CONTROL INFO 2.4.6" + '\n'
        f.write(line)

        #The second line indicates that the output file should be .neu
        line = "** GAMBIT NEUTRAL FILE" + '\n'
        f.write(line)

        #The third line the mesh name
        line = "mesh" + '\n'
        f.write(line)

        #The fourth line the version of the programme
        line = "PROGRAM:                BRCHMESH     VERSION:  0.0.1" + '\n'
        f.write(line)

        #The fifth line is the date and time
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line = dt_string  + '\n'
        f.write(line)

        #The sixth line the order of the neu mesh paramerets:
        #number of points
        #number of elements
        #number of element groups
        #number of BC sets
        #number of coordinate directions
        #number of fluid velocity directions
        line = "     NUMNP     NELEM     NGRPS    NBSETS     NDFCD     NDFVL" + '\n'
        f.write(line)


        line = str(len(nodes)) + '\n'
        f.write(line)

        line = str(len(elements))+ '\n'
        f.write(line)

        line = str(ngrps) + '\n'
        f.write(line)

        line = str(nbsets) + '\n'
        f.write(line)

        line = str(ndfcd) + '\n'
        f.write(line)

        line = str(ndfvl) + '\n'
        f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)

       #For the prism mesh, determine from the boundaries which one is inlet and which one the outlet
        if block_type == "prism":
                inlet = boundaries[0:int(len(boundaries)/2)]
                outlet = boundaries[int(len(boundaries)/2):-1]



        line = "   NODAL COORDINATES 2.4.6" + '\n'
        f.write(line)


        #Next, write all the node coordinates - for each node, the index and coordinates x, y (and z) separated by "\n"
        for n in range(0, len(nodes)):
                node = nodes[n]
                if block_type == "2d_rect_quad" or block_type == "Walpot":
                        line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2])  + '\n'

                elif block_type == "3d_box_quad" or "prism":
                        line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2]) + '\n' + str(node[3])  + '\n'


                else:
                        sys.exit("Writing for the selected block type not yet implemented. Abording.")

                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = "      ELEMENTS/CELLS 2.4.6"  + '\n'
        f.write(line)


        #Next, also write the connectivity of the elements - for each element, its index and the nodex which it is composed of
        for e in range(0, len(elements)):
                ele = elements[e]

                if block_type == "2d_rect_quad" or block_type == "Walpot":
                        line = str(ele[0]+1) + '\n' + str(2) + '\n' + str(4) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n'

                elif block_type == "3d_box_quad":
                        line = str(ele[0]+1) + '\n' + str(2) + '\n' + str(8) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n' + str(ele[5]+1) + '\n' + str(ele[6]+1) + '\n' + str(ele[7]+1) + '\n' + str(ele[8]+1) + '\n'

                elif block_type == "prism":
                        line = str(ele[0]+1) + '\n' + str(5) + '\n' + str(6) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n' + str(ele[5]+1) + '\n' +  str(ele[6]+1) + '\n'

                else:
                        sys.exit("Writing for the selected block type not yet implemented. Abording.")

                f.write(line)


        #For the spherical mesh, also add the inlet and outlet boundaries
        #if block_type == "prism":

        #        for b in range(0, len(boundaries)):
        #                boundary = boundaries[b]
        #                line = str(boundary[0]+1) + '\n' + str(3) + "\n" + str(3) + "\n" + str(boundary[2]+1) + "\n" + str(boundary[3]+1) + "\n" + str(boundary[4]+1) + "\n"
        #                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = "       ELEMENT GROUP 2.4.6"  + '\n'
        f.write(line)

        #Next, write up the physical groups - usually just one composed of all the elements and fluid material
        line = "GROUP:" + str(ngrps) + '\n'
        f.write(line)

        line = "ELEMENTS:" + str(len(elements)) + '\n'
        f.write(line)

        line = "MATERIAL:          2"  + '\n'
        f.write(line)

        line = "NFLAGS:          1" + '\n'
        f.write(line)

        line = "                           fluid" + '\n'
        f.write(line)


        left = len(elements)
        i = 0
        line = ""

        if block_type == "2d_rect_quad" or block_type == "3d_box_quad" or block_type == "Walpot":
                for e in range(0, len(elements)):
                        ele = elements[e]
                        i = i + 1

                        if i > 9:
                                line = line + str(ele[0]+1)  + '\n'
                                i = 0
                                f.write(line)
                                line = ""

                        else:
                                line = line + str(ele[0]+1) + "\n"

        else:
                #print("ll entities:", len(elements))
                for e in range(0, len(elements)):
                        ele = (elements)[e]
                        i = i + 1

                        if i > 9:
                                line = line + str(ele[0]+1)  + '\n'
                                i = 0
                                f.write(line)
                                line = ""

                        else:
                                line = line + str(ele[0]+1) + "\n"

        if len(line) > 0:
                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
        f.write(line)



        #Finally, document the boundaries or inlets/outlets into the domain
        if block_type == "2d_rect_quad":
                for flag in range(1, 5):

                        if flag == 1:
                                line = "x0" + '\n'

                        if flag == 3:
                                line = "x1" + '\n'

                        if flag == 2:
                                line = "y0" + '\n'

                        if flag == 4:
                                line = "y1" + '\n'

                        f.write(line)

                        count = 0
                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        count = count + 1

                        line = str(count) + '\n'
                        f.write(line)

                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0]
                                        line = str(el+1) + "\n" + str(3) + "\n" + str(flag)  + '\n'
                                        f.write(line)

                line = "ENDOFSECTION" + '\n'
                f.write(line)
                line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
                f.write(line)



        elif block_type == "Walpot":
                for flag in range(1, 5):

                        if flag == 1:
                                line = "inlet" + '\n'

                        if flag == 2:
                                line = "outlet" + '\n'

                        if flag == 3:
                                line = "wall" + '\n'

                        if flag == 4:
                                line = "sym" + '\n'

                        f.write(line)

                        count = 0
                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        count = count + 1

                        line = str(count) + '\n'
                        f.write(line)

                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0] 
					side =  boundaries[b][2]
                                        line = str(el+1) + "\n" + str(2) +  "\n" + str(side) + '\n'
                                        f.write(line)

                line = "ENDOFSECTION" + '\n'
                f.write(line)
                line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
                f.write(line)
        


        elif block_type == "prism":
                for flag in range(1, 3):

                        if flag == 1:
                                line = "inlet" + '\n'

                        if flag == 2:
                                line = "outlet" + '\n'


                        f.write(line)


                        count = 0

                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        count = count + 1

                        line = str(count) + '\n'
                        f.write(line)


                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0]

                                        if (flag == 1):
                                                side = 4
                                        else:
                                                side = 5
                                        line = str(el+1) + "\n" + str(5) + "\n" + str(side)  + '\n'
                                        f.write(line)

                line = "ENDOFSECTION" + '\n'
                f.write(line)
                line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
                f.write(line)


        else:
                sys.exit("Writing for the selected block type not yet implemented. Abording.")

        line = "ENDOFSECTION" + '\n'
        f.write(line)

        f.close()

        SUCCESS = 1
        return SUCCESS








def isbody(x, y):

	if bodytype == 1:
		y_max = 0.29365905906084594 * x + 0.16323111235395454
		if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
			return True

		elif y < y_max+0.1*y_max:
			if x > 0.22:
				if x < 1.345:
					return True
				else:
					return False
			else:
				return False

		else:
			return False

	if bodytype == 2:
		y_max = 0.24852337841527655*x + 0.1813574183214096
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 3:
		y_max = 0.2922245497835926*x + 0.1705573424423707	
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 4:
		y_max = 0.2451372029213282*x + 0.17879709818592726
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



	if bodytype == 5:
		y_max = 0.2931985387469937*x+0.16682973882896213
                if (x-0.2368)**2 + y**2 < 0.2368**2 + (0.2368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False

	if bodytype == 6:
		y_max = 0.24710185356751507*x+0.18105220256010612
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False

	if bodytype == 7:
		y_max = 0.29512244874352983*x+0.1684418911227265
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 8:
		y_max = 0.2451380830028364*x+0.18182855259764208
                if (x-0.22368)**2 + y**2 < 0.22368**2 + (0.22368**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.22:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False

	#### IN THE ONES ABOVE, CHANGE THE X AND Y LIMIT CONDITIONS!!!

	if bodytype == 9:
		y_max = 0.202305821635407*x+0.2993828391490366		
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 10:
		y_max = 0.168563767882373*x+0.31138141705574574
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.56:                                        
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False




	if bodytype == 11:
		y_max = 0.197165239077454*x+0.3008443898432992
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.345:                                        
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



	if bodytype == 12:
		y_max = 0.1554747858941384*x+0.32195199719695655
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.56: 
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False

	if bodytype == 13:
		y_max = 0.18731386742229783*x+0.31185051482118736
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



	if bodytype == 14:
		y_max = 0.15646053603385157*x+0.32186064971273387
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 15:
		y_max = 0.19514141130053786*x+0.309247101284559
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.37:
                                if x < 1.345:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 16:
		y_max = 0.16368226797240498*x+0.32117053720481625
                if (x-0.37)**2 + y**2 < 0.37**2 + (0.37**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.34:
                                if x < 1.56:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 17:
		y_max = 0.29137313206660953*x+0.14818077994489015
                if (x-0.20)**2 + y**2 < 0.20**2 + (0.20**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.20:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False

	if bodytype == 18:
		y_max = 0.15355161184674213*x+0.35184003702640937
		if (x-0.4)**2 + y**2 < 0.4**2 + (0.4**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.4:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



	if bodytype == 19:
		y_max = 0.23123685759128051*x+0.23639947149306978
		if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 20:
		y_max = 0.22316043371756608*x+0.2465721838610513
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



	if bodytype == 21:
		y_max = 0.2291975455801554*x+0.23739639561401782
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 22:
		y_max = 0.23280427931124073*x+0.23680382208638756
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True
                
                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.451:
                                        return True
                                else:   
                                        return False
                        else:   
                                return False

                else:   
                        return False



	if bodytype == 23:
		y_max = 0.2569113935198816*x+0.23304785036242232
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.305:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 24:
		y_max = 0.2027909325266294*x+0.24426840834566932
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.605:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False


	if bodytype == 25:
		y_max = 0.23224735620905315*x+0.23726293800659531 
                if (x-0.3)**2 + y**2 < 0.3**2 + (0.3**2)*0.05:
                        return True

                elif y < y_max+0.1*y_max:
                        if x > 0.3:
                                if x < 1.451:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                else:
                        return False



###################################################################################################
###################################################################################################






filename = infile #"data.dat"

f = open(filename, "r")

lines = f.readlines()

no_vars = 0
no_zones = 0
l = 0
READ_VARS = False
READ_ZONE = False
READ_PNTS = False
variables = []
zone_line = -1000
data = []
idxs = []
sizes = []
i = 1
j = 1
k = 1

no_points_theory = 0

###################################################################################################
#Read the Tecplot data
for line in lines:
	l = l + 1

	#print line[0:3]
	if READ_VARS:
		if line[0:3] == "ZON":
			READ_VARS = False
	if line[0:3] == "ZON":
		no_zones = no_zones + 1
		READ_ZONE = True
		READ_PNTS = False
		zone_line = l
		#print zone_line, "zone_line"
	if l == zone_line + 2:
		line = line.split(",")
		Ni = (line[0].split("="))[1]
		Nj = (line[1].split("="))[1]
		Nk = (line[2].split("="))[1]
		sizes.append([Ni, Nj, Nk])
		no_points_theory = no_points_theory + int(Ni) * int(Nj) * int(Nk)
		#print Ni, Nj, Nk
	if l == zone_line + 5:
		READ_PNTS = True
	if READ_PNTS:
		data.append(line)
		
	if READ_VARS:
		variables.append(line)
	if line[0:9] == "VARIABLES":
		READ_VARS = True
		line = line.split(" = ")
		variables.append(line[1])

#Now, all the data are in the data array, where the variables that are contained there are in the
#variables array

#In addition, for each zone, we have a i,j,k size stored in the sizes array as [Ni, Nj, Nk]

no_vars = len(variables)
data_formatted = []

xs = []
ys = []
zs = []

print("Theoretial number of points: ", no_points_theory)



###################################################################################################
#Extract coordinate information

for d in range(0, len(data)):
	dataline = data[d].split(" ")
	xs.append(float(dataline[1]))
	ys.append(float(dataline[2]))
	zs.append(float(dataline[3]))


print("Length of coordinate arrays: ", len(xs))



#Now all the coordinates reside in the xs, ys and zs field

index = 0
borders = []
connectivity = []
no_elements = 0
no_cells = 0
zone_elements = []
connectivity_all = []
connectivity_all_global = []
connectivity_global = []

no_points_all = []
no_points = 0

for z in range(0, no_zones):
        #Extract the local zone size
        size = sizes[z]
        kmax = int(size[2])
        jmax = int(size[1])
        imax = int(size[0])

        #For each point in the zone
        for k in range(1, kmax+1):
                for j in range(1, jmax+1):
                        for i in range(1, imax+1):
				no_points = no_points + 1

	no_points_all.append(no_points)
	no_points = 0


print("No points in the no_points_all array: ", sum(no_points_all))
xs_border = []
ys_border = []
zs_border = []

#print("no_points_all", no_points_all)

###################################################################################################
#Create connectivity based on zone information
for z in range(0, no_zones):
	#Extract the local zone size
	size = sizes[z]
	kmax = int(size[2])
	jmax = int(size[1])
	imax = int(size[0])

	#Indexing and bordering:

	#For each point in the zone
	for k in range(1, kmax+1):
		for j in range(1, jmax+1):
			for i in range(1, imax+1):

				border_count = 0

				#Determine the local zone index
				idx = i + (j-1) * imax + (k-1) * jmax
				idx = idx - 1
				#Append the zone index, index, and i, j and k to the index array
				if z > 0:
					first_idx = 0
					for n in range(0, z):
						first_idx = first_idx + no_points_all[n]
				else:
					first_idx = 0
				idxs.append([z, idx+first_idx, i, j, k])
	
				#If this point is on the border, save this information to borders
				if i == 1:
					border_count = border_count + 1	
				if i == imax:
					border_count = border_count + 1
				if j == 1:
					border_count = border_count + 1
				if j == jmax:
					border_count = border_count + 1
				
				borders.append(border_count)
	

	#Creating connectivity:

	#For each cell in the zone
	for k in range(1, kmax+1):
		for j in range(1, jmax):
			for i in range(1, imax):
				#Determine the four points of the cell
				cell1 = i   + (j  -1) * imax + (k-1) * jmax
				cell2 = i+1 + (j  -1) * imax + (k-1) * jmax
				cell3 = i+1 + (j+1-1) * imax + (k-1) * jmax
				cell4 = i   + (j+1-1) * imax + (k-1) * jmax


				cell1 = cell1 - 1
				cell2 = cell2 - 1
				cell3 = cell3 - 1
				cell4 = cell4 - 1
				#Save this information and append to local connectivity
				element = [cell1, cell2, cell3, cell4]
				connectivity.append(element)

				if z > 0:
					first_idx = 0
					for n in range(0, z):
						first_idx = first_idx + no_points_all[n]
	
					element_global = [cell1 + first_idx, cell2 + first_idx, cell3 + first_idx, cell4 + first_idx]
				else:
					element_global = element

				connectivity_global.append(element_global)


				no_elements = no_elements + 1

	#Save the number of elements
	zone_elements.append(no_elements)

	#Save the zone connectivity to all connectivities and clear the array
	connectivity_all.append(connectivity)
	connectivity = []


	connectivity_all_global.append(connectivity_global)
	connectivity_global = []

	no_cells = 0


#for i in range(0, len(connectivity_all_global)):
#	print connectivity_all_global[i]



print("No points in borders: ", len(borders))
#print idxs[0:200]

print("No elements: ", no_elements)



#At this point, we have a procedure that knows where the points are and how they are connected together
#The next step is to merge all of it together
total_elements = no_elements 

print("Theoretical number of elements: ", total_elements)

elements_merged = []


#for i in range(0, 4000):
#	print(idxs[i])


for z in range(0, len(connectivity_all_global)):
	for e in range(0, len(connectivity_all_global[z])):
		elements_merged.append(connectivity_all_global[z][e])

print("Length of elements_merged: ", len(elements_merged))

#Now we have the connectivity together and with those the respective point coordinates in xs, ys and zs 
#Of course, there are now double points between the zone borders. These must be identified and removed


#I.    For each point, scan through all other points
#II.   If the coordinates agree add it to a separate array
#III.  Go over all elements and their points and if some of them have "duplicates", replace the index by the smallest
#IV.   For each raplaced point, write to an array the index that was removed
#V.    

no_points = len(xs)
border_points = []

for i in range(0, no_points):
	if borders[i] > 0:
		border_points.append([i, xs[i], ys[i], zs[i]])


print("Number of border points: ", len(border_points))
#Border points now contains information like:
#[[3, 0.0, 0.1, 0.1], [6, 0.2, 0.4, 0.2], ...   ]


no_border_points = len(border_points)
identities = []

for i in range(0, no_points):
	identities.append([-1])

for i in range(0, no_border_points):
	#print("Check: ", i,  border_points[i][0])
	index_bp = border_points[i][0]
	identities[index_bp] = [index_bp]
	for j in range(0, no_border_points):    #(i, no_border_points):
		xi = border_points[i][1]
		yi = border_points[i][2]
		zi = border_points[i][3]

		xj = border_points[j][1]
		yj = border_points[j][2]
		zj = border_points[j][3]

		xmatch = ( abs(xi-xj) < 1e-7 )
		ymatch = ( abs(yi-yj) < 1e-7 )
		zmatch = ( abs(zi-zj) < 1e-7 ) 

		if xmatch and ymatch: # and i!=j:
			identities[index_bp].append(border_points[j][0])


#for i in range(0, len(identities)):
#	print identities[i]

	#        if len(identities[i]) > 2:
        #        print identities[i], xs[identities[i][0]], xs[identities[i][1]], xs[identities[i][2]]

#for i in range(0, no_points):
#	print borders[i], identities[i]

#for e in range(0, no_elements):
#	print elements_merged[e]
			
replaced = []
replaced_single = []


################# STUFF WORKS WELL DOWN TO THIS POINT


#Go through every element from the merged element array
for e in range(0, no_elements):
	element = elements_merged[e]

	#Extract the points and for each point
	for p in range(0, 4):
		point = element[p]
		
		#If this point is a border point
		if borders[point] > 0:

			#And if it is supposed to be possibly replaced
			if len(identities[point]) > 1:

				#Replace it by the smallest index
				replace_idx = min(identities[point])

				#In case the index changed, write it to a separate array
				if replace_idx != point:
					replaced.append([point, replace_idx])
					replaced_single.append(point)
					if borders[point] == 1 and borders[replace_idx] == 1:
						borders[point] = 0
						borders[replace_idx] = 0




					#element[p] = replace_idx
					#elements_merged[e] = element
				

replaced_single = list(dict.fromkeys(replaced_single))
elements_merged_corrected = []
shift_count = []

#for i in range(0, len(replaced_single)):
#	print replaced_single[i]
print("No of replaced points: ", len(replaced_single))

for i in range(0, no_points):
	shift_count.append(-1)

#print("Min:")
#print min(replaced_single)
replacements = []
 
for i in range(0, no_points):
	replacements.append([i, i])


for i in range(0, len(replaced)):
	idx = replaced[i][0]
	replacements[idx] = [replaced[i][0], replaced[i][1]]


for i in range(0, no_points):
	point_idx = replacements[i][1]
	new_idx = replacements[i][1]
	shift = 0
	for r in range(0, len(replaced_single)):
		replaced_id = replaced_single[r]
		if point_idx > replaced_id:
			shift = shift + 1

	new_idx = new_idx - shift
	replacements[i][1] = new_idx


for e in range(0, no_elements):
	element = elements_merged[e]
	for p in range(0, 4):
		point = element[p]
		new_point = replacements[point][1]
		#for r in range(0, len(replaced_single)):
		#	replaced_id = replaced_single[r]

		#	if point > replaced_id:
		#		shift = shift + 1
 
		element[p] = new_point
		#replacements[point] = [point, point-shift]
		#shift_count[point] = shift
	elements_merged_corrected.append(element)

#for i in range(0, 100):
#	print shift_count[i]


replaced = []
for i in range(0, no_points):
	replaced.append(0)


for i in range(0, len(replaced_single)):
	idx = replaced_single[i]
	replaced[idx] = 1

xs_filtered = []
ys_filtered = []
zs_filtered = []

for i in range(0, no_points):
	if replaced[i] == 0:
		xs_filtered.append(xs[i])
		ys_filtered.append(ys[i])
		zs_filtered.append(zs[i])

#print("Shifts: ", shift_count)

#print("Len filtered: ", len(xs_filtered))


no_points_filtered = len(xs_filtered)
no_elements = len(elements_merged_corrected)
#Now the coordinates and connectivity are fixed, but we lost the information about the borders
#To retrieve this, the borders field must be readjusted using the replacements information

borders_filtered = []
for i in range(0, no_points_filtered):
	borders_filtered.append(-1)


#print ("replacements: ", replacements)

for i in range(0, no_points):
	original_idx = replacements[i][0]
	new_idx = replacements[i][1]
	#if new_idx > len(borders_filtered) - 1:
	#	print("Problem: ",  replacements[i])
	#borders_filtered[new_idx] = borders[original_idx]
	#if borders_filtered[new_idx] != -1:
	#	print borders_filtered[new_idx], borders[original_idx]

	if borders[original_idx] == 0:
		borders_filtered[new_idx] = 0
	else:
		borders_filtered[new_idx] = 1

	#borders_filtered[new_idx] = borders[original_idx]

#print("borders_filtered", borders_filtered)


inlet = []
outlet = []
upper = []
wall = []

inlet_maxx = 0.0
outlet_minx = 5.9863
upper_miny = 100.0
lower_maxy = 0.000824

print("Point 27914", borders_filtered[27913], xs_filtered[27913], ys_filtered[27913] )

element_boundary_sides = []
for e in range(0, no_elements):
	element_boundary_sides.append([-1])

print("No points filtered", no_points_filtered)
print("Borders filtered ", len(borders_filtered))

for e in range(0, no_elements):
	element = elements_merged_corrected[e]
	b_count = 0
	b_points = []
	b_idxs = []
	for p in range(0, 4):
		point = element[p]
		if borders_filtered[point] == 1:
			b_count = b_count + 1
			b_points.append(point)
			b_idxs.append(p)

	if b_count == 2:
		idx1 = b_points[0]	
		idx2 = b_points[1]

		x1 = xs_filtered[idx1]
		y1 = ys_filtered[idx1]
		z1 = zs_filtered[idx1]

		x2 = xs_filtered[idx2]
		y2 = ys_filtered[idx2]
		z2 = zs_filtered[idx2]

		if b_idxs == [0, 1]:
			side = 1
		if b_idxs == [1, 2]:
			side = 2
		if b_idxs == [2, 3]:
			side = 3
		if b_idxs == [0, 3]:
			side = 4

		
	
		if x2 > outlet_minx and x1 > outlet_minx:
			element_boundary_sides[e] = ["outlet", side]
		elif y1 > upper_miny and y2 > upper_miny:
			element_boundary_sides[e] = ["upper", side]
		elif y1 < lower_maxy and y2 < lower_maxy:
			element_boundary_sides[e] = ["lower", side]
		elif isbody(x1, y1) and isbody(x2, y2):
			element_boundary_sides[e] = ["wall", side]
		else:
			if b_idxs == [0, 1]: 
				element_boundary_sides[e] = ["inlet", 1]

			if b_idxs == [1, 2]:
				element_boundary_sides[e] = ["inlet", 2]

			if b_idxs == [2, 3]:
				element_boundary_sides[e] = ["inlet", 3]

			if b_idxs == [0, 3]:
				element_boundary_sides[e] = ["inlet", 4]

	if b_count == 3:
		idx1 = b_points[0]
		idx2 = b_points[1]
		idx3 = b_points[2]
		
		x1 = xs_filtered[idx1]
		x2 = xs_filtered[idx2]
		x3 = xs_filtered[idx3]

		y1 = ys_filtered[idx1]
		y2 = ys_filtered[idx2]
		y3 = ys_filtered[idx3]

		z1 = zs_filtered[idx1]
		z2 = zs_filtered[idx2]
		z3 = zs_filtered[idx3]

		first = []
		second = []
		if b_idxs == [0, 1, 2]:
			if x1 > outlet_minx and x2 > outlet_minx:
				first = ["outlet", 1]
			elif y1 > upper_miny and y2 > upper_miny:
				first = ["upper", 1]
			elif y1 < lower_maxy and y2 < lower_maxy:
				first = ["lower", 1]
                        elif isbody(x1, y1) and isbody(x2, y2):
                                first = ["wall", 1]
			else:
				first = ["inlet", 1]


			if x2 > outlet_minx and x3 > outlet_minx:
				second = ["outlet", 2]
			elif y2 > upper_miny and y3 > upper_miny:
				second = ["upper", 2]
			elif y2 < lower_maxy and y3 < lower_maxy:
				second = ["lower", 2]
			elif isbody(x2, y2) and isbody(x3, y3):
                                second = ["wall", 2]
			else:
				second = ["inlet", 2]


		if b_idxs == [1, 2, 3]: 
                        if x1 > outlet_minx and x2 > outlet_minx:
                                first = ["outlet", 2]
                        elif y1 > upper_miny and y2 > upper_miny:
                                first = ["upper", 2]
                        elif y1 < lower_maxy and y2 < lower_maxy:
                                first = ["lower", 2]
			elif isbody(x1, y1) and isbody(x2, y2):
				first = ["wall", 2]
                        else:
                                first = ["inlet", 2]


                        if x2 > outlet_minx and x3 > outlet_minx:
                                second = ["outlet", 3]
                        elif y2 > upper_miny and y3 > upper_miny:
                                s2cond = ["upper", 3]
                        elif y2 < lower_maxy and y3 < lower_maxy:
                                second = ["lower", 3]
			elif isbody(x2, y2) and isbody(x3, y3): 
				second = ["wall", 3]
                        else:
                                second = ["inlet", 3]			


		if b_idxs == [0, 1, 3]:
                        if x1 > outlet_minx and x2 > outlet_minx:
                                first = ["outlet", 1]
                        elif y1 > upper_miny and y2 > upper_miny:
                                first = ["upper", 1]
                        elif y1 < lower_maxy and y2 < lower_maxy:
                                first = ["lower", 1]
			elif isbody(x1, y1) and isbody(x2, y2):
				first = ["wall", 1]
                        else:
                                first = ["inlet", 1]


                        if x1 > outlet_minx and x3 > outlet_minx:
                                second = ["outlet", 4]
                        elif y1 > upper_miny and y3 > upper_miny:
                                second = ["upper", 4]
                        elif y1 < lower_maxy and y3 < lower_maxy:
                                second = ["lower", 4]
			elif isbody(x1, y1) and isbody(x3, y3):
				second = ["wall", 4]
                        else:
                                second = ["inlet", 4]


		if b_idxs == [0, 2, 3]:
                        if x1 > outlet_minx and x3 > outlet_minx:
                                first = ["outlet", 4]
                        elif y1 > upper_miny and y3 > upper_miny:
                                first = ["upper", 4]
                        elif y1 < lower_maxy and y3 < lower_maxy:
                                first = ["lower", 4]
			elif isbody(x1, y1) and isbody(x3, y3):
				first = ["wall", 4]
                        else:
                                first = ["inlet", 4]


                        if x2 > outlet_minx and x3 > outlet_minx:
                                second = ["outlet", 3]
                        elif y2 > upper_miny and y3 > upper_miny:
                                second = ["upper", 3]
                        elif y2 < lower_maxy and y3 < lower_maxy:
                                second = ["lower", 3]
			elif isbody(x2, y2) and isbody(x3, y3):
				second = ["wall", 3]
                        else:
                                second = ["inlet", 3]



		element_boundary_sides[e] = first + second

		print x1, y1, x2, y2, x3, y3, first + second, b_idxs
		#print element_boundary_sides[e]

#print element_boundary_sides



print("27484: ", element_boundary_sides[27483])
print("43904: ", element_boundary_sides[43903])


name = outfile #"converted_2.brch" 
path = "/scratch/leuven/338/vsc33811/Lore/dats/"
#name = "sub1_5.brch"

block_type = "Walpot"
ngrps = 1
nbsets = 4
ndfcd = 2
ndfvl = 2

#1 inlet
#2 outlet
#3 wall
#4 sym

nodes_final = []
elems_final = []
boundaries_final = []

for i in range(0, no_points_filtered):
	nodes_final.append([i, xs_filtered[i], ys_filtered[i], zs_filtered[i]]) 

for i in range(0, no_elements):
	element = elements_merged_corrected[i]
	elems_final.append([i, element[0], element[1], element[2], element[3]]) 


count_three = 0
for i in range(0, no_elements):
	if element_boundary_sides[i] != [-1]: 
	 	if len(element_boundary_sides[i]) == 2:	
			if element_boundary_sides[i][0] == "inlet":
				flag = 1
			elif element_boundary_sides[i][0] == "outlet":  
				flag = 2
			elif element_boundary_sides[i][0] == "wall":
				flag = 3
			else:
				flag = 4

			side = element_boundary_sides[i][1]

			boundaries_final.append([i, flag, side])


		elif len(element_boundary_sides[i]) == 4:
			count_three = count_three + 1
                        if element_boundary_sides[i][0] == "inlet":
                                flag = 1
                        elif element_boundary_sides[i][0] == "outlet": 
                                flag = 2
                        elif element_boundary_sides[i][0] == "wall":
                                flag = 3
                        else:
                                flag = 4

                        side = element_boundary_sides[i][1]

                        boundaries_final.append([i, flag, side])

                        if element_boundary_sides[i][2] == "inlet":
                                flag = 1
                        elif element_boundary_sides[i][2] == "outlet":
                                flag = 2
                        elif element_boundary_sides[i][2] == "wall":
                                flag = 3
                        else:
                                flag = 4

                        side = element_boundary_sides[i][3]

                        boundaries_final.append([i, flag, side])

		else:
			print("PROBLEM")


if count_three != 5:
	print("Problem somewhere!") 
		

#print(elems_formatted[0])
written = writeMesh(path, name, block_type, elems_final, nodes_final, boundaries_final, ngrps, nbsets, ndfcd, ndfvl)





