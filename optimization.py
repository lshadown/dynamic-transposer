import re

from process_line import ProcessLine


class Optimization:
    _pattern_for_iter = "[a-zA-Z]={1}[a-zA-Z0-9/+\-*]+;{1}"
    _pattern_matrix = "[A-Z]\[{1}[a-z+\-*1-9]+\]{1}\[{1}[a-z+\-*1-9]+\]{1}"
    _pattern_iterator = "[a-zA-Z]+[+\-/]{1}[a-zA-Z1-9]"
    _pattern_special_operator = "[+\-*/]{1}"

    _format_special_line = "{}[{}][{}] = {}[{}][{}]"

    def __init__(self, input_file_path, output_file_path):
        self._input_file_path = input_file_path
        self._output_file_path = output_file_path

    def optimization_for(self):
        self._read_file()

    def _save_to_file(self, line):
        with open(self._output_file_path) as fobj:
            text = fobj.read()
        with open(self._output_file_path, 'a+') as fobj:
            if not text.endswith('\n'):
                fobj.write('\n')
            fobj.write(line)

    def _get_special_line(self, line, tran_matrix, name_matrix):
        matrix = line.split("=")[0]
        first_itr = matrix.split("[")[1].split("]")[0]
        sec_itr = matrix.split("[")[2].split("]")[0]
        return self._format_special_line.format(tran_matrix, sec_itr, first_itr, name_matrix, first_itr, sec_itr)

    def _process_line(self, line, dictionary_iter):
        result_line = line;
        result_special_line = None
        if len(dictionary_iter) > 0:
            result_matrix = re.findall(self._pattern_matrix, line)
            if len(result_matrix) > 0:
                for i in range(len(result_matrix)):
                    name_matrix = ''
                    tab_f = result_matrix[i].split("[")
                    for j in range(len(tab_f)):
                        if len(tab_f[j].split("]")) == 1:
                            name_matrix = tab_f[j]
                        elif len(tab_f[j].split("]")) == 2:
                            it_matrix = tab_f[j].split("]")[0]
                            is_spec_first = re.search(self._pattern_iterator, it_matrix)
                            if is_spec_first is not None:
                                index_spec_first = re.search(self._pattern_special_operator, it_matrix).start()
                                it_first = it_matrix.split(it_matrix[index_spec_first])[0]
                            else:
                                it_first = it_matrix
                            it_matrix2 = tab_f[j + 1].split("]")[0]
                            is_spec_sec = re.search(self._pattern_iterator, it_matrix2)
                            if is_spec_sec is not None:
                                index_spec_sec = re.search(self._pattern_special_operator, it_matrix2).start()
                                it_sec = it_matrix2.split(it_matrix2[index_spec_sec])[0]
                            else:
                                it_sec = it_matrix2
                            if dictionary_iter[it_first] > dictionary_iter[it_sec]:
                                new_value = name_matrix + 'T' + '[' + it_matrix2 + ']' + '[' + it_matrix + ']'
                                result_line = line.replace(result_matrix[i], new_value)
                                result_special_line = name_matrix
                            break

                        print(tab_f[j])

                print(result_matrix)
        return ProcessLine(result_line, result_special_line)

    def _read_file(self):
        dic_iter = {}
        iter = 1
        with open(self._input_file_path) as fp:
            line = fp.readline()
            line_number = 1
            special_line = None
            while line:
                print("Line {} : {}".format(line_number, line))
                line_code = line.replace(" ", "")
                new_line = line
                result = re.search(self._pattern_for_iter, line_code)
                if result is not None:
                    dic_iter[result.group().split('=')[0]] = iter
                    iter += 1
                    print("Result: {}".format(result.group()))
                else:
                    result = self._process_line(line, dic_iter)
                    if result is not None:
                        new_line = result.line
                        if result.special_line is not None:
                            special_line = result.special_line
                self._save_to_file(new_line)
                if special_line is not None:
                    if line.split("=")[0].split("[")[0].replace(" ", "") == special_line:
                        self._save_to_file(self._get_special_line(line, special_line + "T", special_line))
                        special_line = None
                line = fp.readline()
                line_number += 1
