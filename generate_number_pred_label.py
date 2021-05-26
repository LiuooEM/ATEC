import codecs
import json
import csv
import numpy as np

def generate_number_test_data(domain, run_epoch):
    output_file = 'output_data/' + domain + '/test_' + str(run_epoch) + '.utf8'
    f = codecs.open(output_file, "r", encoding="utf-8")
    pred_aspects_nums = []
    string = []
    true_label = []
    pre_label = []
    string_part = []
    true_label_part = []
    pre_label_part = []

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

    sentence = []
    sentence_idx = []
    aspects = []
    aspects_start = []
    aspects_end = []
    aspects_label = []

    #找出预测的方面，生成json文件
    for i in range(len(pre_label)):
        pred_aspects_nums_part = 0
        string_part = string[i]
        true_label_part = true_label[i]
        pre_label_part = pre_label[i]
        aspects_part = []
        for j in range(len(pre_label_part)):
            if pre_label_part[j] == '1' or (pre_label_part[j - 1] == '0' and pre_label_part[j] == '2'):
                aspects_start.append(j)
                end = 0
                for l in range(j + 1, len(pre_label_part)):
                    if pre_label_part[l] == '0' or pre_label_part[l] == '1':
                        end = l
                        break
                    if end == 0:
                        end = len(pre_label_part) - 1
                aspects_end.append(end - 1)
                for m in range(j, end):
                    #记录方面
                    aspects_part.append(string_part[m])
                #存储句子、方面、label
                sentence.append(string_part)
                aspects.append(aspects_part)
                sentence_idx.append(i)
                aspects_label.append(0)
                aspects_part = []
                pred_aspects_nums_part += 1
        pred_aspects_nums.append(pred_aspects_nums_part)
    #写入json文件
    file_name = 'output_data/' + domain + '/test_' + str(run_epoch) + '_number_test_data.json'
    f = codecs.open(file_name, "w", encoding="utf-8")

    all = {}
    dic = []
    for i in range(len(sentence)):
        sentence_part = sentence[i]
        aspects_part = aspects[i]
        aspects_label_part = aspects_label[i]
        sentence_idx_part = sentence_idx[i]
        aspects_start_part = aspects_start[i]
        aspects_end_part = aspects_end[i]
        
        dic_in = {}
        dic_in["title"] = "train_data"
        par = []
        par_in = {}
        
        par_in["sentence"] = " ".join(sentence_part)
        par_in["aspects"] = " ".join(aspects_part)
        par_in["aspects_label"] = aspects_label_part
        par_in["sentence_idx"] = sentence_idx_part
        par_in["aspects_start"] = aspects_start_part
        par_in["aspects_end"] = aspects_end_part
        par.append(par_in)
        dic_in["train"] = par
        dic.append(dic_in)
    all["data"] = dic
    all["version"] = str(0.1)
    json.dump(all, f, indent=4)
    f.close()
    return pred_aspects_nums

def json_to_csv(domain, run_epoch):
    #读取json文件
    json_filename = 'output_data/' + domain + '/test_' + str(run_epoch) + '_number_test_data.json'
    f = codecs.open(json_filename, "r", encoding="utf-8")
    dict = json.load(f)
    data = dict["data"]
    sentence = []
    aspects = []
    aspects_label = []
    sentence_idx = []
    aspects_start = []
    aspects_end = []
    
    len_aspects = []

    for i in range(len(data)):
        data_part = data[i]
        par = data_part["train"]
        par_1 = par[0]
        sentence_part = par_1["sentence"]
        aspects_part = par_1["aspects"]
        aspects_label_part = par_1["aspects_label"]
        sentence_idx_part = par_1["sentence_idx"]
        aspects_start_part = par_1["aspects_start"]
        aspects_end_part = par_1["aspects_end"]

        aspects.append(aspects_part)
        sentence.append(sentence_part)
        aspects_label.append(aspects_label_part)
        sentence_idx.append(sentence_idx_part)
        aspects_start.append(aspects_start_part)
        aspects_end.append(aspects_end_part)

        #分析aspect里面的异常数据
        len_aspects.append(len(aspects_part.split()))

    csv_test_filename = 'output_data/' + domain + '/test_' + str(run_epoch) + '_number_test_data.csv'
    with open(csv_test_filename, "w", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        header = ["aspects", "sentence", "aspects_label", "sentence_idx", "aspects_start", "aspects_end"]
        writer.writerow(header)
        for i in range(len(sentence)):
            data_row=[aspects[i], sentence[i], aspects_label[i], sentence_idx[i], aspects_start[i], aspects_end[i]]
            writer.writerow(data_row)
        csv_file.close()

def return_predicted_number_test_label(domain, run_epoch, pred_y):
    #思路：先读取csv和预测结果，然后构建一个pred_label列表，初始全为0。
    #先读取句子信息，如果存在就继续，不存在就跳过
    #遍历csv中的信息，按照预测结果填充
    
    sentence = []
    aspects = []
    aspects_label = []
    sentence_idx = []
    aspects_start = []
    aspects_end = []
    predicted_label = []
    
    #读取GE-CNN预测文件
    filename = 'output_data/' + domain + '/test_' + str(run_epoch) + '_number_test_data.csv'
    with open(filename, 'r') as f:
        quotechar = None
        reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
        lines = []
        for line in reader:
            lines.append(line)
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            sentence_idx.append(line[3])
            aspects_start.append(line[4])
            aspects_end.append(line[5])
    
    #读取BERT预测结果
    filename1 = 'number_output_data/' + domain + '/' + str(run_epoch) + '_test_results.tsv'
    with open(filename1, 'r') as f1:
        quotechar = None
        reader1 = csv.reader(f1, delimiter="\t", quotechar=quotechar)
        lines1 = []
        for line in reader1:
            lines1.append(line)
        for line in lines1:
            #如果预测为0的概率大于0.7才采信，不然就保留方面.......
            if float(line[0]) >= 0.7:
                predicted_label.append(0)
            else:
                predicted_label.append(1)
    
    #保证长度相同
    if len(sentence_idx) != len(predicted_label):
        print(len(sentence_idx))
        print(len(predicted_label))
        assert len(sentence_idx) == len(predicted_label)
    
    #开始构建pred_label
    for i in range(len(sentence_idx)):
        #第i个句子
        i_th = int(sentence_idx[i])
        start = aspects_start[i]
        end = aspects_end[i]
        #方面只有1个单词
        if start == end:
            if predicted_label[i] == 0:
                pred_y[i_th][int(start)] = 0
            else:
                pred_y[i_th][int(start)] = 1
        #方面有多个单词
        else:
            if predicted_label[i] == 0:
                for j in range(int(start), int(end) + 1):
                    pred_y[i_th][j] = 0
            else:
                pred_y[i_th][int(start)] = 1
                for j in range(int(start) + 1, int(end) + 1):
                    pred_y[i_th][j] = 2
    
    return pred_y
