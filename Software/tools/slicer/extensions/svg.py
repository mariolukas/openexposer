__author__ = 'mariolukas'
from xml.dom import minidom

class Extension():

        y_precision = 10
        x_precision = 10

        print_bed_width = 330
        print_bed_height = 160
        layers = []
        g_code_file = []

        def __init__(self, file):

            self.file = file
            self.svg_doc = minidom.parse(file)
            self.height = self.getSVGHeight()
            self.width =  self.getSVGWidth()
            self.distances = None

            print "SVG EXTENSION"

            print "Extensions loaded"

        def debug_output(self,layer):
               i = 0
               for distance_line in layer['distances']:
                   if len(distance_line) == 0:
                       print "empty line"

                   if (len(distance_line) %2 != 0):

                       print "Intersections " + str(layer['intersection_points'][i])
                       print "Distances "+str(distance_line)
                   i = i+1

        def create_gcode(self,output_file_name):
            f = open(output_file_name,'w')

            print("Creating G-Code")
            layers =  self.parse_data()

            # home y
            f.write('G30;\n')

            # home z
            f.write('G29;\n')
            f.write("G01 Z-0.2 F20000;\n")
            # move to y start position, begin of stage
            f.write("G01 Y-15 F8000;\n")

            # activate laser active
            f.write('M19;\n')
            # create G-Code for layers with distances
            for layer in layers:


               print "Generating G-Code for layer " +str(layer['layer']+1) + " of "+ str(len(layers))

               #generate intersectsions
               layer = self.calculate_intersections(layer)

               #calculate distances for intersection points
               layer = self.calculate_distances(layer)

               #self.debug_output(layer)

               #write layer name as comment
               f.write(";Layer "+str(layer['layer'])+"\n")

               # generate exposing and moves for one layer
               # forward and backward
               if(layer['layer'] <= len(layers)):

                   for distance_line in layer['distances']:
                     if len(distance_line) > 0:

                         for distance in distance_line:
                             f.write("G05 D"+str(distance)+";\n")

                         f.write("G05 D0;\n")

                         #set exposing time for layer 1 else default
                         if (layer['layer'] == 0):
                             exposing_delay = 400
                         else:
                             exposing_delay = 100

                         f.write("G06 E"+str(exposing_delay)+";\n")

                     if (layer['layer'] %2) == 0:
                        f.write("G01 Y-0.1 F1400;\n")
                     else:
                        f.write("G01 Y0.1 F1400;\n")

                   #move to next layer
                   flow_value = 3
                   f.write("G01 Z-"+str(flow_value)+" F30000;\n")
                   f.write("G03 D400;\n")
                   #print float(layer['height']*1000000)
                   f.write("G01 Z"+str((flow_value - (layer['height']*1000000)*1))+" F30000;\n")

            #print done move z to end position
            #f.write("G03 Z100;\n")

            f.close()

            print "G-Code written to file: "+ str(output_file_name)

        def calculate_intersections(self, layer):

            if(layer['layer']%2==0):
                first_line = 1
                last_line = self.height
                count = 1
            else:
                first_line = self.height-1
                last_line = 0
                count = -1

            for row in xrange(first_line,last_line, count):

                for polygon in layer['polygons']:
                    layer['intersection_points'].append(self.scan_line(polygon,row))
                    #layer['intersection_points'].sort()

            return layer

        def calculate_distances(self,layer):

            offset = (self.print_bed_width)/2 - (self.width)/2
            offset_end = self.print_bed_width

            for intersections_of_line in layer['intersection_points']:


                # calculate offset for x position of object on printbed
                # TODO: we have to calculate a real offset which centers the object on printbed

                for i  in xrange(0,len(intersections_of_line)):
                    intersections_of_line[i] = intersections_of_line[i] + offset
                    #intersection_points[i] = intersection_points[i]


                # add begin and end point to intersection points
                if len(intersections_of_line) > 0:
                    if 0 not in intersections_of_line:
                        intersections_of_line.insert(0,0)

                    if offset_end not in intersections_of_line:
                        intersections_of_line.append(offset_end)


                i = 0

                distances = []
                # now calculate distances

                while i < len(intersections_of_line)-1:

                    distance = intersections_of_line[i+1] - intersections_of_line[i]

                    if int(distance * self.x_precision) == 0:
                        distance = intersections_of_line[i+2] - intersections_of_line[i-1]

                    i = i+1

                    distances.append(int(distance * self.x_precision))

                #remove the last distance, from last intersection point to end is
                #not needed...
                if len(distances) > 0:
                    distances.pop()

                layer['distances'].append(distances)


            return layer


        ''' convert polygon points from string to float tuple'''
        def convertStringToFloatPoints(self,points):
            converted_points = []
            if len(points) is not 0:
                points = points = points.split(' ')
                for point in points:
                    x_y_coord = point.split(',')
                    converted_points.append((float(x_y_coord[0]),float(x_y_coord[1])))
            return converted_points

        ''' cleans the intersection list '''
        def cleanNodes(self,xNodes):
            xNodes.sort()
            xNodes = self.removeDuplicateNodes(xNodes)
            return xNodes

        ''' removes nodes '''
        def removeDuplicateNodes(self,nodes):
            remove_nodes = []
            for i, elem in enumerate(nodes):
                if elem in nodes[i+1:]:
                   remove_nodes.append(elem)

            nodes = [p for p in nodes if p not in remove_nodes]

            return nodes


        '''
            scanline algorithm
            returns list of x intersection points one polygon for a row
        '''
        def scan_line(self,points,y_line):

            X = 0
            Y = 1
            intersection_points = []

            y_line = float(y_line)/self.y_precision

            j = len(points)-1
            for i in xrange(0,len(points)):
               if (points[i][Y] < float(y_line) and points[j][Y] >= float(y_line)
                   or points[j][Y] < float(y_line) and points[i][Y] >= float(y_line)):
                    ## add x position of intersection to list
                    new_point = float(points[i][X]+(y_line-points[i][Y])/(points[j][Y]-points[i][Y])*(points[j][X]-points[i][X]))
                    new_point = float(new_point)
                    intersection_points.append(new_point)
               j = i

            intersection_points = self.cleanNodes(intersection_points)
            return intersection_points

        def get_layer_height(self, layers):
            first_layer_height = layers[0].attributes["slic3r:z"]
            second_layer_height = layers[1].attributes["slic3r:z"]

            height  = float(second_layer_height.value) - float(first_layer_height.value)

            return height

        def get_layer_array(self, doc):

            layers = []

            layers_in_svg = doc.getElementsByTagName('g')

            i = 0
            for layer_in_svg in layers_in_svg:

                layer = dict()
                # ugly hack to get layer number
                # TODO: Parse Layer id and get real layer number
                layer['layer'] = i
                i = i+1

                layer['distances'] = []
                layer['intersection_points'] = []
                layer['polygons'] = []
                # ugly hack to calculate layer by difference of first and second layer
                # works only if all layers have the same height.
                # TODO: Calculate real layer height for each layer!
                layer['height'] = self.get_layer_height(layers_in_svg)

                polygons = layer_in_svg.getElementsByTagName('polygon')
                for polygon in polygons:
                    points = polygon.getAttribute('points')
                    points = self.convertStringToFloatPoints(points)
                    layer['polygons'].append(points)

                layers.append(layer)

            return layers

        def parse_data(self):
            print "Parsing SVG File"
            return self.get_layer_array(self.svg_doc)


        ''' get SVG width '''
        def getSVGWidth(self):
            width = [svg_root.getAttribute('width') for svg_root in self.svg_doc.getElementsByTagName('svg')][0]
            width = float(width)
            return width

        ''' get SVG Height  '''
        def getSVGHeight(self):
            height = [svg_root.getAttribute('height') for svg_root in self.svg_doc.getElementsByTagName('svg')][0]
            height = int(float(height)*self.y_precision)
            return height