#include <torch/extension.h>

#include "core/registration.h"
#include "ext.h"

TORCH_LIBRARY_EXPAND(TORCH_EXTENSION_NAME, m) {
  // ScalarType, a custom class for representing data types that supports
  // quantized types, declared here so it can be used when creating interfaces
  // for custom ops.
  vllm::ScalarTypeTorch::bind_class(m);

  // Aligning the number of tokens to be processed by each expert such
  // that it is divisible by the block size.
  m.def(
      "moe_align_block_size(Tensor topk_ids, int num_experts,"
      "                     int block_size, Tensor! sorted_token_ids,"
      "                     Tensor! experts_ids,"
      "                     Tensor! num_tokens_post_pad) -> ()");
  m.impl("moe_align_block_size", torch::kCUDA, &moe_align_block_size);

  // Apply topk softmax to the gating outputs.
  m.def(
      "topk_softmax(Tensor! topk_weights, Tensor! topk_indices, Tensor! "
      "token_expert_indices, Tensor gating_output) -> ()");
  m.impl("topk_softmax", torch::kCUDA, &topk_softmax);

#ifndef USE_ROCM
  m.def(
      "marlin_gemm_moe(Tensor! a, Tensor! b_q_weights, Tensor! sorted_ids, "
      "Tensor! topk_weights, Tensor! topk_ids, Tensor! b_scales, Tensor! "
      "b_zeros, Tensor! g_idx, Tensor! perm, Tensor! workspace, "
      "__torch__.torch.classes._moe_kernels_ops.ScalarType b_q_type, int size_m, "
      "int size_n, int size_k, bool is_k_full, int num_experts, int topk, "
      "int moe_block_size, bool replicate_input, bool apply_weights)"
      " -> Tensor");
  // Added in the implementation.
  // m.impl("marlin_gemm_moe", torch::kCUDA, &marlin_gemm_moe);
#endif

  m.def("silu_and_mul(Tensor! out, Tensor input) -> ()");
  m.impl("silu_and_mul", torch::kCUDA, &silu_and_mul);
}

REGISTER_EXTENSION(TORCH_EXTENSION_NAME)
