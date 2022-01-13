import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Scatter, HeatMap

import warnings

warnings.filterwarnings('ignore')

data=pd.read_csv("E:\\flask\\坤的可视化\\hangzhouhouse1.csv",encoding='utf-8')
data.dropna(how="any",inplace=True)
data=data.loc[data["产权"] != "未知"]

def location(x):
    if "临安" in x: return "临安市"
    elif "上城" in x: return "上城区"
    elif "下城" in x: return "下城区"
    elif "江干" in x: return "江干区"
    elif "拱墅" in x: return "拱墅区"
    elif "西湖" in x: return "西湖区"
    elif "滨江" in x: return "滨江区"
    elif "萧山" in x: return "萧山区"
    elif "余杭" in x: return "余杭区"
    elif "富阳" in x: return "富阳区"
    elif "钱塘" in x: return "钱塘新区"
    else: return "其他"

data["地理位置"]=data["区域"].apply(location)
data["单价"]=data["单价"].apply(lambda x: str(x)).str.findall("(\d+)").str[0].astype("float")

data["起建时间"]=data["年限"].str.split("/").str[0]
data["建筑类型"]=data["年限"].str.split("/").str[1]
data=data.loc[(data["起建时间"]!="未知年建") & (data["建筑类型"] != "暂无数据")]
data["楼龄"]=2021-data["起建时间"].str.extract("(\d+)").astype("int")
data=data.drop(["年限","起建时间"],axis=1)
data["室数"]=data["户型"].str.findall("(\d)室(\d)厅").str[0].str[0].astype("int")
data["厅数"]=data["户型"].str.findall("(\d)室(\d)厅").str[0].str[1].astype("int")




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

data["窗户"]=data["朝向"].apply(orientation)
data.drop(["朝向"],axis=1,inplace=True)
data.shape[0]-data["楼层"].str.contains("/").sum()
data=data.loc[data["楼层"].str.contains("/")]
data["楼层位置"]=data["楼层"].str.split("/").str[0]
data["层数"]=data["楼层"].str.split("/").str[1].str.extract("(\d+)").astype("int")
data=data.loc[data["楼层位置"].isin(["高楼层","中楼层","低楼层"])]
data=data.drop(["楼层"],axis=1)

def decoration(x):
    if "精装" in x: return "精装"
    elif "简装" in x: return "简装"
    elif "毛坯" in x: return "毛坯"
    else: return "其他"

data["装修情况"]=data["装修情况"].apply(decoration)
data=data.loc[data["装修情况"] != "其他"]

data["面积"]=data["面积"].apply(lambda x: str(x)).str.extract("([\d,.]+)").astype("float")
data=data[["地理位置","区域","小区","总价/万元","单价","面积","楼龄","建筑类型","楼层位置","层数","装修情况","室数","厅数","窗户","产权","户型","关注"]]

data_=data.loc[(data["总价/万元"] > 50) & (data["总价/万元"] < 3000)]
data=data.loc[data["户型"] != "0室0厅"]

def gediqu():
    sum_area = data.groupby("地理位置")["总价/万元"].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(sum_area["地理位置"], sum_area["总价/万元"], palette=sns.color_palette('Blues_r'))
    ax.set_title("杭州市各城区房源平均总价对比")
    ax.set_xlabel("城区")
    ax.set_ylabel("总价/万元")

    plt.show()
    pair2 = [(row["地理位置"], round(row["总价/万元"], 2)) for i, row in sum_area.iterrows()]
    map2 = Map(init_opts=opts.InitOpts(theme='macarons', width='800px', height='400px'))
    map2.add('杭州', pair2, "杭州", is_roam=False)
    map2.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map2.set_global_opts(
        title_opts=opts.TitleOpts(title="杭州市各城区房源平均总价"),
        legend_opts=opts.LegendOpts(is_show=True),
        visualmap_opts=opts.VisualMapOpts(min_=sum_area["总价/万元"].min(), max_=sum_area["总价/万元"].max()),
        tooltip_opts=opts.TooltipOpts(formatter='{b}:{c}万元')
    )
    return map2.render_embed()

def select(diqu,mianji,jiage):
    temp=data
    if diqu[0]==mianji[0]==jiage[0]=='全部':return temp.iloc[:200]
    if diqu[0]=='全部':
        temp=data.iloc[:200]
    elif len(diqu)==1:
        temp=temp[temp['地理位置']==diqu[0]]
    else:
        temp=pd.DataFrame([])
        for i in diqu:
            temp2=data[data['地理位置']==i]
            temp=pd.concat([temp,temp2],axis=0)

    mianjied = pd.DataFrame([])
    if mianji[0]=='全部':mianjied=temp
    else:
        for i in mianji:
            if i == '100平以下':mianjied=pd.concat([mianjied,temp[temp['面积']<100]],axis=0)
            elif i=='100-200平':mianjied=pd.concat([mianjied,temp.loc[(temp['面积']>=100) & (temp['面积']<200)]],axis=0)
            else:mianjied=pd.concat([mianjied,temp[temp['面积']>=200]],axis=0)

    jiaged = pd.DataFrame([])
    if jiage[0] == '全部':jiaged=mianjied
    else:
        for i in jiage:
            if i == '200万以下':jiaged=pd.concat([jiaged,mianjied[mianjied['总价/万元']<200]],axis=0)
            elif i == '200-400万':jiaged=pd.concat([jiaged,mianjied.loc[(mianjied['总价/万元']>=200) & (mianjied['总价/万元']<400)]],axis=0)
            elif i == '400-600万':jiaged=pd.concat([jiaged,mianjied.loc[(mianjied['总价/万元']>=400) & (mianjied['总价/万元']<600)]],axis=0)
            elif i == '600-800万':jiaged=pd.concat([jiaged,mianjied.loc[(mianjied['总价/万元']>=600) & (mianjied['总价/万元']<800)]],axis=0)
            else:jiaged=pd.concat([jiaged,mianjied[mianjied['总价/万元']>=800]],axis=0)
    jiaged=jiaged.sort_values(axis=0,by='关注',ascending=False)
    return jiaged

def gediqufangyuanshu():
    count_area = data.groupby("地理位置")["关注"].count().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(count_area["地理位置"], count_area["关注"], palette='Greens_r')
    ax.set_title("杭州市各区房源数量对比")
    ax.set_xlabel('区域')
    ax.set_ylabel('数量')

    plt.show()

    pair1 = [(row["地理位置"], row['关注']) for i, row in count_area.iterrows()]
    map1 = Map(init_opts=opts.InitOpts(theme='macarons', width='800px', height='400px'))
    map1.add('杭州', pair1, "杭州", is_roam=False)
    map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map1.set_global_opts(
        title_opts=opts.TitleOpts(title="杭州市各区房源数量对比"),
        legend_opts=opts.LegendOpts(is_show=True),
        visualmap_opts=opts.VisualMapOpts(min_=count_area["关注"].min(), max_=count_area["关注"].max())
    )
    return map1.render_embed()

def gediquguanzhu():
    attention_area = data.groupby("地理位置")["关注"].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(attention_area["地理位置"], attention_area["关注"], palette=sns.color_palette('Purples_r'),
                     saturation=0.5)
    ax.set_title("杭州市各城区房源关注热度对比")
    ax.set_xlabel("城区")
    ax.set_ylabel("关注度")
    plt.show()
    pair4 = [(row["地理位置"], row["关注"]) for i, row in attention_area.iterrows()]
    map4 = Map(init_opts=opts.InitOpts(theme='macarons', width='800px', height='400px'))
    map4.add('杭州', pair4, "杭州", is_roam=False)
    map4.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map4.set_global_opts(
        title_opts=opts.TitleOpts(title="杭州市各城区房源关注热度对比"),
        legend_opts=opts.LegendOpts(is_show=True),
        visualmap_opts=opts.VisualMapOpts(min_=attention_area["关注"].min(), max_=attention_area["关注"].max())
    )
    return map4.render_embed()

def chaoxiang():
    orientation_attention = data.groupby("窗户")["关注"].sum().sort_values(ascending=False).reset_index()
    pair5 = [(row["窗户"], row["关注"]) for i, row in orientation_attention.iterrows()]
    pie1 = Pie(init_opts=opts.InitOpts(theme='light', width='800px', height='400px'))
    pie1.add("", pair5, radius=["35%", "75%"])
    pie1.set_global_opts(title_opts=opts.TitleOpts(title="不同朝向的关注度对比"),
                         legend_opts=opts.LegendOpts(is_show=True))
    pie1.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    return pie1.render_embed()

def huxing():
    data["户型"] = data["室数"].astype("str") + "室" + data["厅数"].astype("str") + "厅"
    house_type_attention = data.groupby("户型")["关注"].sum().sort_values(ascending=False).reset_index()
    bar1 = Bar(init_opts=opts.InitOpts(theme='wonderland', width='600px', height='400px'))
    bar1.add_xaxis(house_type_attention.head(10)["户型"].to_list())
    bar1.add_yaxis("", house_type_attention.head(10)["关注"].to_list())
    bar1.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    bar1.set_global_opts(title_opts=opts.TitleOpts(title="关注度最高的户型TOP10"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0"}))
    return bar1.render_embed()

def loucen():
    location_attention = data.groupby("楼层位置")["关注"].sum().sort_values(ascending=False)
    cut_range = [x for x in range(5, 61, 5)]
    cut_name = [str(cut_range[i]) + "～" + str(cut_range[i + 1]) + "层" for i in range(11)]
    data["层数范围"] = pd.cut(data["层数"], cut_range, labels=cut_name)
    floor_attention = data.groupby("层数范围")["关注"].sum().sort_values(ascending=False).reset_index()
    bar2 = Bar(init_opts=opts.InitOpts(theme='vintage', width='600px', height='400px'))
    bar2.add_xaxis(floor_attention["层数范围"].to_list())
    bar2.add_yaxis("关注度", floor_attention["关注"].to_list())
    bar2.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    bar2.set_global_opts(title_opts=opts.TitleOpts(title="不同楼层的关注度对比"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0", "rotate": 45}))
    return bar2.render_embed()