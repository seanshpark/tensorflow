/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
#include "tensorflow/lite/delegates/hexagon/builders/pad_builder.h"

#include <stdint.h>

#include "tensorflow/lite/core/c/builtin_op_data.h"
#include "tensorflow/lite/delegates/hexagon/hexagon_nn/hexagon_nn.h"
#include "tensorflow/lite/kernels/kernel_util.h"

namespace tflite {
namespace delegates {
namespace hexagon {
TfLiteStatus PadOpBuilder::PopulateSubGraph(const TfLiteIntArray* inputs,
                                            const TfLiteIntArray* outputs,
                                            TfLiteContext* context) {
  // Input data tensor.
  int tensor_id = inputs->data[0];
  const auto& input_tensor = context->tensors[tensor_id];
  AddInput(graph_builder_->GetHexagonTensorId(tensor_id));

  // Min/max values for input tensor.
  TF_LITE_ENSURE_STATUS(ComputeAndAddMinAndMax(context, input_tensor));

  // Padding tensor.
  tensor_id = inputs->data[1];
  const auto& padding_tensor = context->tensors[tensor_id];
  if (padding_tensor.allocation_type == kTfLiteMmapRo) {
    // If the padding input is a constant, bake it into the Hexagon graph as a
    // Const node.
    auto* const_padding_node =
        graph_builder_->AddConstNodeWithData(tensor_id, padding_tensor);
    AddInput(TensorID(const_padding_node->GetID(), 0));
  } else {
    AddInput(graph_builder_->GetHexagonTensorId(tensor_id));
  }

  // Hexagon outputs for this node.
  int output_batch_size, output_height_size, output_width_size,
      output_depth_size;
  GetDims(&output_batch_size, &output_height_size, &output_width_size,
          &output_depth_size, context->tensors[outputs->data[0]].dims);
  node_output_ = AddOutput(sizeof(uint8_t), 4,
                           {output_batch_size, output_height_size,
                            output_width_size, output_depth_size});
  AddOutput(sizeof(float), 4, kScalarShape);
  AddOutput(sizeof(float), 4, kScalarShape);

  return kTfLiteOk;
}

TfLiteStatus PadOpBuilder::RegisterOutputs(const TfLiteIntArray* outputs,
                                           TfLiteContext* context) {
  // Should be only 1 output.
  graph_builder_->AddTensorWithID(outputs->data[0], node_output_.first,
                                  node_output_.second);
  return kTfLiteOk;
}

PadOpBuilder::~PadOpBuilder() {}

OpBuilder* CreatePadBuilder(GraphBuilder* graph_builder, int op_type) {
  return new PadOpBuilder(graph_builder, op_type);
}

}  // namespace hexagon
}  // namespace delegates
}  // namespace tflite
