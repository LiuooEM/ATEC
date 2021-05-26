import json
import codecs

def return_predicted_boundary_test_label(domain, run_epoch):
    """
    读取原始test的顺序索引，存为origin_index，是一个二维数组,[flag, index]
    """
    file_name = 'output_data/' + domain + '/origin_index_' + str(run_epoch) + '.utf8'
    origin_index = []
    with open(file_name, 'r') as f:
        for i in f:
            temp = i.strip().split(" ")
            origin_index.append([temp[0], temp[1]])
    
    """
    读取存在方面句子的预测结果,先全置0，再修改
    """
    #读取索引
    file_name_index = 'output_data/' + domain + '/que2con_' + str(run_epoch) + '.json'
    f1 = codecs.open(file_name_index,"r",encoding="utf-8")
    chosen_index = json.load(f1)
    ans_id = []
    con_id = []
    for key in chosen_index:
        ans_id.append(key)
    for i in range(len(ans_id)):
        con_id.append(chosen_index[str(ans_id[i])])
    #读取预测结果
    file_name_pre = 'boundary_output_data/' + domain + '/predictions_' + str(run_epoch) + '.json'
    f2 = codecs.open(file_name_pre,"r",encoding="utf-8")
    predictions = json.load(f2)
    lens = len(ans_id)
    start_index = []
    end_index = []
    for i in range(len(ans_id)):
        start_index.append(predictions[str(ans_id[i])]["start_index"])
        end_index.append(predictions[str(ans_id[i])]["end_index"])

    chosen_pred = [[0 for i in range(0, 83)] for j in range(con_id[len(con_id) - 1] + 1)]
    for i in range(0, lens):
        con_id_temp = con_id[i]
        start_index_temp = start_index[i]
        end_index_temp = end_index[i]
        if start_index_temp == end_index_temp:
            chosen_pred[con_id_temp][start_index_temp] = 1
        else:
            for j in range(start_index_temp,end_index_temp+1):
                if j == start_index_temp:
                    chosen_pred[con_id_temp][j] = 1
                else:
                    chosen_pred[con_id_temp][j] = 2
        
    """
    构造pred列表
    """
    pred = []
    temp = [0 for j in range(0, 83)]
    count = 0
    for i in range(0, len(origin_index)):
        #句子中没有提取出方面
        if origin_index[i][0] == '1':
            pred.append(temp)
        #句子中存在方面
        else:
            pred.append(chosen_pred[count])
            count += 1
    
    return pred

def generate_boundary_test_data(domain, run_epoch):
    path = 'output_data/' + domain + '/test_' + str(run_epoch) + '.utf8'
    context,query = load_data_test(domain, run_epoch)
    if len(context) != 0:
        squad_test_data(domain, context,query,run_epoch)
        
def load_data_test(domain, run_epoch):
    split_file = 'output_data/' + domain + '/test_' + str(run_epoch) + '.utf8'
    f = codecs.open(split_file, "r", encoding="utf-8")
    
    chosen_file = 'output_data/' + domain + '/chosen_test_' + str(run_epoch) + '.utf8'
    other_file = 'output_data/' + domain + '/other_test_' + str(run_epoch) + '.utf8'
    
    f1 = codecs.open(chosen_file, "w", encoding="utf-8")
    f2 = codecs.open(other_file, "w", encoding="utf-8")

    string = []
    true_label = []
    pre_label = []

    string_part = []
    true_label_part = []
    pre_label_part = []

    """
    """
    origin_index = []
    other_index = 0
    chosen_index = 0
    

    for line in f:
        if len(line.strip()) != 0:
            line_sp = line.strip().split(" ")
            string_part.append(line_sp[0])

            true_label_part.append(line_sp[1])
            pre_label_part.append(line_sp[2])
        else:
            if len(string_part) != 0:
                string.append(string_part)
                string_part = []
            if len(true_label_part) != 0:
                true_label.append(true_label_part)
                true_label_part = []
            if len(pre_label_part) != 0:
                pre_label.append(pre_label_part)
                pre_label_part = []

    chosen_string = []
    chosen_true_label = []
    chosen_pre_label = []

    other_string = []
    other_true_label = []
    other_pre_label = []

    context = []
    query = []

    query_id = {}
    id_ = 0
    for i in range(len(pre_label)):
        string_part = string[i]
        true_label_part = true_label[i]
        pre_label_part = pre_label[i]
        query_part = []
        judge = 0
        aspect_index = 0
        if "1" not in pre_label_part:
            other_string.append(string_part)
            other_true_label.append(true_label_part)
            other_pre_label.append(pre_label_part)
            
            """
            """
            origin_index.append([1, other_index])
            other_index += 1
            
            continue
        else:
            con = 0
            start = 0
            end = 0
            for j in range(len(pre_label_part)):
                if pre_label_part[j] == "1" and j + 1 < len(pre_label_part) and pre_label_part[j + 1] == '2':
                    start = j
                    con = 1
                    aspect_index = aspect_index + 1
                    for m in range(j + 1, len(pre_label_part)):
                        if (pre_label_part[m] == "2" and m == len(pre_label_part) - 1) or (
                                pre_label_part[m] == "2" and m + 1 < len(pre_label_part) and (
                                pre_label_part[m + 1] == "0" or pre_label_part[m + 1] == "1")):
                            end = m
                            break
                elif pre_label_part[j] == "1" and j + 1 < len(pre_label_part) and (
                        pre_label_part[j + 1] == '0' or pre_label_part[j + 1] == '1'):
                    start = j
                    end = j
                    con = 1
                    aspect_index = aspect_index + 1
                elif pre_label_part[j] == "1" and j + 1 == len(pre_label_part):
                    start = j
                    end = j
                    con = 1
                    aspect_index = aspect_index + 1
                if con == 1:
                    judge = 1
                    query_part.append(string_part[start:end + 1])
                    query_id[id_] = aspect_index
                    id_ = id_ + 1
                    con = 0

        if judge == 1:
            context.append(string_part)
            query.append(query_part)
            chosen_string.append(string_part)
            chosen_true_label.append(true_label_part)
            chosen_pre_label.append(pre_label_part)
            
            """
            """
            origin_index.append([0, chosen_index])
            chosen_index += 1
            

        else:
            other_string.append(string_part)
            other_true_label.append(true_label_part)
            other_pre_label.append(pre_label_part)
            
            """
            """
            origin_index.append([1, other_index])
            other_index += 1
            

    save_test(f1,f2,chosen_string, chosen_true_label, chosen_pre_label, other_string, other_true_label, other_pre_label)
    """
    写入test数据集本来的索引顺序
    """
    filename_origin_index = 'output_data/' + domain + '/origin_index_' + str(run_epoch) + '.utf8'
    with open(filename_origin_index, 'w', encoding='utf8') as f:
        for i in origin_index:
            f.writelines(str(i[0]) + ' ' + str(i[1]) + '\n')
    
    return context, query

def save_test(f1,f2,chosen_string, chosen_true_label, chosen_pre_label, other_string, other_true_label, other_pre_label):
    for j in range(len(chosen_string)):
        chosen_string_part = chosen_string[j]
        chosen_pre_label_part = chosen_pre_label[j]
        chosen_true_label_part = chosen_true_label[j]

        for m in range(len(chosen_string_part)):
            f1.write(chosen_string_part[m]+" "+chosen_pre_label_part[m]+"\n")
        f1.write("\n")

    for j in range(len(other_string)):
        other_string_part = other_string[j]
        other_pre_label_part = other_pre_label[j]
        other_true_label_part = other_true_label[j]

        for m in range(len(other_string_part)):
            f2.write(other_string_part[m]+" "+other_pre_label_part[m]+"\n")
        f2.write("\n")
        
def squad_test_data(domain, context,query,run_epoch):
    squad_file = 'output_data/' + domain + '/test_' + str(run_epoch) + '_boundary_test_data.json'
    f = open(squad_file,"w",encoding="utf-8")
    que2con_file = 'output_data/' + domain + '/que2con_' + str(run_epoch) + '.json'
    f1 = open(que2con_file, "w", encoding="utf-8")
    all = {}
    dic = []
    id_ = 0
    que2con = {}
    for i in range(len(context)):
        context_part = " ".join(context[i])
        query_part = query[i]
        dic_in = {}
        dic_in["title"] = " "
        par = []
        par_in = {}
        par_in["context"] = context_part
        qas = []
        for j in range(len(query_part)):
            qas_in = {}
            ans = []
            ans_in = {}
            ans_in["answer_start"] = ""
            ans_in["text"] = ""
            ans.append(ans_in)
            qas_in["answers"] = ans
            qas_in["question"] = " ".join(query_part[j])
            qas_in["id"] = str(id_)
            que2con[id_] = i
            id_ = id_+1
            qas.append(qas_in)


        par_in["qas"] = qas
        par.append(par_in)
        dic_in["paragraphs"] = par
        dic.append(dic_in)
    all["data"] = dic
    all["version"] = str(1.1)
    json.dump(all,f, indent=4)
    json.dump(que2con,f1, indent=4)
