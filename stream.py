import streamlit as st
import pandas as pd
from PIL import Image
import numpy
from subprocess import Popen, PIPE
import streamlit.components.v1 as components
import pic
import streamlit0
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
df=pd.read_csv('hangzhouhouse1.csv',encoding='utf-8')

def main():
    #st.markdown(pic.gediqu(),unsafe_allow_html=True)


    st.sidebar.markdown('<h3>第七组数据仓库与数据挖掘课程设计</h3>',unsafe_allow_html=True)
    st.sidebar.markdown('<h5>组员：童亨  侯照坤  方翔</h5>', unsafe_allow_html=True)
    lable1 = st.sidebar.radio('',('首页','数据查看','数据可视化','房价预测'))
    if lable1 == '数据查看':
        st.title('房源信息查询')
        diqu=st.multiselect('请选择地区',['全部', '上城区', '下城区', '临安市', '余杭区', '富阳区', '拱墅区', '江干区', '滨江区', '萧山区', '西湖区', '钱塘新区'],['全部'])
        mianji=st.multiselect('请选择面积',['全部','100平以下','100-200平','200平以上'],['全部'])
        jiage=st.multiselect('请选择价格',['全部','200万以下','200-400万','400-600万','600-800万','800万以上'],['全部'])
        if st.button('确认'):
            data=pic.select(diqu,mianji,jiage)
            st.table(data)

        #st.table(df.iloc[:200])
    elif lable1 == '数据可视化':
        st.title('数据可视化')
        if st.checkbox('各属性关联度'):
            guanlaindu=Image.open('属性关联度.jpg')
            st.image(guanlaindu,caption='各属性关联度')
        if st.checkbox('各面积房屋数'):
            mianji=Image.open('各面积房屋数.jpg')
            st.image(mianji)
        if st.checkbox('各总价房屋数'):
            zongjia=Image.open('各总价房屋数.jpg')
            st.image(zongjia)
        if st.checkbox('各地区房源数'):
            fangyuanshu()
        if st.checkbox('各地区关注热度'):
            guanzhu()
        if st.checkbox('最受欢迎朝向'):
            components.html(pic.chaoxiang(),height=400)
        if st.checkbox('最受欢迎户型'):
            components.html(pic.huxing(),height=400)


    elif lable1 == '房价预测':
        st.title('房价预测系统')
        html_temp = """
            <div style="background-color:tomato;padding:10px">
            <h2 style="color:white;text-align:center;">房源信息输入</h2>
            </div>
            """
        st.markdown(html_temp, unsafe_allow_html=True)
        input_cq = st.selectbox('产权', ('40年', '50年', '70年'))

        input_xq = st.text_input("小区", "请输入")

        input_zx = st.selectbox('装修情况', ('毛坯', '简装', '精装'))

        input_mj = st.text_input("面积", "请输入")

        input_jz = st.selectbox('建筑类型', ('塔楼', '板楼', '板塔结合', '平房'))

        input_ll = st.text_input("楼龄", "请输入")

        input_ss = st.text_input("室数", "请输入")

        input_ts = st.text_input("厅数", "请输入")

        input_ch = st.selectbox('窗户', ('东', '南', '西', '北', '东南', '西南'))

        input_lc = st.selectbox('楼层位置', ('低楼层', '中楼层', '高楼层'))
        if st.button('预测房价'):
            result = streamlit0.Predict(input_cq,input_xq,input_zx,input_mj,input_jz,input_ll,input_ss,input_ts,input_ch,input_lc)

            st.success('房源价格预测：{}万元'.format(result))
    else:welcome()


def welcome():
    st.title('杭州房价数据可视化')
    components.html(pic.gediqu(), width=800, height=500)
    st.markdown('注：数据来自2019年链家二手房平台')

def yuanshushuju():
    st.markdown('<h3 style="background-color:rgb(182,194,154);text-align:center">房价数据</h3>', unsafe_allow_html=True)
    diqu=st.selectbox('地区', ['全部', '上城区', '下城区', '临安市', '余杭区', '富阳区', '拱墅区', '江干区', '滨江区', '萧山区', '西湖区', '钱塘新区'], key=1)
    if st.button('确认'):
        diqu=diqu
    st.success(st.table(pic.diqu(diqu)))
    # mianji=st.selectbox('面积',[])
    #st.table(df.iloc[0:200])
    
def fangyuanshu():
    components.html(pic.gediqufangyuanshu(),width=800,height=450)
    
def guanzhu():
    components.html(pic.gediquguanzhu(),width=800,height=450)

if __name__ == '__main__':
    main()
