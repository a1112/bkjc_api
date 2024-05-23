import openpyxl

import openpyxl

from Base.module import SteelProject


def saveExcel(data, excel_path):
    workbook = openpyxl.load_workbook("template/templateDataOut.xlsx")
    ws1 = workbook.get_sheet_by_name("Sheet1")
    workbook.active = 0  # 设置active参数，即工作表索引值
    for colIndex, dataItem in enumerate(data):
        dataItem: SteelProject
        for rowIndex, value in enumerate([
            dataItem.seqNo,
            dataItem.steelNo,
            dataItem.packageName,
            dataItem.steelType,
            dataItem.steelLength,
            dataItem.steelWidth,
            dataItem.steelThick,
            dataItem.detectTime,
            len(dataItem.level) > 0+1,
            "否" if len(dataItem.level) > 0 else "是",
            dataItem.levelInfo
        ]):
            print(value)
            ws1.cell(colIndex + 2, rowIndex + 1).value = value
            #  流水号	板号	捆包号	钢种	长度	宽度	厚度	检测时间	判级	是否合格	判级原因	人工
    workbook.save(excel_path)


listDatas = []


def getSaveExcelFileName(data):
    return f"out/{data[0].seqNo}~{data[-1].seqNo}.xlsx"


def append(steelInfo):
    global listDatas
    listDatas.append(steelInfo)
    if len(listDatas) >= 100:
        saveExcel(listDatas, getSaveExcelFileName(listDatas))
        listDatas = []

# saveExcel([[1,2,3,4],[1,2,3,3]], "test.xlsx")
