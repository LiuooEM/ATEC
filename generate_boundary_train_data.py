import json
import codecs
import csv
import numpy as np
import random
import os

def load_data(domain, epoch, run_epoch):
    add = str(run_epoch) + '_' + str(epoch) + ".utf8"
    output_file = 'train_data/' + domain + '/' + add
    f = codecs.open(output_file, "r", encoding="utf-8")

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

    context = []
    query = []
    answer = []
    answer_start_index = []
    for i in range(len(true_label)):
        string_part = string[i]
        true_label_part = true_label[i]
        pre_label_part = pre_label[i]
        query_part = []
        answer_part = []
        answer_start_index_part = []
        judge = 0
        if "1" not in pre_label_part:
            continue
        else:
            con = 0
            start = 0
            end = 0
            for j in range(len(pre_label_part)):
                if pre_label_part[j] == "1" and j + 1 < len(pre_label_part) and pre_label_part[j + 1] == '2':
                    start = j
                    con = 1
                    for m in range(j + 1, len(pre_label_part)):
                        if (pre_label_part[m] == "2" and m == len(pre_label_part) - 1) or (
                                pre_label_part[m] == "2" and m + 1 < len(pre_label_part) and (
                                pre_label_part[m + 1] == "0" or pre_label_part[m + 1] == "2")):
                            end = m
                            break
                elif pre_label_part[j] == "1" and j + 1 < len(pre_label_part) and (
                        pre_label_part[j + 1] == '0' or pre_label_part[j + 1] == '1'):
                    start = j
                    end = j
                    con = 1
                elif pre_label_part[j] == "1" and j + 1 == len(pre_label_part):
                    start = j
                    end = j
                    con = 1

                if con == 1:
                    a = 0
                    for p in range(start, end + 1):
                        if true_label_part[p] == "1" or true_label_part[p] == "2":
                            a = 1

                    if a == 1:
                        judge = 1
                        query_part.append(string_part[start:end + 1])

                        if true_label_part[start] == "2":
                            start_ind = start - 1
                            if start_ind < 0:
                                start_ans = 0
                            else:
                                while start_ind >= 0:
                                    if true_label_part[start_ind] == "1" or true_label_part[
                                        start_ind] == "0" or start_ind == 0:
                                        start_ans = start_ind
                                        break
                                    else:
                                        start_ind = start_ind - 1
                            end_ind = start
                            if end_ind + 1 == len(true_label_part):
                                end_ans = start
                            else:
                                while end_ind < len(true_label_part):

                                    if true_label_part[end_ind] == "2" and end_ind + 1 < len(
                                            true_label_part) and (
                                            true_label_part[end_ind + 1] == "0" or true_label_part[
                                        end_ind + 1] == "1"):
                                        end_ans = end_ind
                                        break

                                    elif true_label_part[end_ind] == "2" and end_ind + 1 == len(true_label_part):
                                        end_ans = end_ind
                                        break
                                    else:
                                        end_ind = end_ind + 1
                        else:

                            for t in range(start, len(true_label_part)):
                                if true_label_part[t] == "1" and t + 1 < len(true_label_part) and \
                                        true_label_part[t + 1] == "2":
                                    start_ans = t

                                    for q in range(start_ans, len(true_label_part)):
                                        if true_label_part[q] == "2" and q + 1 < len(true_label_part) and (
                                                true_label_part[q + 1] == "0" or true_label_part[q + 1] == "1"):
                                            end_ans = q
                                            break
                                        elif true_label_part[q] == "2" and q + 1 == len(true_label_part):
                                            end_ans = q
                                            break
                                    break
                                elif true_label_part[t] == "1" and t + 1 < len(true_label_part) and (
                                        true_label_part[t + 1] == "0" or true_label_part[t + 1] == "1"):
                                    start_ans = t
                                    end_ans = t
                                    break
                                elif true_label_part[t] == "1" and t + 1 == len(true_label_part):
                                    start_ans = t
                                    end_ans = t
                                    break
                        answer_part.append(string_part[start_ans:end_ans + 1])
                        answer_start_index_part.append(start_ans)
                    con = 0

        if judge == 1:
            context.append(string_part)
            query.append(query_part)
            answer.append(answer_part)
            answer_start_index.append(answer_start_index_part)

    return context, query, answer, answer_start_index
    
def generate_boundary_start_index(context,answer_start_index,answer):
    update_index = []
    for i in range(len(context)):
        update_index_part = []
        context_part = context[i]
        answer_part = answer[i]
        answer_start_index_part = answer_start_index[i]
        for j in range(len(answer_start_index_part)):
            ind = answer_start_index_part[j]
            if ind == 0:
                update_index_part.append(0)
            else:
                index = 0
                if ind > len(context_part):
                    print("!!!!!!!!!!!!!!!!!!!!!")
                    print(context_part)
                    print(answer_part[j])
                    print(ind)
                for m in range(0,ind):
                    index = index+len(context_part[m])+1
                update_index_part.append(index)
        update_index.append(update_index_part)

    return update_index

def generate_boundary_train_data(domain, context, query, answer,update_index,epoch,run_epoch):
    add = str(run_epoch) + '_' + str(epoch)+"_boundary_train_data.json"
    output_file = 'train_data/' + domain + '/' + add
    f = open(output_file,"w",encoding="utf-8")
    
    all = {}
    dic = []
    id_ = 0
    for i in range(len(context)):
        context_part = context[i]
        query_part = query[i]
        answer_part = answer[i]
        update_index_part = update_index[i]
        dic_in = {}
        dic_in["title"] = " "
        par = []
        par_in = {}
        par_in["context"] = " ".join(context_part)
        qas = []
        for j in range(len(query_part)):
            qas_in = {}
            ans = []
            ans_in = {}
            ans_in["answer_start"] = update_index_part[j]
            ans_in["text"] = " ".join(answer_part[j])
            ans.append(ans_in)
            qas_in["answers"] = ans
            qas_in["question"] = " ".join(query_part[j])
            qas_in["id"] = str(id_)
            id_ = id_+1
            qas.append(qas_in)
        par_in["qas"] = qas
        par.append(par_in)
        dic_in["paragraphs"] = par
        dic.append(dic_in)
    all["data"] = dic
    all["version"] = str(1.1)
    json.dump(all, f, indent=4)

def merge_load_data(f1):
    dict = json.load(f1)
    data = dict["data"]
    context = []
    answer = []
    question = []
    answer_start = []
    for i in range(len(data)):
        data_part = data[i]
        par = data_part["paragraphs"]
        par_1 = par[0]
        context_part = par_1["context"]
        context.append(context_part)
        qas = par_1["qas"]
        answer_part = []
        question_part = []
        answer_start_part = []
        for j in range(len(qas)):
            qas_part = qas[j]
            ans = qas_part["answers"]
            ans_1 = ans[0]
            ans_start = ans_1["answer_start"]
            text = ans_1["text"]
            ques = qas_part["question"]
            answer_part.append(text)
            question_part.append(ques)
            answer_start_part.append(ans_start)
        answer.append(answer_part)
        question.append(question_part)
        answer_start.append(answer_start_part)
    return context,answer,question,answer_start
    
def generate_merged_boundary_train_data(domain, context,answer,question,answer_start,q,run_epoch):
    add = str(run_epoch) + '_' + str(q)+"_boundary_train_data_merged.json"
    path = "train_data/" + domain + '/'
    file = os.path.join(path, add)
    f = codecs.open(file, "w", encoding="utf-8")

    all = {}
    dic = []
    id_ = 0
    for i in range(len(context)):
        context_part = context[i]
        query_part = question[i]
        answer_part = answer[i]
        update_index_part = answer_start[i]
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
            ans_in["answer_start"] = update_index_part[j]
            ans_in["text"] = answer_part[j]
            ans.append(ans_in)
            qas_in["answers"] = ans
            qas_in["question"] = query_part[j]
            qas_in["id"] = str(id_)
            id_ = id_ + 1
            qas.append(qas_in)
        par_in["qas"] = qas
        par.append(par_in)
        dic_in["paragraphs"] = par
        dic.append(dic_in)
    all["data"] = dic
    all["version"] = str(1.1)
    json.dump(all, f, indent=4)
    f.close()
    
def merge_boundary_train_data(domain, run_epoch, epoch):
    path = "train_data/" + domain + '/'
    for q in range(1, epoch + 1):
        if q-1 == 0:
            add_merge = "0_0_boundary_train_data.json"
        else:
            add_merge = str(run_epoch) + '_' + str(q-1)+"_boundary_train_data_merged.json"
        pre_file = os.path.join(path, add_merge)
        add = str(run_epoch) + '_' + str(q) + "_boundary_train_data.json"
        now_file = os.path.join(path, add)

        f1 = codecs.open(pre_file, "r", encoding="utf-8")
        f2 = codecs.open(now_file, "r", encoding="utf-8")

        context1,answer1,question1,answer_start1 = merge_load_data(f1)
        context2, answer2, question2, answer_start2 = merge_load_data(f2)
        for i in range(len(context2)):
            context2_part = context2[i]
            a = 0
            for j in range(len(context1)):
                if context2_part == context1[j]:
                    a = 1
                    for m in range(len(question2[i])):
                        if question2[i][m] not in question1[j]:
                            question1[j].append(question2[i][m])
                            answer1[j].append(answer2[i][m])
                            answer_start1[j].append(answer_start2[i][m])
            if a == 0:
                context1.append(context2_part)
                answer1.append(answer2[i])
                question1.append(question2[i])
                answer_start1.append(answer_start2[i])

        generate_merged_boundary_train_data(domain, context1,answer1,question1,answer_start1,q,run_epoch)
        f1.close()
        f2.close()
        
def merge_boundary_train_data_final(domain, run_epoch, epoch):
    path = "train_data/" + domain +'/'
    for q in range(1, run_epoch):
        add_merge = str(q-1) + '_' + str(epoch[q-1]) + "_boundary_train_data_merged.json"
        pre_file = os.path.join(path, add_merge)
        add = str(q) + '_' + str(epoch[q] - 1) + "_boundary_train_data_merged.json"
        now_file = os.path.join(path, add)

        f1 = codecs.open(pre_file, "r", encoding="utf-8")
        f2 = codecs.open(now_file, "r", encoding="utf-8")

        context1,answer1,question1,answer_start1 = merge_load_data(f1)
        context2, answer2, question2, answer_start2 = merge_load_data(f2)
        for i in range(len(context2)):
            context2_part = context2[i]
            a = 0
            for j in range(len(context1)):
                if context2_part == context1[j]:
                    a = 1
                    for m in range(len(question2[i])):
                        if question2[i][m] not in question1[j]:
                            question1[j].append(question2[i][m])
                            answer1[j].append(answer2[i][m])
                            answer_start1[j].append(answer_start2[i][m])
            if a == 0:
                context1.append(context2_part)
                answer1.append(answer2[i])
                question1.append(question2[i])
                answer_start1.append(answer_start2[i])

        generate_merged_boundary_train_data(domain, context1,answer1,question1,answer_start1,epoch[q],q)
        f1.close()
        f2.close()
    filename_ori = 'train_data/' + domain + '/' + str(run_epoch - 1) + '_' + str(epoch[run_epoch - 1]) + '_boundary_train_data_merged.json'
    filename_now = 'train_data/' + domain + '/' + 'boundary_train_data.json'
    os.rename(filename_ori, filename_now)
