import sqlite3
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 建立ORM基础类
Base = declarative_base()


# 定义ORM映射
class Student(Base):
    # 指定本类映射到stu_info表
    __tablename__ = "stu_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    stu_name = Column(String(10))
    stu_phone = Column(String(16))
    par_name = Column(String(10))
    par_phone = Column(String(16))
    dormitory = Column(String(10))
    address = Column(String(32))
    ischoice = Column(Integer)

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return f"<User(stu_name={self.stu_name},stu_phone={self.stu_phone},\
            par_name={self.par_name},par_phone={self.par_phone},\
                dormitory={self.dormitory},address={self.address},\
                    ischoice={self.ischoice}>"


# def con_sqlite3(db_name):
#     # 创建链接
#     conn = sqlite3.connect(db_name)
#     # 创建数据库游标
#     # cur = conn.cursor()
#     # 创建查询语句
#     sql_str = 'select * from sys_info'
#     # # 执行查询语句
#     # cur.execute(sql_str)
#     # result = cur.fetchall()
#     # print(result)

#     df = pd.read_sql(sql_str, conn)
#     print(df)


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
    engine = create_engine(f"sqlite:///myDB.db", echo=True)
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


# 文件下载
def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载 {file_label}</a>'
    return href


if __name__ == "__main__":
    info_tuple = read_xlsx("./students_info.xlsx")
    to_sql(info_tuple[1])
    pass
