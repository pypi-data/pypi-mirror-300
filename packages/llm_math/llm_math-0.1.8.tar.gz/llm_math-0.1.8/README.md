# LLM-Math

基于 [math-evaluation-harness](https://github.com/ZubinGou/math-evaluation-harness/) 改造的 plug-and-play 数学评测包.

### Usage

1. `set_seed(seed)`

   设置全局种子.

2. `basic_check(A, B)`

   检查 A, B 两个**纯数学**表达式是否一致，返回 True / False.

3. `check(prompt_type, data_name, target, pred)`

   检查 pred 是否与 target 一致，返回 True / False. target 即为数据集的某一行.

4. `engine = MathEval(model_path, args)`

   加载模型，args 为加载参数，见 [vllm.LLM](https://docs.vllm.ai/en/latest/dev/offline_inference/llm.html#vllm.LLM).

5. `engine.set_sampling_args(args)`

   设定推理参数，再次使用该命令可更新参数，见 [vllm.SamplingParams](https://docs.vllm.ai/en/latest/dev/sampling_params.html#vllm.SamplingParams).

6. `results = engine.generate(inputs)`

   进行**批量**推理.

7. `results = engine.chat(messages)`

   进行**单次**对话.

8. `engine.test(datasets=["gsm8k", "math"], prompt_type="direct", args)`

   进行评测. 可用的参数：

   `prompt_type="cot"`: prompt 的类型设置.

   `split="test"`: 测试集的选取.

   `num_test_sample=-1`, 随机选取进行测试的数量.

   `shuffle=True`, 是否随机打乱测试集.

   `save_outputs=True`, 是否保存模型输出.

- 支持的 prompt 类型: `tool-integrated`, `direct`, `cot`, `pal`, `self-instruct`, `self-instruct-boxed`, `tora`, `wizard_zs`, `platypus_fs`, `deepseek-math`, `kpmath`.

- 支持的数据集: `gsm8k`, `math`, `svamp`, `asdiv`, `mawps`, `tabmwp`, `mathqa`, `mmlu_stem`, `sat_math`.

### Notes

- 模型需支持 [vLLM](https://github.com/vllm-project/vllm).

- 在 `set_sampling_args` 中设定的 stop_word 在 `test` 中不起作用.

- 由于设置全局种子也会设定模型加载和推理的种子，所以模型加载和推理时不需要再次设定种子.

- `tensor_parallel_size` 默认设为 `torch.cuda.device_count()`.
