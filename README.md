1. 下载bert放在BERT_BASE_DIR文件夹下

2. 使用jupyter notebook打开DE-CNN_train.ipynb.你可以设置各种参数然后训练DE-CNN。

3. 打开DE-CNN_evaluate.ipynb.评测模型。

4. 训练Aspect Number Determining模块
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
  #you can set this parameter to [laptop], [reataurant], [reataurant14], [reataurant15]
  --domain=laptop

5. 训练Aspect Boundary Modifying模块
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
  #you can set this parameter to [laptop], [reataurant], [reataurant14], [reataurant15]
  --domain=laptop
