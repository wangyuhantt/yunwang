import pandas as pd
import json

def process_sub_twins(df, parent, processed_nodes):
    """
    递归处理子孪生体，生成对应的 JSON 结构
    """
    sub_twins_json = []

    # 获取当前孪生体的所有子孪生体
    sub_twins = df[df['父孪生体'] == parent]['子孪生体'].tolist()

    for sub_twin in sub_twins:
        # 如果子孪生体已经处理过，跳过，，避免重复处理
        if sub_twin in processed_nodes:
            continue

        # 递归处理当前子孪生体
        sub_json = process_sub_twins(df, sub_twin, processed_nodes)
        sub_twins_json.append({
            "name": sub_twin,
            "description": "",
            "id": "",
            "events": [],
            "actions": [],
            "subTwins": sub_json,
            "properties": [],
            "updateTime": str(int(pd.Timestamp("now").timestamp()))
        })

        # 将已处理的子孪生体加入列表，避免重复处理
        processed_nodes.append(sub_twin)

    return sub_twins_json

def process_root_node(df, root_node):
    """
    处理单个根节点，生成对应的 JSON 结构
    """
    root_json = {
        "name": root_node,
        "description": "",
        "id": "",
        "events": [],
        "actions": [],
        "subTwins": process_sub_twins(df, root_node, []),
        "properties": [],
        "updateTime": str(int(pd.Timestamp("now").timestamp()))
    }

    return root_json

# 读取Excel文件
df = pd.read_excel('D:\Python\excelTojson\excel.xlsx')

# 获取所有根节点
root_nodes = df[df['父孪生体'] == '无']['子孪生体'].tolist()

# 生成JSON框架
json_framework = {
    "projectID": "project_id",
    "projectData": []
}

# 遍历每个根节点
for root_node in root_nodes:
    # 处理单个根节点，并将结果添加到 json_framework 中
    root_node_json = process_root_node(df, root_node)
    json_framework["projectData"].append(root_node_json)

# 输出JSON框架
print(json.dumps(json_framework, indent=2))
