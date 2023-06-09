#  导入xlsx处理模块
from shutil import ReadError
import openpyxl
import json


# 读取根目录下的配置文件
def read_config(fileName):
    # 读取配置
    with open(fileName, encoding="utf-8") as json_file:
        config = json.load(json_file)
    return config


# 读取excel表中的内容
def readXlsx(xlsx_name):
    # 读取excel表
    try:
        book = openpyxl.load_workbook(xlsx_name)
        # 返回当前工作表对象
        return book.worksheets
    except ReadError:
        print("Open xlsx error!")


# 接收一个工作表对象，返回该工作表内容的列表
def createRunningParamList(sheet2):
    # 读取第二个工作表中的参数，并生成参数列表
    RunningParamList = []
    for cell in sheet2["B"]:
        RunningParamList.append(str(cell.value))
    return RunningParamList


# 接收一个工作表对象,返回该工作表内容的字典
def createStudentInfoDis(sheet1):
    # 计算机excel表中的有效人数
    rowNum = 1  # 记录当前访问的行号
    rowNum_list = []  # 行号列表

    # 第"H"格内容是判断excel表中学生是否留宿
    for cell in sheet1["H"]:
        if cell.value == "是":
            rowNum_list.append(rowNum)
        rowNum += 1

    # 如果学生人数符合要求，读取工作表内容并转换成字典列表（大于等于1，同时小于等于10）
    rowNum_listLenth = len(rowNum_list)

    # 批量生成多个字典
    student_info_dics = [
        dict(
            [
                ("name", ""),
                ("phone", ""),
                ("parent", ""),
                ("parentPhone", ""),
                ("dormitory", ""),
                ("address", ""),
            ]
        )
        for i in range(rowNum_listLenth)
    ]

    i = 0
    # 读取列表中的行号，把列对应内容,存储到字典列表对应的字段中
    for rowNum in rowNum_list:
        student_info_dics[i]["name"] = str(sheet1[rowNum][1].value).strip()
        student_info_dics[i]["phone"] = str(sheet1[rowNum][2].value).strip()
        student_info_dics[i]["parent"] = str(sheet1[rowNum][3].value).strip()
        student_info_dics[i]["parentPhone"] = str(sheet1[rowNum][4].value).strip()
        student_info_dics[i]["dormitory"] = str(sheet1[rowNum][5].value).strip()
        student_info_dics[i]["address"] = str(sheet1[rowNum][6].value).strip()
        i += 1
    return student_info_dics


if __name__ == "__main__":
    # 读取excel表，返回工作表列表
    sheetsList = readXlsx("./students_info.xlsx")
    student_info_list = createStudentInfoDis(sheetsList[0])
    running_Param_List = createRunningParamList(sheetsList[1])
    print(student_info_list)
    print(running_Param_List)
