# How big are neural networks, and how much compute trains them?

![Parameters vs year](../../figures/ai_models.png)
![Compute vs parameters](../../figures/ai_compute.png)

## Parameters over time

Trainable parameters went from about 60,000 in LeNet-5 (1998) to more than a trillion in mixture-of-experts models (2021 onward). For mixture-of-experts models the bar runs from the parameters active for each token to the total. DeepSeek-V3, for example, uses 37B of its 671B parameters per token.

The two grey lines show brain counts for scale: 8.6×10¹⁰ neurons and 1.5×10¹⁴ neocortical synapses. **They are not bounds.** A parameter is not a synapse, and the brain lines say nothing about capability.

## Compute against size

For dense transformers, training compute is about C ≈ 6ND FLOP, where N is the parameter count and D is the number of training tokens. Hoffmann et al. (2022) found that, for a fixed budget, loss is lowest when D ≈ 20N. That gives the compute-optimal line C = 120N² (dash-dot).

- Points **below** the line (GPT-3, Gopher, PaLM) are larger than their compute budget could train optimally.
- Points **above** it (LLaMA, Llama 3.1, DeepSeek-V3, Kimi K2) trained on far more than 20 tokens per parameter. That makes them cheaper to run for their quality.

Compute marked "reported" comes from the paper. Compute marked "6ND" is derived (see `flop_basis` in `data/ai_models.csv`). For mixture-of-experts models, N is the active parameter count.
