import sqlite3
import pandas as pd
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
    ischoice = Column(Integer)

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return f"<Student(stu_name={self.stu_name},stu_phone={self.stu_phone},\
            par_name={self.par_name},par_phone={self.par_phone},\
                dormitory={self.dormitory},address={self.address},\
                    ischoice={self.ischoice}>"


# 定义sys的ORM影响
class SysParam(Base):
    __tablename__ = "sys_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator = Column(String(32))
    department = Column(String(16))
    class_name = Column(String(16))
    week = Column(Integer)
    reason = Column(String(64))
    option = Column(Integer)

    def __repr__(self):
        return f"<SysParam(creator={self.creator},department={self.department},class_name={self.class_name},week={self.week},reason={self.reason},option={self.option}"


# 读取excle
def read_xlsx(file_name):
    # 传入文件名，读取excle文件
    xls = pd.ExcelFile(file_name)
    # 把第一个工作表除第一行外，读作学生信息，第二个工作表除第一行外，读作系统信息
    stu_info = xls.parse(0)
    sys_info = xls.parse(1)

    return sys_info, stu_info


# 写入数据库，形参：pandas对象、数据库名、表名
def to_sql(df):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    # 建立table
    Base.metadata.create_all(engine)
    # 建立session对象
    Session = sessionmaker(bind=engine)
    session = Session()

    # 数据写入数据库
    for row in df.values:
        student_obj = Student(
            stu_name=row[0],
            stu_phone=row[1],
            par_name=row[2],
            par_phone=row[3],
            dormitory=row[4],
            address=row[5],
            ischoice=row[6],
        )
        session.add(student_obj)

    # 保存
    session.commit()
    session.close()


# 读取数据库中的数据
def out_sql(table_name):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    sql_command = f"select * from {table_name}"
    return pd.read_sql(sql_command, engine)


# 文件下载
def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载 {file_label}</a>'
    return href


if __name__ == "__main__":
    # 从excel导入数据到数据库
    # to_sql(read_xlsx("./students_info.xlsx")[1])
    print(out_sql("sys_info"))
    print(out_sql("stu_info"))
