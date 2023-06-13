import sqlite3
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 建立ORM基础类
Base = declarative_base()


# 定义Student的ORM映射
class Student(Base):
    # 指定本类映射到stu_info表
    __tablename__ = "stu_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形
    stu_name = Column(String(10))
    stu_phone = Column(String(16))
    par_name = Column(String(10))
    par_phone = Column(String(16))
    dormitory = Column(String(10))
    address = Column(String(32))

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return f"<Student(stu_name={self.stu_name},stu_phone={self.stu_phone},\
            par_name={self.par_name},par_phone={self.par_phone},\
                dormitory={self.dormitory},address={self.address}>"


# 定义sys的ORM影响
class SysParam(Base):
    __tablename__ = "sys_info"
    id = Column(Integer, primary_key=True)
    creater = Column(String(32))
    department = Column(String(16))
    class_name = Column(String(16))
    week = Column(Integer)
    reason = Column(String(64))
    option = Column(String(16))

    def __repr__(self):
        return f"<SysParam(creater={self.creater},department={self.department},class_name={self.class_name},week={self.week},reason={self.reason},option={self.option}"


# 读取excle
@st.cache_data
def read_xlsx(file_name):
    # 传入文件名，读取excle文件
    xls = pd.ExcelFile(file_name)
    # 把第一个工作表除第一行外，读作学生信息，第二个工作表除第一行外，读作系统信息
    stu_info = xls.parse(0)
    sys_info = xls.parse(1)

    return sys_info, stu_info


# 以追加的形式，写入数据库
def to_sql_sys_info(sys_info_df):
    """
    sys_info_df: df_object()=>none
    """
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    # 建立table
    Base.metadata.create_all(engine)
    # 建立session对象
    Session = sessionmaker(bind=engine)
    session = Session()

    # 数据写入数据库
    for row in sys_info_df.values:
        sys_obj = SysParam(
            creater=row[0],
            department=row[1],
            class_name=row[2],
            week=row[3],
            reason=row[4],
            option=row[5],
        )
        session.add(sys_obj)

    # 保存
    session.commit()
    session.close()


# 写入数据库，形参：pandas对象、数据库名、表名
def to_sql_stu_info(stu_info_df):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    # 建立table
    Base.metadata.create_all(engine)
    # 建立session对象
    Session = sessionmaker(bind=engine)
    session = Session()

    # 数据写入数据库
    for row in stu_info_df.values:
        student_obj = Student(
            stu_name=row[0],
            stu_phone=row[1],
            par_name=row[2],
            par_phone=row[3],
            dormitory=row[4],
            address=row[5],
        )
        session.add(student_obj)

    # 保存
    session.commit()
    session.close()


# 读取数据库中的数据
# @st.cache_data
def out_sql(table_name):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    sql_command = f"select * from {table_name}"
    return pd.read_sql(sql_command, engine)


# def del_table(table_name):
#     # 创建数据库连接引擎
#     engine = create_engine("sqlite:///myDB.db", echo=True)
#     sql_command = f"drop table {table_name}"


def update_sys_info_table(sys_info_df):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    Base.metadata.create_all(engine)
    # Base = declarative_base()
    # 建立session对象
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    # Base = declarative_base()
    # 新增数据
    session.query(SysParam).filter_by(id=1).update(
        {
            SysParam.creater: sys_info_df.values[0][0],
            SysParam.department: sys_info_df.values[0][1],
            SysParam.class_name: sys_info_df.values[0][2],
            SysParam.week: sys_info_df.values[0][3],
            SysParam.reason: sys_info_df.values[0][4],
            SysParam.option: sys_info_df.values[0][5],
        }
    )
    session.commit()
    session.close()
    return True


if __name__ == "__main__":
    # 从excel导入数据到数据库
    to_sql_stu_info(read_xlsx("./students_info.xlsx")[1])
    to_sql_sys_info(read_xlsx("./students_info.xlsx")[0])
    print(out_sql("sys_info"))
    print(out_sql("stu_info"))
