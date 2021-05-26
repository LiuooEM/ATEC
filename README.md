1. 训练DE-CNN并生成数据
	在jupyter中

2. 评测DECNN
	在jupyter中

3. 训练boundary模块
训练数据需要修改
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

4. 训练num模块
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

5.在jupyter中评测DE-CNN并生成数据

6.在jupyter中评测DE-CNN加上num或boundary模块并关闭生成数据
