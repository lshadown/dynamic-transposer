"""HELLO CLI
Usage:
    hello.py
    hello.py <name>
    hello.py -h|--help
    hello.py -v|--version
Options:
    <name>  Optional name argument.
    -h --help  Show this screen.
    -v --version  Show version.
"""
import re
from docopt import docopt

pattern_for_iter = "[a-zA-Z]={1}[a-zA-Z1-9/+\-*]+;{1}"
pattern_matrix = "[A-Z]\[{1}[a-z+\-*1-9]+\]{1}\[{1}[a-z+\-*1-9]+\]{1}"
pattern_iterator = "[a-zA-Z]+[+\-/]{1}[a-zA-Z1-9]"
pattern_special_operator = "[+\-*/]{1}"


def get_special_line(line, tran_matrix, name_matrix):
    matrix = line.split("=")[0]
    first_itr = matrix.split("[")[1].split("]")[0]
    sec_itr = matrix.split("[")[2].split("]")[0]
    return tran_matrix + "[" + sec_itr + "]" + "[" + first_itr + "]" + "=" + name_matrix + "[" + first_itr + "]" + "[" + sec_itr + "]"


def save_to_file(line):
    with open('result.txt') as fobj:
        text = fobj.read()
    with open('result.txt', 'a+') as fobj:
        if not text.endswith('\n'):
            fobj.write('\n')
        fobj.write(line)


def read_file(file_path):
    dic_iter = {}
    iter = 1
    with open(file_path) as fp:
        line = fp.readline()
        line_number = 1
        special_line = None
        while line:
            print("Line {} : {}".format(line_number, line))
            line_code = line.replace(" ", "")
            new_line = line
            result = re.search(pattern_for_iter, line_code)
            if result is not None:
                dic_iter[result.group().split('=')[0]] = iter
                iter += 1
                print("Result: {}".format(result.group()))
            else:
                if len(dic_iter) > 0:
                    # TODO check line
                    result_matrix = re.findall(pattern_matrix, line)
                    if len(result_matrix) > 0:
                        for i in range(len(result_matrix)):
                            name_matrix = ''
                            tab_f = result_matrix[i].split("[")
                            for j in range(len(tab_f)):
                                if len(tab_f[j].split("]")) == 1:
                                    name_matrix = tab_f[j]
                                    print("")
                                elif len(tab_f[j].split("]")) == 2:
                                    it_matrix = tab_f[j].split("]")[0]
                                    is_test = re.search(pattern_iterator, it_matrix)
                                    if is_test is not None:
                                        index_spec = re.search(pattern_special_operator, it_matrix).start()
                                        it_first = it_matrix.split(it_matrix[index_spec])[0]
                                    else:
                                        it_first = it_matrix
                                    it_matrix2 = tab_f[j+1].split("]")[0]
                                    is_test2 = re.search(pattern_iterator, it_matrix2)
                                    if is_test2 is not None:
                                        index_spec2 = re.search(pattern_special_operator, it_matrix2).start()
                                        it_secon = it_matrix2.split(it_matrix2[index_spec2])[0]
                                    else:
                                        it_secon = it_matrix2
                                    if dic_iter[it_first] < dic_iter[it_secon]:
                                        print("Wszystko ok ")
                                    else:
                                        new_value = name_matrix + 'T' + '[' + it_matrix2 + ']' + '[' + it_matrix + ']'
                                        new_line = line.replace(result_matrix[i], new_value)
                                        special_line = name_matrix
                                        print("Trzeba zmieniać")
                                    break

                                print(tab_f[j])

                        print(result_matrix)
            save_to_file(new_line)
            if special_line is not None:
                if line.split("=")[0].split("[")[0].replace(" ", "") == special_line:
                    save_to_file(get_special_line(line, special_line + "T", special_line))
                    special_line = None
            line = fp.readline()
            line_number += 1


if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')
    if arguments['<name>']:
        read_file(arguments['<name>'])
    else:
        print(arguments)