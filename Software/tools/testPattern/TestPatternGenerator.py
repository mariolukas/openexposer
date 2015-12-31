__author__ = 'christoph'

from optparse import OptionParser


def pre_object(options):
    #;Home Y und Z
    print("G30;")
    print("G29;")
    #; Z anheben auf 0.1 mm ueber Null fuer erste Schicht
    print("G01 Z-%d F%d;" % (options.layer_height, options.retraction_speed))
    # fahren bis zur Beckenmitte abzueglich halbe hoehe des objekts

    printing_area_start_depth = (options.bed_depth/2) - (options.depth/2)
    print("G01 Y%d F8000;" % printing_area_start_depth)

def post_object(options):
    pass

def pre_layer(options, reverse=False):
    #; Laser an.
    print("M19;")


def post_layer(options, reverse=False):
    #; Laser aus.
    print("M20;")
    #; Servo kippen  und halten
    print("M21;")
    #; Z heben um harz nachfliessen zu lassen
    print("G01 Z-%d F%d;" % (options.retraction_height, options.retraction_speed))
    #; Servo zurueck kippen
    print("M22;")
    #; Z zurueck fahren abzueglich des Abstands einer Schicht hoehe.
    print("G01 Z%d F%d;" % (options.retraction_height-options.layer_height, options.retraction_speed))


def create_layer(options, reverse=False):
    for line in range(0, options.depth/options.thickness):
        #; Zur naechsen Linie
        if reverse:
            print("G01 Y-%d F1400;" % options.thickness)
        else:
            print("G01 Y%d F1400;" % options.thickness)
        if line*options.thickness<options.gutter_width or line*options.thickness>(options.depth-options.gutter_width):
            draw_full_line(options)
        else:
            draw_segmented_line(options)


def draw_segmented_line(options):
    printing_area_start_width = (options.bed_width/2) - (options.width/2)

    #; Erster Wert bis Wuerfel start
    print("G05 D%d;" % printing_area_start_width)

    remaining_width = options.width
    gutter_width = options.gutter_width
    column_width = 1

    while remaining_width >= column_width+gutter_width:
        print("G05 D%d;" % gutter_width)
        print("G05 D%d;" % column_width)
        remaining_width -= (column_width+gutter_width)
        column_width *= 2

    if remaining_width > 2*gutter_width:
        remaining_column_width = remaining_width - gutter_width*2
        print("G05 D%d;" % gutter_width)
        print("G05 D%d;" % remaining_column_width)
        print("G05 D%d;" % gutter_width)
    else:
        # beenden, es passt keine Spalte mehr dahinter
        print("G05 D%d;" % remaining_width)

    #; Letzter Wert 0
    print("G05 D0;")
    #; Belichte 100 Zykel ( Wert kann stark variieren je nach harz erste schickt immer viel laenger )
    print("G06 E%d;" % options.cycles)


def draw_full_line(options):
    printing_area_start_width = (options.bed_width/2) - (options.width/2)

    #; Erster Wert bis Wuerfel start
    print("G05 D%d;" % printing_area_start_width)

    print("G05 D%d;" % options.width)

    #; Letzter Wert 0
    print("G05 D0;")
    #; Belichte 100 Zykel ( Wert kann stark variieren je nach harz erste schickt immer viel laenger )
    print("G06 E%d;" % options.cycles)


def main():
    parser = OptionParser(add_help_option=False)
    parser.add_option("-l", "--layer-height",
                      dest="layer_height", type='int', action='store', default="10",
                      help="defines the height of one layer")
    parser.add_option("-h", "--height",
                      dest="height", type='int', action='store', default="500",
                      help="defines the height of the whole test pattern")
    parser.add_option("-w", "--width",
                      dest="width", type='int', action='store', default="5000",
                      help="defines the width of the whole test pattern")
    parser.add_option("-d", "--depth",
                      dest="depth", type='int', action='store', default="5000",
                      help="defines the depth of the whole test pattern")
    parser.add_option("-c", "--exposing-cycles",
                      dest="cycles", type='int', action='store', default="100",
                      help="defines the cycles a line is exposed")
    parser.add_option("-t", "--line-thickness",
                      dest="thickness", type='int', action='store', default="10",
                      help="defines the thickness of a line")
    parser.add_option("-g", "--gutter-width",
                      dest="gutter_width", type='int', action='store', default="50",
                      help="defines the width of the gutter between the pattern parts")
    parser.add_option("-r", "--retraction-height",
                      dest="retraction_height", type='int', action='store', default="1000",
                      help="defines the height of the retraction of the platform between the layers")
    parser.add_option("--retraction-speed",
                      dest="retraction_speed", type='int', action='store', default="30000",
                      help="defines the speed of the retraction of the platform between the layers")
    parser.add_option("--bed-width",
                      dest="bed_width", type='int', action='store', default="8000",
                      help="defines the width of the whole printing bed")
    parser.add_option("--bed-depth",
                      dest="bed_depth", type='int', action='store', default="8000",
                      help="defines the depth of the whole printing bed")
    parser.add_option("--help",
                      action='help',
                      help="shows the help")


    (options, args) = parser.parse_args()

    layer_count = options.height / options.layer_height

    pre_object(options)

    reverse = False
    for layer in range(0, layer_count):
        pre_layer(options, reverse=reverse)
        create_layer(options, reverse=reverse)
        post_layer(options, reverse=reverse)
        reverse = not reverse

    post_object(options)

if __name__ == "__main__":
    main()
