import numpy as np
import os

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)


train_data = object_detector.DataLoader.from_pascal_voc(
    r'E:\Codigos\ModelMakerALPR\ModifiedDatabase\images\Treino',
    r'E:\Codigos\ModelMakerALPR\ModifiedDatabase\xmlLabels\Treino',
    ['placa']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    r'E:\Codigos\ModelMakerALPR\ModifiedDatabase\images\Validacao',
    r'E:\Codigos\ModelMakerALPR\ModifiedDatabase\xmlLabels\Validacao',
    ['placa']
)

spec = model_spec.get('efficientdet_lite1')

model = object_detector.create(train_data, model_spec=spec, batch_size=5, train_whole_model=True, epochs=30, validation_data=val_data)
print(model.evaluate(val_data))
model.export(export_dir='.', tflite_filename='E:\Codigos\ModelMakerALPR/model.tflite')
print(model.evaluate_tflite('E:\Codigos\ModelMakerALPR/model.tflite', val_data))