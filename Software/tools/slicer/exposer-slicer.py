__author__ = 'mariolukas'
import optparse
import imp
import os.path
import sys

def importFromURI(self, uri, absl=False):
	if not absl:
		uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
	path, fname = os.path.split(uri)
	mname, ext = os.path.splitext(fname)

	no_ext = os.path.join(path, mname)

	if os.path.exists(no_ext + '.pyc'):
		try:
			return imp.load_compiled(mname, no_ext + '.pyc')
		except:
			pass
	if os.path.exists(no_ext + '.py'):
		try:
			return imp.load_source(mname, no_ext + '.py')
		except:
			pass

def main():
    parser = optparse.OptionParser("exposer-send <options>");
    parser.add_option("-f","--file", action = "store", type="string", dest="input_file", help="Input File e.x. test.svg")
    parser.add_option("-e","--extension", action = "store", type="string", dest="extension", default="svg", help="Extension Type e.g. SVG, EAGLE")
    parser.add_option("-o","--output", action = "store", type="string", dest="output_file", default="output.gcode", help="Output G-code Filename")


    (options, target) = parser.parse_args()

    input_file = options.input_file
    output_file = options.output_file
    extenstion = options.extension

    if not os.path.isfile(options.input_file):
        print str(options.input_file)+" file not found"
        sys.exit()

    #extenstions = imp.load_source("module", 'extensions/'+options.extension+'.py')
    import extensions.svg
    extension = extensions.svg.Extension(options.input_file)
    extension.create_gcode(options.output_file)

    print "Done"


if __name__=="__main__":
    main()
