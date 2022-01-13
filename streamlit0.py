import streamlit as st
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset,DataLoader,TensorDataset
import numpy as np

def orientation(x):
    if "东南" in x:
        if x.count("南") > 1:
            if ("西南" in x) & ("南" not in x):
                return "东南"
            else:
                return "南"
        else:
            return "东南"
    elif "西南" in x:
        if x.count("南") >1:
            return "南"
        else:
            return "西南"
    elif "南" in x:
        return "南"
    elif "东" in x:
        return "东"
    elif "西" in x:
        return "西"
    else:
        return "北"



def decoration(x):
    if "精装" in x: return "精装"
    elif "简装" in x: return "简装"
    elif "毛坯" in x: return "毛坯"
    else: return "其他"


#产权（40年、50年、70年），小区，装修情况（毛坯、简装、精装），面积，建筑类型（塔楼、板楼、板塔结合、平房），
# 楼龄，室数，厅数，窗户（东西南北、东南、西南），楼层位置（低楼层、中楼层、高楼层）


def Predict(input_cq,input_xq,input_zx,input_mj,input_jz,input_ll,input_ss,input_ts,input_ch,input_lc):
    data = pd.read_csv("hangzhouhouse1.csv", encoding='utf-8')
    data.dropna(how="any", inplace=True)
    data = data.loc[data["产权"] != "未知"]
    data = data.iloc[:, [0, 4, 5, 6, 7, 9, 10, 11, 12]]

    data["起建时间"] = data["年限"].str.split("/").str[0]
    data["建筑类型"] = data["年限"].str.split("/").str[1]
    data = data.loc[(data["起建时间"] != "未知年建") & (data["建筑类型"] != "暂无数据")]
    data["楼龄"] = 2019 - data["起建时间"].str.extract("(\d+)").astype("int")
    data = data.drop(["年限", "起建时间"], axis=1)
    data["室数"] = data["户型"].str.findall("(\d)室(\d)厅").str[0].str[0].astype("int")
    data["厅数"] = data["户型"].str.findall("(\d)室(\d)厅").str[0].str[1].astype("int")

    data["窗户"] = data["朝向"].apply(orientation)
    data.drop(["朝向"], axis=1, inplace=True)
    data.shape[0] - data["楼层"].str.contains("/").sum()
    data = data.loc[data["楼层"].str.contains("/")]
    data["楼层位置"] = data["楼层"].str.split("/").str[0]
    # data["总层数"]=data["楼层"].str.split("/").str[1].str.extract("(\d+)").astype("int")
    data = data.loc[data["楼层位置"].isin(["高楼层", "中楼层", "低楼层"])]
    # data=data.drop(["楼层"],axis=1)

    data["装修情况"] = data["装修情况"].apply(decoration)
    data = data.loc[data["装修情况"] != "其他"]

    data["面积"] = data["面积"].apply(lambda x: str(x)).str.extract("([\d,.]+)").astype("float")
    data = data.iloc[:, [0, 1, 2, 5, 6, 7, 8, 9, 10, 11, 12]]
    result = ""
    data.iloc[[0], [0]] = input_cq

    data.iloc[[0], [1]] = input_xq

    data.iloc[[0], [3]] = input_zx

    data.iloc[[0], [4]] = float(input_mj)

    data.iloc[[0], [5]] = input_jz

    data.iloc[[0], [6]] = int(input_ll)

    data.iloc[[0], [7]] = int(input_ss)

    data.iloc[[0], [8]] = int(input_ts)

    data.iloc[[0], [9]] = input_ch

    data.iloc[[0], [10]] = input_lc

    temp1 = pd.get_dummies(data['产权'])
    temp2 = pd.get_dummies(data['小区'])
    temp3 = pd.get_dummies(data['装修情况'])
    temp4 = pd.get_dummies(data['建筑类型'])
    temp5 = pd.get_dummies(data['窗户'])
    temp6 = pd.get_dummies(data['楼层位置'])
    data = data.iloc[:, [2, 4, 6, 7, 8]]

    data = pd.concat([temp1, temp2, temp3, temp4, temp5, temp6, data], axis=1)

    test = data.iloc[0:1, :]

    test.drop('总价/万元', axis=1, inplace=True)

    test = torch.tensor(np.array(test))
    test = test.to(torch.float32)

    net = torch.load('net.pth')

    result = float(net(test[0]))
    return result


