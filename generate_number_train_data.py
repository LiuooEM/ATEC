import json
import codecs
import csv
import numpy as np
import random
import os
from sklearn.model_selection import train_test_split

def generate_number_train_data(domain, runs, epochs):
	#读取json文件
        #json_filename = 'train_data/' + str(runs - 1) + '_' + str(epochs - 1) + '_merge.json'
	json_filename = 'train_data/' + domain + '/' + str(runs - 1) + '_' + str(epochs[runs - 1]) + '_number_train_data_merged.json'
	f = codecs.open(json_filename, "r", encoding="utf-8")
	dict = json.load(f)
	data = dict["data"]
	sentence = []
	aspects = []
	aspects_label = []
	count_label_total = 0
	count_over_8 = 0
	len_aspects = []
	for i in range(len(data)):
		data_part = data[i]
		par = data_part["train"]
		par_1 = par[0]
		sentence_part = par_1["sentence"]
		aspects_part = par_1["aspects"]
		aspects_label_part = par_1["aspects_label"]
		
		#剔除aspects过长且label为0的数据
		if len(aspects_part.split()) >= 8 and aspects_label_part == 0:
		    count_over_8 += 1
		else:
		    aspects.append(aspects_part)
		    sentence.append(sentence_part)
		    if aspects_label_part == 1:
		        count_label_total += 1
		    aspects_label.append(aspects_label_part)
		
		#分析aspect里面的异常数据
		len_aspects.append(len(aspects_part.split()))

	sentence_pos = []
	aspects_pos = []
	aspects_label_pos = []
	sentence_neg = []
	aspects_neg = []
	aspects_label_neg = []
	for i in range(len(sentence)):
		sentence_part = sentence[i]
		aspects_part = aspects[i]
		aspects_label_part = aspects_label[i]
		
		#剔除aspects过长且label为0的数据
		if aspects_label_part == 1:
		    sentence_pos.append(sentence_part)
		    aspects_pos.append(aspects_part)
		    aspects_label_pos.append(aspects_label_part)
		else:
		    sentence_neg.append(sentence_part)
		    aspects_neg.append(aspects_part)
		    aspects_label_neg.append(aspects_label_part)

	random_state = 1
	#保留2位小数，并四舍五入
	test_size = round(1 - (len(sentence_pos) / len(sentence_neg)), 2)
	sentence_keep, sentence_aban = train_test_split(sentence_neg,
		                                            test_size = test_size,
		                                            random_state = random_state)
	aspects_keep, aspects_aban = train_test_split(aspects_neg,
		                                          test_size = test_size,
		                                          random_state = random_state)
	aspects_label_keep, aspects_label_aban = train_test_split(aspects_label_neg,
		                                                      test_size = test_size,
		                                                      random_state = random_state)
	

	sentence_final = sentence_pos + sentence_keep
	aspects_final = aspects_pos + aspects_keep
	aspects_label_final = aspects_label_pos + aspects_label_keep
	#保证shuffle后对应关系不变
	r=random.random
	random.seed(215)
	random.shuffle(sentence_final, random=r)
	random.seed(215)
	random.shuffle(aspects_final, random=r)
	random.seed(215)
	random.shuffle(aspects_label_final, random=r)

	csv_train_filename = 'train_data/' + domain + '/number_train_data.csv'
	#写入train数据
	with open(csv_train_filename, "w", newline = '') as csv_file:
		writer = csv.writer(csv_file, delimiter="\t")
		header = ["aspects", "sentence", "aspects_label"]
		writer.writerow(header)
		for i in range(len(sentence_final)):
		    data_row=[aspects_final[i], sentence_final[i], aspects_label_final[i]]
		    writer.writerow(data_row)
		csv_file.close()

def save_number_train_data(domain, run_epoch, epoch):
	#读取预测数据
	output_file = 'train_data/' + domain + '/' + str(run_epoch) + '_' + str(epoch) + '.utf8'
	f = codecs.open(output_file, "r", encoding="utf-8")

	string = []
	true_label = []
	pre_label = []
	string_part = []
	true_label_part = []
	pre_label_part = []

	for line in f:
		"""
		一行有三个字符串，第一个是单词，第二个是真正的标注，第三是预测的标注
		遇到空行，重置。最终使用的输出是string = []，true_label = []，pre_label = []
		"""
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
	
	
	#找出不正确的方面
	#以pre为基，如果不完全与true相同就记录
	"""
	思路：
	1.先把true_label里面的方面全记下来
	2.再使用pre作为基找出不同的方面
	3.需要记录句子、方面、标签
	"""

	sentence = []
	#单个方面
	aspects = []
	#方面是否正确
	aspects_label = []

	#找出每个预测文件的符合数据
	for i in range(len(pre_label)):
		string_part = string[i]
		true_label_part = true_label[i]
		pre_label_part = pre_label[i]
		aspects_part = []
		#记录所有正确的方面
		for j in range(len(true_label_part)):
		    if true_label_part[j] == '1':
		        for l in range(j, len(true_label_part)):
		            if true_label_part[l] != '0':
		                #记录方面
		                aspects_part.append(string_part[l])
		            else:
		                #存储句子、方面、label
		                sentence.append(string_part)
		                aspects.append(aspects_part)
		                aspects_label.append(1)
		                aspects_part = []
		                break
		#记录预测的且和真正的不同的方面
		for j in range(len(pre_label_part)):
		    if pre_label_part[j] == '1' or (pre_label_part[j - 1] == '0' and pre_label_part[j] == '2'):
		        #不同
		        if true_label_part[j] != '1':
		            for l in range(j, len(pre_label_part)):
		                if pre_label_part[l] != '0':
		                    #记录方面
		                    aspects_part.append(string_part[l])
		                else:
		                    #存储句子、方面、label
		                    sentence.append(string_part)
		                    aspects.append(aspects_part)
		                    aspects_label.append(0)
		                    aspects_part = []
		                    break
		        else:
		            end = 0
		            for l in range(j, len(pre_label_part)):
		                if pre_label_part[l] == '0':
		                    end = l
		                    break
		                if end == 0:
		                    end = len(pre_label_part) - 1
		                #对比直到pre的最后一个单词的后一位，必须都全部相等才是完全相等的，否则都为结束错误
		                for k in range(l + 1, end + 1):
		                    if true_label_part[j] != pre_label_part[j]:
		                        #记录和存储预测的错误方面
		                        for m in range(j, end + 1):
		                            if pre_label_part[l] != '0':
		                                #记录方面
		                                aspects_part.append(string_part[m])
		                            else:
		                                #存储句子、方面、label
		                                sentence.append(string_part)
		                                aspects.append(aspects_part)
		                                aspects_label.append(0)
		                                aspects_part = []
		                                break
		                        break
		                        

	#写入json文件
	file_name = 'train_data/' + domain + '/' + str(run_epoch) + '_' + str(epoch) + '_number_train_data.json'
	f = codecs.open(file_name, "w", encoding="utf-8")

	all = {}
	dic = []
	for i in range(len(sentence)):
		sentence_part = sentence[i]
		aspects_part = aspects[i]
		aspects_label_part = aspects_label[i]
		
		dic_in = {}
		dic_in["title"] = "train_data"
		par = []
		par_in = {}
		
		par_in["sentence"] = " ".join(sentence_part)
		par_in["aspects"] = " ".join(aspects_part)
		par_in["aspects_label"] = aspects_label_part
		par.append(par_in)
		dic_in["train"] = par
		dic.append(dic_in)
	all["data"] = dic
	all["version"] = str(0.1)
	json.dump(all, f, indent=4)
	f.close()
	

def merge_load_data(f1):
    dict = json.load(f1)
    data = dict["data"]
    sentence = []
    aspects = []
    aspects_label = []

    for i in range(len(data)):
        data_part = data[i]
        par = data_part["train"]
        par_1 = par[0]
        sentence_part = par_1["sentence"]
        sentence.append(sentence_part)
        aspects_part = par_1["aspects"]
        aspects.append(aspects_part)
        aspects_label_part = par_1["aspects_label"]
        aspects_label.append(aspects_label_part)
        
    return sentence, aspects, aspects_label
    
def generate_merged_number_train_data(domain, sentence, aspects, aspects_label, q, run_epoch):
    add = str(run_epoch) + '_' + str(q)+"_number_train_data_merged.json"
    path = "train_data/" + domain + '/'
    file = os.path.join(path, add)
    f = codecs.open(file, "w", encoding="utf-8")

    all = {}
    dic = []
    id_ = 0
    for i in range(len(sentence)):
        sentence_part = sentence[i]
        aspects_part = aspects[i]
        aspects_label_part = aspects_label[i]
        
        dic_in = {}
        dic_in["title"] = "train_data"
        par = []
        par_in = {}
        par_in["sentence"] = sentence_part
        par_in["aspects"] = aspects_part
        par_in["aspects_label"] = aspects_label_part
        
        par.append(par_in)
        dic_in["train"] = par
        dic.append(dic_in)
    all["data"] = dic
    all["version"] = str(0.1)
    json.dump(all, f, indent=4)
    f.close()
    
def merge_number_train_data(domain, run_epoch, epoch):
    path = "train_data/" + domain + '/'
    for q in range(1, epoch + 1):
        """
        每次顺序取2个，将这两个融合，然后后移一位，再重复，所以最后一个19是包含前面所有的
        最终的结果是存在完全正确的，也存在有瑕疵的
        """
        if q-1 == 0:
            add_merge = "0_0_number_train_data.json"
        else:
            add_merge = str(run_epoch) + '_' + str(q-1)+"_number_train_data_merged.json"
        pre_file = os.path.join(path, add_merge)
        add = str(run_epoch) + '_' + str(q) + "_number_train_data.json"
        now_file = os.path.join(path, add)
        f1 = codecs.open(pre_file, "r", encoding="utf-8")
        f2 = codecs.open(now_file, "r", encoding="utf-8")
        
        #调用merge_load_data()
        #f1是上一个
        sentence1, aspects1, aspects_label1 = merge_load_data(f1)
        #f2是当前的
        sentence2, aspects2, aspects_label2 = merge_load_data(f2)
        
        #如果不存在就添加，然后再重新生成json文件
        for i in range(len(sentence2)):
            sentence2_part = sentence2[i]
            flag_a = 0
            flag_s = 0
            #过完一遍以后，如果确认
            for j in range(len(sentence1)):
                if sentence2_part == sentence1[j]:
                    flag_s = 1
                    if aspects2[i] == aspects1[j]:
                        flag_a = 1
            if flag_s == 0:
                aspects1.append(aspects2[i])
                sentence1.append(sentence2[i])
                aspects_label1.append(aspects_label2[i])
            elif flag_a == 0:
                aspects1.append(aspects2[i])
                sentence1.append(sentence2[i])
                aspects_label1.append(aspects_label2[i])
        
        generate_merged_number_train_data(domain, sentence1, aspects1, aspects_label1, q, run_epoch)
        f1.close()
        f2.close()
        
def merge_number_train_data_final(domain, run_epoch, epoch):
    path = "train_data/" + domain + '/'
    for q in range(1, run_epoch):
        """
        每次顺序取2个，将这两个融合，然后后移一位，再重复，所以最后一个19是包含前面所有的
        最终的结果是存在完全正确的，也存在有瑕疵的
        """
        
        #add_merge = str(q-1) + '_' + str(epoch - 1) + "_merge.json"
        add_merge = str(q-1) + '_' + str(epoch[q - 1]) + "_number_train_data_merged.json"
        pre_file = os.path.join(path, add_merge)
        #add = str(q) + '_' + str(epoch - 1) + "_merge.json"
        add = str(q) + '_' + str(epoch[q] - 1) + "_number_train_data_merged.json"
        now_file = os.path.join(path, add)
        
        f1 = codecs.open(pre_file, "r", encoding="utf-8")
        f2 = codecs.open(now_file, "r", encoding="utf-8")
        
        #调用merge_load_data()
        #f1是上一个
        sentence1, aspects1, aspects_label1 = merge_load_data(f1)
        #f2是当前的
        sentence2, aspects2, aspects_label2 = merge_load_data(f2)
        
        #如果不存在就添加，然后再重新生成json文件
        for i in range(len(sentence2)):
            sentence2_part = sentence2[i]
            flag_a = 0
            flag_s = 0
            #过完一遍以后，如果确认
            for j in range(len(sentence1)):
                if sentence2_part == sentence1[j]:
                    flag_s = 1
                    if aspects2[i] == aspects1[j]:
                        flag_a = 1
            if flag_s == 0:
                aspects1.append(aspects2[i])
                sentence1.append(sentence2[i])
                aspects_label1.append(aspects_label2[i])
            elif flag_a == 0:
                aspects1.append(aspects2[i])
                sentence1.append(sentence2[i])
                aspects_label1.append(aspects_label2[i])
        
        generate_merged_number_train_data(domain, sentence1, aspects1, aspects_label1, epoch[q], q)
        f1.close()
        f2.close()
