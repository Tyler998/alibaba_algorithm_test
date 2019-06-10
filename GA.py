import sys
import pandas as pd
import geatpy as ga
import numpy as np


def get_promotion(input_data):
    '''
    :param input_data: 输入的原始数据
    :return: 经过排序的优惠活动list 。如[(80,5),(90,6).....]
    '''
    promotion = input_data[0].split(';')
    for i in range(len(promotion)):
        promotion[i] = (int(promotion[i].split('-')[0]), int(promotion[i].split('-')[1]))
    return sorted(promotion)


def get_food_info_table(input_data):
    '''
    :param input_data: 输入的原始数据
    :return:DataFrame结构的数据,将食物信息放在一个表里。
    '''
    # 获得活动列表
    promotion_number_list = []
    price_list = []
    # 根据输入信息，将每个零食对号入座。
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


def fitness_cal(food_info_table, promotion, balance, isbuy_list):
    '''
	:param input_data：商品信息表，折扣，余额，所有购买情况组成的列表（二维数组）
    :return:购买的商品的原价
    '''
    # 用二进制数标记每个零食。
    food_info_table['isbuy'] = isbuy_list
    # 筛选出需要买的零食
    discount_price = 0
    food_info_table_buy = food_info_table[food_info_table['isbuy'] == 1]
    for i in range(1, len(promotion) + 1):
        temp = food_info_table_buy[food_info_table_buy['promotion_number'] == i]
        discount_price += (sum(temp['price']) - (sum(temp['price']) // promotion[i - 1][0]) * promotion[i - 1][1])
    if discount_price <= balance:
        fitness = sum(food_info_table_buy['price'])
    else:
        fitness = 0
    return fitness


if __name__ == '__main__':
    # 获取输入的初始数据
    input_data = []
    for i in range(3):
        line = sys.stdin.readline().strip()
        input_data.append(line)
    # 整理初始数据
    food_info_table = get_food_info_table(input_data)
    # 种群规模，
    pop_size = 60
    # 最大迭代次数
    gen_max = 100
    # 维度，即商品种类
    M = len(food_info_table)
    # 初始种群
    chrom = ga.crtbp(pop_size, M)

    gen = 0
    while gen < gen_max:
        # FitnV用来存储适应度值
        FitnV = []
        for individual in chrom:
            FitnV.append(fitness_cal(food_info_table, get_promotion(input_data), get_balance(input_data), individual))
        # temp用来存储参与交叉编译的个体
        temp = []
        # 选出每代种群中最优秀的五个进行交叉变异
        for i in ga.tour(np.array(FitnV).reshape(pop_size, 1), 5):
            temp.append(chrom[i])
            # xovdp 是交叉编译函数，其第二个参数是交叉概率
        temp = ga.xovdp(np.array(temp), 1)
        new_chrom = ga.reins(chrom, temp, 1, 1, 1, np.array(FitnV).reshape(pop_size, 1))
        gen += 1
    print(max(FitnV))
