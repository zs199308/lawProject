
#阈值上界和下界
e1 = 0.7
e2 = 0.5

'''
1.默认每个条件都与所有结果相连
2.认定有边的条件才会共同作用于最终的结果，若不连接，则要么是矛盾的关系 ，要么是平行的关系，单向边相连是上下级关系）
3.因此具有多个条件的时候，需要先求出两两有边相连的条件集合（单向边和双向边均可），有可能有多个，每一个集合可能都会引向不同的结果，这样可能会涉及到多个罪责
4.指向判罪结果的概率即使大于所有指向条件的概率也需要大于e2才行。
5.若最终既没有能指向判罪结果也没有能指向条件的概率，则判为无罪
6.下面示例是根据算出来的最大的条件概率引导提问，并假设满足。
7.实际情况也可以让提问者自行补充条件，每增加一个条件都需要进行第三步的步骤
'''
#condition = {'A1': 0.35, 'A2': 0.2, 'A3': 0.15, 'A4': 0.5,'A5': 0.15, 'A6': 0.05}
#result = {'B1': 0.6, 'B2': 0.4}
results = ['B1','B2']

#键表示前提条件，值表示跳向的条件
cond_cond = {}
cond_cond['A1'] = ['A2','A3','A4','A5','A6']
cond_cond['A2'] = ['A1','A3','A4','A5','A6']
cond_cond['A3'] = ['A1','A2','A4']
cond_cond['A4'] = ['A1','A2','A3']
cond_cond['A5'] = ['A1','A2']
cond_cond['A6'] = ['A1','A2']

'''
给定一个例子：已知A1，A2，下一步需要跳向两者能共同指向的条件
'''
p = {'A3|A1A2': 0.45, 'A4|A1A2': 0.4, 'A5|A1A2': 0.3, 'A6|A1A2': 0.2, 'B1|A1A2': 0.2, 'B2|A1A2': 0.3,
     'A4|A1A2A3':0.55, 'B1|A1A2A3': 0.36, 'B2|A1A2A3': 0.33,
     'B1|A1A2A3A4':0.75, 'B2|A1A2A3A4':0.2}
conds = ['A1','A2']

def intersec(list1, list2):
    return [val for val in list1 if val in list2]
def conversation():
    print("甲：现在有条件A1和A2，请问犯罪吗，如果犯罪，是什么罪")
    nextstate = ''
    candidate_cond = cond_cond[conds[0]]
    maxpro = 0
    condstr = ''
    while True:
        for c in conds:
            candidate_cond = list(set(candidate_cond) & set(cond_cond[c]))
            condstr = condstr + c
        for i in candidate_cond:
            if p[i + '|' + condstr] > maxpro:
                maxpro = p[i + '|' + condstr]
                nextstate = i
        for re in results:
            #print('p' + '[' + str(re) + '|' + str(condstr) + '] = ' + str(p[re + '|' + condstr]))
            if p[re + '|' + condstr] > e1:
                maxpro = p[re + '|' + condstr]
                nextstate = re
            if p[re + '|' + condstr] > maxpro and p[re + '|' + condstr] > e2:
                maxpro = p[re + '|' + condstr]
                nextstate = re

        for re in results:
            if nextstate == re:
                print("乙: 属于犯罪，类型是%s" %re)
                return
        if len(candidate_cond) == 0:
            print("甲: 该情况属于无罪")
            return
        else:
            print("乙：请问满足条件%s吗" %nextstate)
            print("甲: 是的")

        conds.append(nextstate)
        maxpro = 0
        condstr = ''

if __name__ == "__main__":
    conversation()
