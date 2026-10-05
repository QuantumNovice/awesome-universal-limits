# How close are AI systems to the ceiling of their benchmarks?

![Benchmark scores](../../figures/ai_benchmarks.png)

Each panel is one benchmark, drawn with the same three layers as the physics charts.

1. **Hard ceiling (red).** No score can pass 100%. On MMLU the real ceiling is lower. Gema et al. (2025) found about 6.5% of its questions contain errors, so a perfect model would top out near 93.5% (dotted amber).
2. **Reference levels.** Random guessing (blue, shaded below) and the human baseline (dashed grey). The human baseline is:
   - ImageNet: a trained annotator, at 5.1% top-5 error.
   - MMLU: the authors' estimate of expert accuracy.
   - GPQA: PhD-level domain experts, at 65%.
   - ARC-AGI-1: the average person in the H-ARC study.
3. **Reported results.** Each point is a score as reported by its authors or developer, joined in time order.

**Read with care.** Evaluation settings differ: few-shot or zero-shot, chain of thought or not, a single attempt or majority voting, and different scaffolds for SWE-bench. The `setting` column of `data/ai_benchmarks.csv` records each one. These are not leaderboard-verified numbers. A benchmark near its ceiling stops measuring progress, and that is why ImageNet, MMLU and GSM8K have been replaced by harder tests.
