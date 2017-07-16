#coding:utf8
import xlrd
from config import *
__metaclass__ = type

class xls:
    def __init__(self, file_name, sheet_name, f_points=1, f_title=()):
        '''
        :param file_name: xls file name
        :param sheet_name: sheet name
        :param f_points: float value's decimal number
        :param f_title: float value's title
        '''
        self.wb = xlrd.open_workbook(file_name, formatting_info=True)
        self.ws = self.wb.sheet_by_name(sheet_name)
        self.f_title = f_title
        self.f_points = f_points

    def _unmergedValue(self,rowx,colx):
        for crange in self.ws.merged_cells:
            rlo, rhi, clo, chi = crange
            if rowx in xrange(rlo, rhi):
                if colx in xrange(clo, chi):
                    return self.ws.cell_value(rlo,clo)
        return self.ws.cell_value(rowx,colx)

    def _fixMergedValue(self, row, nrow):
        for i in range(len(row)):
            if not row[i]:
                row[i] = self._unmergedValue(nrow, i)

    def _formatValue(self, d):
        for title in d:
            if title in self.f_title:  # format points
                d[title] = str(round(float(d[title]), self.f_points))

    def getRowDict(self):
        ''' get row dict with row value and title
            Note: input xls must all text, don't have float value
        '''
        title = self.ws.row_values(0)
        for nrow in range(1, self.ws.nrows):
            row = [i.strip() for i in self.ws.row_values(nrow)]
            self._fixMergedValue(row, nrow)
            row_dict = dict(zip(title, row))
            self._formatValue(row_dict)
            yield row_dict

