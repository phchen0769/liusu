import json

from db_operator import out_sql


# 通过df对象生成发送内容
def body_create_df(sys_info_df, stu_info_df):
    """
    sys_info_df:df对象()
    stu_info_df:df对象()
    => json
    """

    # 计算需要提交学生的人数
    students_nums = len(stu_info_df)

    # sys_info_df.values[0]中读取第六个参数
    if sys_info_df.values[0][5] == "申请长期留宿":
        # 待发送内容字符串(申请长期留宿)
        body_str = '{"creator_userid": "dgxxcph", "use_template_approver": 0, "approver": [{"attr": 1,"userid": ["dgxx018","dgxx011","dgxx006"]}], "apply_data":{"contents":[{"id":"item-1514443079194","control":"Tips","title":[{"text":"说明","lang":"zh_CN"}],"value":{}},{"id":"item-1514443295417","control":"Text","title":[{"text":"班级","lang":"zh_CN"}],"value":{"text":"测试测试"}},{"id":"item-1514443554457","control":"Table","title":[{"text":"长期留宿名单","lang":"zh_CN"}],"value":{"stat_field":[],"sum_field":[],"children":[{"list":[{"id":"item-1514447041933","control":"Text","title":[{"text":"学生姓名","lang":"zh_CN"}],"value":{"text":"吴立维"}},{"id":"item-1514447082757","control":"Number","title":[{"text":"学生手机","lang":"zh_CN"}],"value":{"new_number":"16620737446"}},{"id":"item-1515031306397","control":"Text","title":[{"text":"家长姓名","lang":"zh_CN"}],"value":{"text":"吴树茂"}},{"id":"item-1514447102677","control":"Number","title":[{"text":"家长手机","lang":"zh_CN"}],"value":{"new_number":"13725756584"}},{"id":"item-1519633346441","control":"Text","title":[{"text":"学生宿舍","lang":"zh_CN"}],"value":{"text":"B215"}},{"id":"item-1514447353628","control":"Textarea","title":[{"text":"家庭住址","lang":"zh_CN"}],"value":{"text":"广西壮族自治区罗城仫佬族自治县东门镇"}},{"id":"item-1514447433852","control":"Tips","title":[{"text":"说明","lang":"zh_CN"}],"value":{}}]}]}},{"id":"item-1514470626560","control":"Tips","title":[{"text":"说明","lang":"zh_CN"}],"value":{}}]},"timezone_info":"","choose_party":{"partyid":"1688851641314945","party_name":"信息技术系"},"template_id":"1970325121005616_1688851641322056_2010055007_1514443043","process_node_list":[{"id":"node_4","type":"APPROVAL","appro":{"type":"APV_TAG","members":{"vids":[]},"leader":{"order":"LOW_2_HIGH","level":1,"recursive_search_leader":true,"skip_empty_leader":true,"vids":[]},"tag":{"tag_ids":["6755403036058772"],"vids":["1688851641322280","1688851641322281","1688851641322310"]},"self":{"vids":[]},"self_select":{"type":"SELF_SELECT_MULTI","range_type":"UN_LIMITED","vids":[]},"apv_rel":"APV_REL_OR","multi_leader":{"part_order":"UP_2_DOWN","level":1,"vids":[]},"member_with_tag":{"part_order":"DOWN_2_UP","level":1,"vids":[]},"member_control":{"vids":[]},"approver_collection":{"vids":[]}},"cc":{"leaders":[]},"name":[{"text":"学生处","lang":"zh_CN"}],"auth_list":[],"self_select_vids":[],"fixed_vids":["1688851641322280","1688851641322281","1688851641322310"],"editable":false,"deleteable":true,"addable":true,"self_select_single":false,"relation":"或签","new_relation":"或签","relation_string":"或签","orderable":false,"icon_class":"approver","is_type_self_select":false,"appro_type":"APV_TAG","name_string":"学生处","members_data":[{"vid":"1688851641322280","name":"黄汉城","avatar":"http://wework.qpic.cn/bizmail/KNK1of2CdelIKu8MzH7rVgzibEts4LFMVQ73SjRhibMajm0gaSchPbmA/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"},{"vid":"1688851641322281","name":"谢培璇","avatar":"https://wework.qpic.cn/wwhead/duc2TvpEgSQO4BpE0WZSZ88x19mvAPmvXKYt4pB3uGWJX0bPtvStVDAibia7hu01kOztaRJhFx4zM/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"},{"vid":"1688851641322310","name":"吴柏柱","avatar":"http://wework.qpic.cn/bizmail/1TF9mZHLhgQmQ60ibxn9CJXGr8PGHTia3Rtglwibxm94JL4PJJMqj0xxA/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"}],"members_self_select":[],"members_all_data":[{"vid":"1688851641322280","name":"黄汉城","avatar":"http://wework.qpic.cn/bizmail/KNK1of2CdelIKu8MzH7rVgzibEts4LFMVQ73SjRhibMajm0gaSchPbmA/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"},{"vid":"1688851641322281","name":"谢培璇","avatar":"https://wework.qpic.cn/wwhead/duc2TvpEgSQO4BpE0WZSZ88x19mvAPmvXKYt4pB3uGWJX0bPtvStVDAibia7hu01kOztaRJhFx4zM/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"},{"vid":"1688851641322310","name":"吴柏柱","avatar":"http://wework.qpic.cn/bizmail/1TF9mZHLhgQmQ60ibxn9CJXGr8PGHTia3Rtglwibxm94JL4PJJMqj0xxA/0","is_delete":false,"is_out_corp":false,"corp_name":"东莞信息技术学校","deleteable":true,"from":"server"}],"lowercase_type":"approval"}],"visual_meta":{"feature_flag_edit":true,"is_approver_change":0,"is_notify_change":0}}'

        # 待发送内容转换成对应的数据结构
        try:
            body_json = json.loads(body_str, strict=False)

        except ValueError as e:
            print(e)

        # children路径
        children_dic = body_json["apply_data"]["contents"][2]["value"]["children"]

    else:
        # 待发送内容字符串(申请临时留宿	申请临时不留宿	申请取消长期留宿)
        body_str = '{"creator_userid": "dgxxcph", "use_template_approver": 0, "approver": [{"attr": 1,"userid": ["dgxx018","dgxx011","dgxx006"]}], "apply_data": {"contents": [{"id": "item-1514447653363", "control": "Tips", "title": [{"text": "说明", "lang": "zh_CN"}], "value": {}}, {"id": "item-1514447662644", "control": "Text", "title": [{"text": "班级", "lang": "zh_CN"}], "value": {"text": "测试测试"}}, {"id": "item-1514447694555", "control": "Number", "title": [{"text": "第几周", "lang": "zh_CN"}], "value": {"new_number": "9999999999"}}, {"id": "item-1514457944110", "control": "Text", "title": [{"text": "申请原因", "lang": "zh_CN"}], "value": {"text": "变更留宿"}}, {"id": "item-1514470343431", "control": "Selector", "title": [{"text": "变更情况", "lang": "zh_CN"}], "value": {"selector": {"options": [{"key": "option-528888885", "value": [{"text": "申请临时留宿", "lang": "zh_CN"}]}], "exp_type": 0, "type": "single"}}}, {"id": "item-1514447722075", "control": "Table", "title": [{"text": "留宿变更名单", "lang": "zh_CN"}], "value": {"stat_field": [], "sum_field": [], "children": [{"list": [{"id": "item-1514447759978", "control": "Text", "title": [{"text": "学生姓名", "lang": "zh_CN"}], "value": {"text": "tttttt"}}, {"id": "item-1514447782658", "control": "Number", "title": [{"text": "学生手机", "lang": "zh_CN"}], "value": {"new_number": "13688888888"}}, {"id": "item-1515031350677", "control": "Text", "title": [{"text": "家长姓名", "lang": "zh_CN"}], "value": {"text": "ttttttttttt"}}, {"id": "item-1514447797634", "control": "Number", "title": [{"text": "家长手机", "lang": "zh_CN"}], "value": {"new_number": "13688888888"}}, {"id": "item-1519633463609", "control": "Text", "title": [{"text": "学生宿舍", "lang": "zh_CN"}], "value": {"text": "Z101"}}, {"id": "item-1514447845515", "control": "Textarea", "title": [{"text": "家庭住址", "lang": "zh_CN"}], "value": {"text": "TTTTTTTT"}}, {"id": "item-1514447882402", "control": "Tips", "title": [{"text": "说明", "lang": "zh_CN"}], "value": {}}]}]}}, {"id": "item-1514533131686", "control": "Tips", "title": [{"text": "说明", "lang": "zh_CN"}], "value": {}}]}, "timezone_info": "", "choose_party": {"partyid": "1688851641314945", "party_name": "信息技术系"}, "template_id": "1970325121005616_1688851641322056_519309562_1514447587", "process_node_list": [{"id": "node_2", "type": "APPROVAL", "appro": {"type": "APV_TAG", "tag": {"tag_ids": ["6755403036058772"], "vids": ["1688851641322280", "1688851641322281", "1688851641322310"]}, "apv_rel": "APV_REL_OR"}, "name": [{"text": "学生处", "lang": "zh_CN"}], "auth_list": [], "self_select_vids": [], "fixed_vids": ["1688851641322280", "1688851641322281", "1688851641322310"], "editable": false, "deleteable": true, "addable": true, "self_select_single": false, "relation": "或签", "new_relation": "或签", "relation_string": "", "orderable": false, "icon_class": "approver", "is_type_self_select": false, "appro_type": "APV_TAG", "name_string": "学生处", "members_data": [{"vid": "1688851641322280", "name": "黄汉城", "avatar": "http://wework.qpic.cn/bizmail/KNK1of2CdelIKu8MzH7rVgzibEts4LFMVQ73SjRhibMajm0gaSchPbmA/0", "is_delete": false, "is_out_corp": false, "corp_name": "东莞信息技术学校", "deleteable": true, "from": "server"}, {"vid": "1688851641322281", "name": "谢培璇", "avatar": "https://wework.qpic.cn/wwhead/duc2TvpEgSQO4BpE0WZSZ88x19mvAPmvXKYt4pB3uGWJX0bPtvStVDAibia7hu01kOztaRJhFx4zM/0", "is_delete": false, "is_out_corp": false, "corp_name": "东莞信息技术学校", "deleteable": true, "from": "server"}, {"vid": "1688851641322310", "name": "吴柏柱", "avatar": "http://wework.qpic.cn/bizmail/1TF9mZHLhgQmQ60ibxn9CJXGr8PGHTia3Rtglwibxm94JL4PJJMqj0xxA/0", "is_delete": false, "is_out_corp": false, "corp_name": "东莞信息技术学校", "deleteable": true, "from": "server"}], "members_self_select": [], "members_all_data": [], "lowercase_type": "approval", "cc_deleted": [], "invalid_string": ""}], "visual_meta": {"feature_flag_edit": true, "is_approver_change": 0, "is_notify_change": 0}}'

        # 待发送内容转换成对应的数据结构
        try:
            body_json = json.loads(body_str, strict=False)

        except ValueError as e:
            print(e)

        # children路径
        children_dic = body_json["apply_data"]["contents"][5]["value"]["children"]

        # 第几周
        body_json["apply_data"]["contents"][2]["value"][
            "new_number"
        ] = sys_info_df.values[0][3]

        # 申请原因
        if sys_info_df.values[0][4] == "None":
            body_json["apply_data"]["contents"][3]["value"]["text"] = ""
        else:
            body_json["apply_data"]["contents"][3]["value"][
                "text"
            ] = sys_info_df.values[0][4]

        # 变更类型名称
        body_json["apply_data"]["contents"][4]["value"]["selector"]["options"][0][
            "value"
        ][0]["text"] = sys_info_df.values[0][5]

        # 变更类型opthon-id
        if sys_info_df.values[0][5] == "申请临时留宿":
            body_json["apply_data"]["contents"][4]["value"]["selector"]["options"][0][
                "key"
            ] = "option-528888885"
        elif sys_info_df.values[0][5] == "申请临时不留宿":
            body_json["apply_data"]["contents"][4]["value"]["selector"]["options"][0][
                "key"
            ] = "option-528888886"
        elif sys_info_df.values[0][5] == "申请取消长期留宿":
            body_json["apply_data"]["contents"][4]["value"]["selector"]["options"][0][
                "key"
            ] = "option-528888887"
        else:
            body_json["apply_data"]["contents"][4]["value"]["selector"]["options"][0][
                "key"
            ] = ""

    # 创建者id号-共有
    body_json["creator_userid"] = sys_info_df.values[0][0]

    # 所属部门id号-共有
    if sys_info_df.values[0][1] == "信息技术系":
        body_json["choose_party"]["partyid"] = "1688851641314945"
    elif sys_info_df.values[0][1] == "智能制造系":
        body_json["choose_party"]["partyid"] = "1688851641307308"
    elif sys_info_df.values[0][1] == "财经商贸系":
        body_json["choose_party"]["partyid"] = "1688851641307309"
    elif sys_info_df.values[0][1] == "公共基础部":
        body_json["choose_party"]["partyid"] = "1688851641307305"
    else:
        body_json["choose_party"]["partyid"] = ""

    # 所属部门名称-共有
    body_json["choose_party"]["party_name"] = sys_info_df.values[0][1]

    # 班级名称-共有
    body_json["apply_data"]["contents"][1]["value"]["text"] = sys_info_df.values[0][2]

    # 根据students人数，生成对应数量的字典
    children_dics = [dict(children_dic[0]) for i in range(students_nums)]

    # 通过json.loads生成多个children字典
    children_str = json.dumps(children_dics, ensure_ascii=False)
    children_dics = json.loads(children_str)

    # 取出学生字典中的学生信息，存储到临时变量children中
    for children in children_dics:
        # 留宿变更名单--学生姓名
        children["list"][0]["value"]["text"] = stu_info_df[0]["stu_name"]
        # 留宿变更名单--学生手机
        children["list"][1]["value"]["new_number"] = stu_info_df[0]["stu_phone"]
        # 留宿变更名单--学生家长
        children["list"][2]["value"]["text"] = stu_info_df[0]["par_name"]
        # 留宿变更名单--学生家长手机
        children["list"][3]["value"]["new_number"] = stu_info_df[0]["par_phone"]
        # 留宿变更名单--学生宿舍
        children["list"][4]["value"]["text"] = stu_info_df[0]["dormitory"]
        # 留宿变更名单--学生家庭住址
        children["list"][5]["value"]["text"] = stu_info_df[0]["address"]
        stu_info_df.pop(0)

    # children_dics覆盖原body中的children
    if sys_info_df.values[0][5] == "申请长期留宿":
        body_json["apply_data"]["contents"][2]["value"]["children"] = children_dics
    else:
        body_json["apply_data"]["contents"][5]["value"]["children"] = children_dics

    # 把对应的数据结构转换成json数据
    body_json = json.dumps(body_json, ensure_ascii=False)

    return body_json


if __name__ == "__main__":
    # 从数据库获取，学生留宿信息
    stu_info_df = out_sql("stu_info")

    # 从数据库获取，系统信息
    sys_info_df = out_sql("sys_info")

    # 通过df对象操作
    body_json = body_create_df(sys_info_df, stu_info_df)
    body_str = json.dumps(body_json, ensure_ascii=False)

    # 生成json文件，便于查看。
    file_name = "now.json"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(body_json)
        f.close
