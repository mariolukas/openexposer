from __future__ import division
from xml.dom import minidom

class PolygonSlicer():

    svg_file_path = ""
    svg_doc = ""
    width = 0
    height = 0
    y_precision = 10
    x_precision = 10
    print_bed_width = 100
    print_bed_height = 100


    def __init__(self, svg_file):
        self.svg_file_path = svg_file
        self.svg_doc = minidom.parse(self.svg_file_path)
        self.height = self.getSVGHeight()
        self.width = self.getSVGWidth()

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

    ''' convert polygon points from string to float tuple'''
    def convertStringToFloatPoints(self,points):
        converted_points = []
        if len(points) is not 0:
            points = points = points.split(' ')
            for point in points:
                x_y_coord = point.split(',')
                converted_points.append((float(x_y_coord[0]),float(x_y_coord[1])))
        return converted_points

    ''' counts layers of the SVG file '''
    def countLayers(self):
        layers = self.svg_doc.getElementsByTagName('g')
        layer_count = len(layers)
        return layer_count

    ''' returns a list of all polygons in one layer '''
    def getPolygonsOfLayer(self,layer_id):

        polygon_list = []

        layers = self.svg_doc.getElementsByTagName('g')

        for layer in layers:
            if (layer.getAttribute('id') == "layer"+str(layer_id)):
                polygons = layer.getElementsByTagName('polygon')
                for polygon in polygons:
                    points = polygon.getAttribute('points')
                    points = self.convertStringToFloatPoints(points)
                    polygon_list.append(points)

        return polygon_list


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
        get the laser toggle points for a row
        by iterating over all polygons in a row
    '''
    def getIntersectionPointsForRowOfLayer(self,row, layer):
      intersection_points = []
      polygon_list = self.getPolygonsOfLayer(layer)
      for polygon in polygon_list:
        intersection_points += self.scanLine(polygon,row)
      intersection_points.sort()
      return intersection_points


    def calculateDistances(self,row,layer):
        intersection_points = []
        distances = []
        # calculate offset here default is center now
        offset = self.print_bed_width/2 - self.width/2
        offset_end = self.print_bed_width

        intersection_points = self.getIntersectionPointsForRowOfLayer(row,layer)

        for i  in xrange(0,len(intersection_points)):
            intersection_points[i] = intersection_points[i]+offset

        if len(intersection_points) > 0:
            if 0 not in intersection_points:
                intersection_points.insert(0,0)

            if offset_end not in intersection_points:
                intersection_points.append(offset_end)

        distances = [intersection_points[i+1]-intersection_points[i] for i in range(len(intersection_points)-1)]

        return distances

    def remove_distance_value(self, the_list, val):
        return [value for value in the_list if value != val]

    def getDistances(self,row,layer):
        distances = self.calculateDistances(row,layer)
        for i in xrange(0,len(distances)):
            distances[i] = int(distances[i]*self.x_precision)

        # remove 0 distances
        distances = self.remove_distance_value(distances,0)

        # remove last distance is not needed
        if len(distances) > 0:
            distances.pop()

        return distances


    '''
        scanline algorithm
        returns list of x intersection points one polygon for a row
    '''
    def scanLine(self,points,y_line):
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

