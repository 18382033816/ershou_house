# encoding=utf8
import numpy as np
import matplotlib.pyplot as mp
# price=np.loadtxt('house.csv',delimiter=',',usecols=(1,),unpack=True)
import csv
with open('house.csv','r') as csv_file:
    all_lines=csv.reader(csv_file)
    block=[]
    price=[]
    area=[]
    for all_line in all_lines:
        block.append(all_line[-1])
        price.append(float(all_line[-2]))
        area.append(int(all_line[2]))
block=np.array(block)
print(block)
price=np.array(price)
area=np.array(area)
price_mean=np.mean(price)
area_mean=np.mean(area)
print("平均价格为：(万元)", price_mean)
print("平均面积为：(平方米)", area_mean)
# 求价格和面积的方差
price_std = np.std(price)
area_std = np.std(area)
print("价格的标准差为：(万元)", price_std)
print("面积的标准差为：", area_std)
xs=np.arange(1,3001)
mp.figure('Prices',facecolor='gray')
mp.subplot(2,1,1)
mp.title('Prices',fontsize=20)
mp.xlabel('x',fontsize=14)
mp.ylabel('price',fontsize=14)
mp.tick_params(labelsize=10)
mp.grid(linestyle=':')
# mp.hist(price, bins=20)
mp.plot(xs,price,c='gray',label='real price')
mp.legend()
mp.subplot(2,1,2)
mp.title('Areas',fontsize=20)
mp.xlabel('x',fontsize=14)
mp.ylabel('area',fontsize=14)
mp.tick_params(labelsize=10)
mp.grid(linestyle=':')
# mp.hist(price, bins=20)
mp.plot(xs,area,c='gray',label='real area')
mp.legend()
mp.show()

