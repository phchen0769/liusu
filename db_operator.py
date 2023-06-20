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

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return f"<Student(stu_name={self.stu_name},stu_phone={self.stu_phone},\
            par_name={self.par_name},par_phone={self.par_phone},\
                dormitory={self.dormitory},address={self.address}>"


# 定义sys的ORM映射
class SysParam(Base):
    __tablename__ = "sys_info"
    id = Column(Integer, primary_key=True)
    creater = Column(String(32))
    department = Column(Integer)
    class_name = Column(String(16))
    week = Column(Integer)
    reason = Column(String(64))
    option = Column(Integer)

    def __repr__(self):
        return f"<SysParam(id={self.id},creater={self.creater},department={self.department},class_name={self.class_name},week={self.week},reason={self.reason},option={self.option}"


# 定义sn_num的ORM映射
class SNNum(Base):
    __tablename__ = "sn_num"
    id = Column(Integer, primary_key=True)
    sn_num = Column(String(64))

    def __repr__(self):
        return f"<SNNum(id={self.id},sn_num={self.sn_num}"


# 读取excle
def read_xlsx(file_name):
    # 传入文件名，读取excle文件
    xls = pd.ExcelFile(file_name)
    # 把第一个工作表除第一行外，读作学生信息，第二个工作表除第一行外，读作系统信息
    stu_info = xls.parse(0)
    sys_info = xls.parse(1)

    return sys_info, stu_info


# excel导入数据库表sys_info
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
        options = (
            "申请临时留宿",
            "申请临时不留宿",
            "申请长期留宿",
            "申请取消长期留宿",
        )
        departments = ("信息技术系", "机电技术系", "财经商贸系", "公共基础部")

        sys_obj = SysParam(
            id=row[0],
            creater=row[1],
            department=departments.index(row[2]),
            class_name=row[3],
            week=row[4],
            reason=row[5],
            option=options.index(row[6]),
        )
        session.add(sys_obj)

    # 保存
    session.commit()
    session.close()


# excel导入数据库表stu_info
def to_sql_stu_info(stu_info_df):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    # 建立table
    # Base.metadata.create_all(engine)
    # 建立session对象
    Session = sessionmaker(bind=engine)
    session = Session()

    # 数据写入数据库
    for row in stu_info_df.values:
        student_obj = Student(
            id=row[0],
            stu_name=row[1],
            stu_phone=row[2],
            par_name=row[3],
            par_phone=row[4],
            dormitory=row[5],
            address=row[6],
        )
        session.add(student_obj)

    # 保存
    session.commit()
    session.close()
    return True


# 读取数据库中的数据
# @st.cache_data
def out_sql(table_name):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    sql_command = f"select * from {table_name}"
    return pd.read_sql(sql_command, engine)


# 清空stu_info数据表中的数据
def del_data(id):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    if id:
        session.query(Student).filter(Student.id == id).delete()
    else:
        session.query(Student).delete()
    session.commit()
    session.close()
    return True


# 保存系统配置到sys_info表
def update_sys_info_table(sys_info_df):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)

    # 建立session对象
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

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


# 保存序列号到sn_num表
def update_sn_num_table(sn_num):
    # 创建数据库连接引擎
    engine = create_engine("sqlite:///myDB.db", echo=True)

    # 建立session对象
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    # 新增数据
    session.query(SNNum).filter_by(id=1).update(
        {
            SNNum.sn_num: sn_num,
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
