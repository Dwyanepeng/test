from bs4 import BeautifulSoup
import copy
import re

def getTabmeta(tabstr):#type是否引入加粗,等于1不加粗；way是否以#区分，1是不区分；method是百分号是否加前面的东西
    """
    把带表格的html字符串，从中提取内容和描述信息，还原为list。
    先以<tr>或<thead>字符串表行标识，拆分表格字符串，其中<thead>部分为表头部分。
    以<td>字符串为标识，逐行找寻列数据，以</td>为标识，拆分列信息。
    获取列的行合并，列合并属性。
    获取列的文字属性，判断是否存在空格或tab。
    完成表格元数据获取的第一步
    """
    try:
        soup_all = BeautifulSoup(tabstr, 'lxml')  # 首先是将具有表格描述的内容进行解析，tabstr是带有html标签的
        tabMeta = []

        # 获取表头或普通行的数据和描述信息
        def metas(rows, tabMeta):
            # 没有行标识的字符串不处理。
            t_list = [' ', '\t', '\u00A0', '\u0020', '\u3000', '\u0009','\n']  # 这些都代表着空格
            if len(rows) > 0:  # 看一下表格包含的行数
                for rowind, row in enumerate(rows):  # 先从每一行看,找到的是带有tr标签的内容
                    # 没有列标识的行不处理。
                    rowdata = []
                    cols = row.find_all('td')  # 找到有td标签的全部内容，也就是每一行有多少列
                    if len(cols) > 0:  # 每一行必须有内容
                        for colind, col in enumerate(cols):  # 再从每一列看，col是html标签内容
                            # 没有列标识的不处理
                            coldata = []
                            try:
                                rowspan = int(col['rowspan'])  # 直接获取td标签中的'rowspan'属性
                            except:
                                rowspan = 1
                            coldata.append(rowspan)  # 得到行合并数

                            try:
                                colspan = int(col['colspan'])
                            except:
                                colspan = 1
                            coldata.append(colspan)  # 得到列合并数

                            text = col.get_text(strip=False).rstrip()  # 只得到每一个单元格的文字部分

                            # 解决某些带有同期增长的表格中，行列标题没有说明时间，只有比去年同期增长但是并没有去年同期是啥
                            if text.find('%') != -1 :#or text.find('增') != -1
                                if colind > 0:
                                    text = cols[colind - 1].get_text(strip=False).rstrip() + '_' + text


                            result = [tmp in t_list for tmp in text]  # 判断所有的表格中是否有缩进的
                            t_count = 0
                            for b in result:
                                if b:
                                    t_count = t_count + 1
                                else:
                                    break

                            if t_count > 0:
                                coldata.append(True)
                            else:
                                coldata.append(False)
                            coldata.append(t_count)
                            coldata.append(text)
                            rowdata = rowdata + [coldata]
                    tabMeta = tabMeta + [rowdata]
            return tabMeta

        heads = soup_all.find_all('th')
        tabMeta = tabMeta + metas(heads, tabMeta)  # 表头
        rows = soup_all.find_all('tr')  # 表格
        tabMeta = tabMeta + metas(rows, tabMeta)

        # 解决某些表格中只有tr没有td的问题,每行的元素个数都不一致，所以需要找到列数最多的行然后将其余行补齐
        colnum = [sum(list(map(lambda x: x[1], row))) for row in tabMeta]
        median = max(colnum)

        for rowind, row in enumerate(tabMeta):
            col_num = sum(list(map(lambda x: x[1], row)))
            if row == []:
                tabMeta[rowind] = [[1, 1, False, 0, '']] * int(median)
            elif col_num<median:
                tabMeta[rowind] = tabMeta[rowind]+[[1, 1, False, 0, '']] * int(median-col_num)
            else:
                tabMeta[rowind] = tabMeta[rowind]
    except:
        tabMeta = {'900':'该页面中表格结构存在问题！'}
    return tabMeta

def getFulltab(tabmeta):
    """
    根据网页表格带描述信息的数据，还原整个表格全貌。
    主要处理三个事情：
    1、出现行合并的，拆分到行。
    2、出现列合并的，拆分到列。
    3、包含空格或TAB的，拼装上级信息。
    入参为第一步的识别结果。
    出参为拼接后的完整表格。
    """
    try:
        fullTab = copy.deepcopy(tabmeta)
        # 先处理列合并
        for rowind, row in enumerate(tabmeta):
            rowdata = []
            for col in row:
                colspan = col[1]  # 列合并数
                value = col[4]  # 对应的每个单元格中的名称
                for i in range(colspan):
                    rowdata.append(value)
            fullTab[rowind] = rowdata

        # 处理行合并
        for rowind, row in enumerate(tabmeta):
            for i in range(len(fullTab[rowind])):  # 每行的数量
                tmps = fullTab[rowind][i]  # 具体到每一个描述
                realrowin = -1
                for ss in row:
                    if rowind >= 1:
                        if ss[4] == tmps:  # 这里有问题#and fullTab[rowind-1][i]!=tmps
                            realrowin = row.index(ss)
                            break
                    if rowind < 1:
                        if ss[4] == tmps:
                            realrowin = row.index(ss)
                            break
                if realrowin != -1:
                    rowspan = row[realrowin][0]  # 行合并数
                    value = row[realrowin][4]  # 对应值
                    if rowspan > 1:
                        for j in range(rowspan - 1):
                            fullTab[rowind + j + 1].insert(i, value)
        # 最后再更新第一列
        # 首先看一下是不是行标题之前有空白列
        coldata_str = [list(map(lambda x: x[i], fullTab)) for i in range(len(fullTab[0]))]
        coldata = list(map(lambda x: ''.join(x), coldata_str))  # 合并
        for i, data in enumerate(coldata_str) :
            if len(''.join(data)) != 0 and data.count(' ')/len(data)<0.1:
                startcol = i
                break
        # 然后再补充
        for rowind, row in enumerate(tabmeta):
            # 从第二行开始
            if rowind > 0:
                for colind, col in enumerate(row):
                    if colind == startcol:  # 暂时先对第一列处理
                         # 如果第一个单元格非空才可以添加上去
                        if col[2]:  # 该条件表示如果存在空格
                            des_rowid = rowind - 1
                            while True:
                                if tabmeta[des_rowid][startcol][3] < col[3] - 1 or tabmeta[des_rowid][startcol][
                                    3] == col[3] - 1:  # 这里将 等于 改为 小于等于
                                    fullTab[rowind][colind] = fullTab[des_rowid][colind] + '_' + fullTab[rowind][
                                        colind].strip()
                                    break
                                else:
                                    des_rowid = des_rowid - 1
                                    if des_rowid < 1:  # 防止前面两行只是简单的缩进并没有字段名包含关系，寻找到第一行也没有符合条件的单元格就跳出便可以了
                                        break
                            if len(''.join(fullTab[0][0])) != 0:
                                fullTab[rowind][colind] = fullTab[0][0] + '_' + fullTab[rowind][colind]  # 将最开始的第一个格的内容利用上
                            else:
                                fullTab[rowind][colind] =  fullTab[rowind][colind]

    except:
        fullTab = {'901':'表格合并单元格的分列过程中出现问题！'}
    return fullTab

def getStructdata(tablist):
    """
    将转换后的报表列表，转换为结构化数据。
    格式为[行信息，列信息，数值]
    默认从第二行第二列开始。替换掉其中的英文逗号，如果能参与计算，即为数值，设定为需要获取的单元格。
    :param tablist:转换后的table列表
    :return: 大的list，每个子list是一个单元格的数据，及其描述信息。
    :rwoid:起始的行号，默认从第二行开始。程序因为是从0开始的，因此，使用中需要减去1.
    :colid:起始的列号，默认从第二列开始。程序因为是从0开始的，因此，使用中需要减去1.
    :type:是否判断计量单位，配合前面行列起始号使用。用于数值中带有计量单位的情况。
    默认为1，即不含计量单位信息，为2时不判断单元格信息是否为数值，从指定的行列直接拼结果。
    """
    # 将整行是空格的删除
    try:
        fullTab_clear = []
        for i in tablist:
            if len(''.join(i)) > 0:
                fullTab_clear.append(i)
        tablist = copy.deepcopy(fullTab_clear)
        danwei = [str(j)[str(j).find('单位：'):].strip() for x in tablist for j in x if
                  str(j).replace('\xa0', '').replace('\u3000', '').replace(' ', '').replace('\n', '').find('单位：') != -1]
        unit = '_' + danwei[0] if danwei != [] else ''
        #获取单位列表
        try:
            unit_list = list(set([re.findall('\d+[\(](.*?)[\)]',str(j))[0]  for  x in tablist for j in x  if re.findall('[\(](.*?)[\)]',str(j))!=[]]))
        except:
            unit_list=[]
            unit_list.append(unit.replace('_',''))



        strudata_result = []
        colStart = 2  # 默认开始的列
        rowStart = 2  # 默认开始的行

        def cantransdigit(strdata,x):
            """
            用于判断给定的字符串能不能转换为数值，需要去除里面的英文逗号，中文句号。
            空值或者‘-’转换为0处理。
            :param strdata:传入的字符串
            :return:能够转换为数字。
            """
            strdata = ''.join(strdata.split())  # 为了去除特殊符号\u3000,\xa0,\n
            tmp_s = strdata.replace(',', '')  # 数字中出现逗号分隔 1,000这种写法
            tmp_s = tmp_s.replace('(百分点)', '')  # 这个括号有什么用呢，
            tmp_s = tmp_s.replace('（百分点）', '')
            tmp_s = tmp_s.replace('倍', '')
            # tmp_s = tmp_s.replace(tmp_s[tmp_s.find('('):tmp_s.find(')') + 1], '')#这个括号有什么用呢，
            tmp_s = tmp_s.replace('。', '')  # 有的时候是小数点输入有误，输入成了句号
            tmp_s = tmp_s.replace('-', '0')  # 某些表格不存在内容以-代替，英文状态的-
            tmp_s = tmp_s.replace('—', '0')  # 某些表格不存在内容以-代替，中文状态的-
            tmp_s = tmp_s.replace('.', '0')  # 将小数点以0代替
            if len(tmp_s) == 0:  # 避免某个单元格就是一个没有内容的空值，这种被识别为不是数字，影响之后的操作
                result = True
            else:
                result = tmp_s.isdigit()
            if result == False:
                tmp_s = tmp_s.replace('(','')
                tmp_s = tmp_s.replace(')', '')
                tmp_s = tmp_s.replace('（','')
                tmp_s = tmp_s.replace('）', '')
                for i in x:
                    tmp_str = re.findall('\d+'+ i ,tmp_s)
                    if tmp_str !=[]:
                        result = True
                        break
                    else:
                        result == False

            return result  # 如果字符串只包含数字返回true
        # 从指定的列开始，取一列数据判断是否均能转换为数值。
        while True:
            colmeta = [tablist[rowind][colStart - 1] for rowind in range(rowStart - 1, len(tablist))]
            coldatabool = [cantransdigit(tablist[rowind][colStart - 1],unit_list) for rowind in
                           range(rowStart - 1, len(tablist))]  # 看一下每一行均从第二列开始是不是都是可以数字化的，遍历了所有的均不可以就从第三列开始依次类推
            if sum(coldatabool) / len(coldatabool) > 0.2 and len(''.join(colmeta)) != 0:
                # 因为有些表的表尾包含一些说明信息，所以只要包含数字，就暂定为这列不是列头。
                break
            else:
                colStart = colStart + 1
        # 从指定的行开始，取一行数据判断是否均能转换为数值。
        while True:
            endcol = min([len(row) for row in tablist])
            rowmeta = [tablist[rowStart - 1][colind] for colind in range(colStart - 1, endcol)]  # 遍历每一行
            rowdatabool = [cantransdigit(tablist[rowStart - 1][colind],unit_list) for colind in
                           range(colStart - 1, len(tablist[0]))]
            if False in rowdatabool or len(''.join(rowmeta)) == 0:
                rowStart = rowStart + 1
            else:
                break

        for rowind in range(rowStart - 1, len(tablist)):
            colcount = endcol  # 每一行有多少列
            for colind in range(colStart - 1, colcount):
                strudata = []

                # 需要算法推断表头所在的行列，以指定的起始行列开始，
                # 剩下对应行或者列数据出去空值和‘-’均能转换为数值型的，则认为不是表头。
                # 替换数据中的英文逗号或者中文句号（人为失误）
                value = tablist[rowind][colind].replace(',', '').replace('。', '').replace('_','')  # 去掉逗号和句号，#前两步处理好的结果,该步处理的只是数字部分
                col_tmp_info = [
                    tablist[i][colind].replace('\xa0', '').replace('\u3000', '').replace(' ', '').replace('\n', '')
                    for i in range(rowStart - 1)]  # 表头部分，同一列是否有重复的指标名称
                col_info = []
                for s in col_tmp_info:
                    s = ''.join(s.split())
                    s_words = s.split('_')
                    for s_word in s_words:
                        if s_word not in col_info:
                            col_info.append(s_word)
                # row_tmp_info = [tablist[rowind][i].replace('\xa0', '').replace('\u3000', '').replace(' ','').replace('\n','') for i in range(colStart - 1)]
                row_tmp_info = [
                    tablist[rowind][i].replace('\xa0', '').replace('\u3000', '').replace(' ', '').replace('\n', '')
                    for i in range(colStart - 1)]
                row_info = []
                for s in row_tmp_info:
                    s = ''.join(s.split())
                    s_words = s.split('_')
                    for s_word in s_words:
                        if s_word not in row_info:
                            row_info.append(s_word)
                strudata.append('_'.join(row_info) + unit)  # 行标题的连接,在这里加上的单位
                strudata.append('_'.join(col_info))  # 以—连接列标题
                try:
                    # 避免表尾的说明信息以及空值转换为无用的结构化数据。
                    if len(value) > 0:  # 这里如果值不能转化为数字就被忽略了
                        value_str = value.replace(value[value.find('('):value.find(')') + 1], '') if value.find(
                            '(') != -1 else value
                        strudata.append(str(float(value_str))+value[value.find('('):value.find(')') + 1])
                        strudata_result = strudata_result + [strudata]
                except:
                    pass

    except:
        strudata_result = {'902':'识别表头部分出现错误'}
    return strudata_result