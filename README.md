## Enhancing-Aspect-Term-Extraction-with-Number-Determining-and-Boundary-Modifying

Code for our XXX paper: 'Enhancing Aspect Term Extraction with Number Determining and Boundary Modifying'

### Requirements

Install the packages listed in Requirements.

We train our model on i9-10900K and 2080Ti (11G RAM). It costs about 50 minutes to train DE-CNN and post-process modules for each domain.

### Usage

1. Download BERT-Base (https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip), save it in BERT_BASE_DIR.

2. Delete placeholder in each empty folder.

   **Note that: you need to repeat step 3~8 for every domain**

3. Use jupyter notebook to run DE-CNN_train.ipynb (set [generate_data] to True).

4. Run DE-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to False).

5. Train Aspect Number Determining module:

   ```
   python3 run_aspect_number_determining_train.py \
   --task_name=and \
   --do_train=true \
   --data_dir=train_data \
   --vocab_file=BERT_BASE_DIR/vocab.txt \
   --bert_config_file=BERT_BASE_DIR/bert_config.json \
   --init_checkpoint=BERT_BASE_DIR/bert_model.ckpt \
   --max_seq_length=85 \
   --train_batch_size=10 \
   --num_train_epochs=10 \
   --learning_rate=3e-5 \
   --output_dir=number_output_data/ \
   --domain=laptop
   ```

   

6. Train Aspect Boundary Modifying module:

   ```
   python3 run_aspect_boundary_modifying_train.py \
   --vocab_file=BERT_BASE_DIR/vocab.txt \
   --bert_config_file=BERT_BASE_DIR/bert_config.json \
   --init_checkpoint=BERT_BASE_DIR/bert_model.ckpt \
   --do_train=True \
   --train_batch_size=10 \
   --learning_rate=3e-5 \
   --num_train_epochs=10 \
   --max_seq_length=85 \
   --output_dir=boundary_output_data/ \
   --domain=laptop
   ```

   

7. Run DE-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to True).

8. Check out the improvements after using post-process modules.



### Results

We do not randomly split the training/validation sets in the training process, the results of DE-CNN is stable. But the experimental results could vary on different machines when coupling DE-CNN with post-process modules. The reason is that Aspect Number Determining module and Aspect Boundary Modifying module have slight different in training process. We have not spent many time in searching for best hyperparameters, your retraining results may be higher than that reported in our paper.

| Model        | Lap14         | Res14         | Res15         | Res16         |
| :----------- | ------------- | ------------- | ------------- | ------------- |
| DE-CNN       | 81.67         | 84.05         | 66.53         | 74.48         |
| DE-CNN + AND | 83.62 (+1.95) | 87.14 (+3.09) | 70.67 (+4.14) | 77.61 (+3.13) |
| DE-CNN + ABM | 84.39 (+2.72) | 87.18 (+3.13) | 72.00 (+5.47) | 77.86 (+3.38) |
| DE-CNN + TP  | 84.89 (+3.22) | 88.41 (+4.36) | 73.47 (+6.94) | 78.73 (+4.25) |

Where AND denotes Aspect Number Determining module, ABM denotes Aspect Boundary Modifying module, TP denotes two post-process modules.

### Adaptation experiments

We examine the adaptation performance of the two post-process modules by replacing DE-CNN with new sequence taggers. We have prepared two sequence taggers: BiLSTM-CNN and Seq2Seq4ATE. The post-process modules have been trained, we can use them without retraining.

We give the usage of BiLSTM-CNN.

**Usage**

**Note that: you need to repeat step 1~4 for every domain**

1. Use jupyter notebook to run BiLSTM-CNN_train.ipynb.
2. Run BiLSTM-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to False).
3. Run BiLSTM-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to True).
4. Check out the improvements after using post-process modules.



### Configure

Our implementation is **highly configurable**, you can tune the different hyperparameters easily.

We also add Earlystopping mechanism to every model, you can try it.



### Acknowledgement

We must thank all authors from this paper: 'Double Embeddings and CNN-based Sequence Labeling for Aspect Extraction'. They have open source their code in https://github.com/howardhsu/DE-CNN. We adopt many codes from their projects. 

We thank all authors from this paper:  'Don’t Eclipse Your Arts Due to Small Discrepancies: Boundary Repositioning with a Pointer Network for Aspect Extraction'. Their code is available at https://www.aclweb.org/anthology/2020.acl-main.339/. We adopt some codes from their projects. 



### Citation

If you find our code useful, please cite our paper.

```
XXXXX
```





