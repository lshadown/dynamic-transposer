import getopt
import sys

from optimization import Optimization

pattern_for_iter = "[a-zA-Z]={1}[a-zA-Z1-9/+\-*]+;{1}"
pattern_matrix = "[A-Z]\[{1}[a-z+\-*1-9]+\]{1}\[{1}[a-z+\-*1-9]+\]{1}"
pattern_iterator = "[a-zA-Z]+[+\-/]{1}[a-zA-Z1-9]"
pattern_special_operator = "[+\-*/]{1}"


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('app.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('app.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    opt = Optimization(input_file, output_file)
    opt.optimization_for()


if __name__ == '__main__':
    main(sys.argv[1:])
