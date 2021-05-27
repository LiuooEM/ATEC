## Enhancing-Aspect-Term-Extraction-with-Number-Determining-and-Boundary-Modifying

Code for our XXX paper: ''

### Requirements

Install the packages listed in Requirements.

### Usage

1. Download BERT-Base (https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip), save it in BERT_BASE_DIR.

2. Delete placeholder in each empty folder.

   **Note that: you need to repeat step 3~8 for every domain**

3. Use jupyter notebook to run DE-CNN_train.ipynb (set [generate_data] to True).

4. Run DE-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to False).

5. Train Aspect Number Determining module:

   ```
   python3 run_aspect_number_determining_train.py
   --task_name=and
   --do_train=true
   --data_dir=train_data
   --vocab_file=BERT_BASE_DIR/vocab.txt
   --bert_config_file=BERT_BASE_DIR/bert_config.json
   --init_checkpoint=BERT_BASE_DIR/bert_model.ckpt
   --max_seq_length=85
   --train_batch_size=10
   --num_train_epochs=10
   --learning_rate=3e-5
   --output_dir=number_output_data
   --domain=laptop
   ```

   

6. Train Aspect Boundary Modifying module:

   ```
   python3 run_aspect_boundary_modifying_train.py
   --vocab_file=BERT_BASE_DIR/vocab.txt
   --bert_config_file=BERT_BASE_DIR/bert_config.json
   --init_checkpoint=BERT_BASE_DIR/bert_model.ckpt
   --do_train=True
   --train_batch_size=10
   --learning_rate=3e-5
   --num_train_epochs=10
   --max_seq_length=85
   --output_dir=boundary_output_data
   --domain=laptop
   ```

   

7. Run DE-CNN_evaluate.ipynb (set [generate_data], [num_process], [boundary_process] to True).

8. Check out the improvements after using post-process modules.



### Adaptation experiments

We examine the adaptation performance of the two post-process modules by replacing DE-CNN with new sequence taggers.

We have prepared two sequence taggers: BiLSTM-CNN and Seq2Seq4ATE.

The post-process modules have been trained, we can use them without retraining.

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





