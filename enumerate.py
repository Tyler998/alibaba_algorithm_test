import sys
import pandas as pd
import numpy as np


def get_promotion(input_data):
    '''
    :param input_data: 输入的原始数据
    :return: 经过排序的优惠活动list 。如[(80,5),(90,6).....]
    '''
    promotion = input_data[0].split(';')
    for i in range(len(promotion)):
        promotion[i] = (int(promotion[i].split('-')[0]), int(promotion[i].split('-')[1]))
        # 按照优惠力度进行排序，避免输入是无序的。
    return sorted(promotion)


def get_food_info_table(input_data):
    '''
    :param input_data: 输入的原始数据
    :return:DataFrame结构的数据,将零时信息放在一个表里。
    '''
    # 获得活动列表
    promotion_number_list = []
    price_list = []
    # 根据输入信息，将每个零时对号入座。
    food_infos = input_data[1].split(';')
    for food_info in food_infos:
        temp = food_info.split('-')
        price_list.append(int(temp[0]))
        promotion_number_list.append(int(temp[1]))
    food_info_table = {'promotion_number': promotion_number_list, 'price': price_list, }
    # 转成DataFrame格式，便于算价格的时候筛选。
    food_info_table = pd.DataFrame(food_info_table)
    return food_info_table


def get_balance(input_data):
    '''
    :param input_data: 输入的原始数据
    :return: 余额
    '''
    return int(input_data[2])


def get_isbuy_list(t, food_number):
    '''
    产生所有可能的解
    :param input_data: t,商品数量
    :return:无
    '''
    if t > food_number - 1:
        for i in range(food_number):
            isbuy_list.append(arr[i])
    else:
        for i in range(2):
            arr[t] = i
            get_isbuy_list(t + 1, food_number)


def price_cal(food_info_table, balance, isbuy_list):
    '''
    :param input_data：零时信息表，余额，所有购买情况组成的列表（二维数组）
    :return:购买的零时的原价
    '''
    result = 0
    promotion = get_promotion(input_data)
    for i in range(len(isbuy_list)):
        # 用二进制数标记每个商品。
        food_info_table['isbuy'] = isbuy_list[i]
        # 筛选出需要买的商品
        discount_price = 0
        food_info_table_buy = food_info_table[food_info_table['isbuy'] == 1]
        for j in range(1, len(promotion) + 1):
            temp = food_info_table_buy[food_info_table_buy['promotion_number'] == j]
            discount_price += (sum(temp['price']) - (sum(temp['price']) // promotion[j - 1][0]) * promotion[j - 1][1])
        if discount_price <= balance and sum(food_info_table_buy['price']) > result:
            result = sum(food_info_table_buy['price'])
        else:
            continue
    return result


if __name__ == '__main__':
    input_data = []
    # 获取输入数据
    for i in range(3):
        line = sys.stdin.readline().strip()
        input_data.append(line)
    food_info_table = get_food_info_table(input_data)
    balance = get_balance(input_data)
    # ----------产生所有可能的解 begain ----------#
    isbuy_list = []
    food_number = len(food_info_table)
    arr = food_number * [0]
    get_isbuy_list(0, food_number)
    isbuy_list = np.array(isbuy_list).reshape(2 ** food_number, food_number)
    # ----------产生所有可能的解 end ----------#
    print(price_cal(food_info_table, balance, isbuy_list))
