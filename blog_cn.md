# get-bibtex：让文献引用管理更轻松的 Python 工具

## 引言

在学术研究中，管理参考文献是一项重要但耗时的工作。尤其是在写论文时，我们经常需要从不同的数据库中获取文献的引用格式。为了解决这个问题，我开发了 `get-bibtex` 这个 Python 库，它可以帮助研究者快速从多个学术数据库获取 BibTeX 格式的引用。

## 为什么选择 get-bibtex？

### 1. 多源支持
- CrossRef（最全面的 DOI 数据库）
- DBLP（计算机科学文献数据库）
- Google Scholar（需要 API key）

### 2. 智能工作流
```python
from get_bibtex import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

# 创建工作流
workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX("your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# 批量处理
papers = [
    "10.1145/3292500.3330919",  # 用 DOI
    "Attention is all you need"   # 用标题
]
results = workflow.get_multiple_bibtex(papers)
```

### 3. 简单易用
```python
from get_bibtex import CrossRefBibTeX

# 单个引用获取
fetcher = CrossRefBibTeX(email="your.email@example.com")
bibtex = fetcher.get_bibtex("10.1145/3292500.3330919")
print(bibtex)
```

### 4. 文件批处理
```python
# 从文件读取并保存
workflow.process_file(
    input_path="papers.txt",
    output_path="references.bib"
)
```

## 特色功能

1. **智能回退机制**
   - 当一个数据源失败时，自动尝试其他数据源
   - 保证最大程度获取引用信息

2. **进度追踪**
   - 使用 tqdm 显示处理进度
   - 清晰掌握批量处理状态

3. **错误处理**
   - 详细的日志记录
   - 优雅处理 API 限制和网络错误

4. **格式化输出**
   - 自动清理和格式化 BibTeX
   - 确保输出格式的一致性

## 使用场景

### 论文写作
当你在写论文时，可以直接用 DOI 或标题获取引用：
```python
from get_bibtex import CrossRefBibTeX

fetcher = CrossRefBibTeX()
citations = [
    "Machine learning",
    "Deep learning",
    "10.1038/nature14539"
]

for citation in citations:
    bibtex = fetcher.get_bibtex(citation)
    print(bibtex)
```

### 文献综述
批量处理大量文献引用：
```python
from get_bibtex import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX())
workflow.add_fetcher(DBLPBibTeX())

# 从文件读取文献列表
workflow.process_file("papers.txt", "bibliography.bib")
```

### 获取注意力机制相关论文的引用

假设我们需要获取以下论文的引用：

1. FedMSA: 联邦学习中的模型选择与适应系统
2. Attention Is All You Need: Transformer 的开创性工作
3. Non-Local Neural Networks: 非局部神经网络
4. ECA-Net: 高效的通道注意力机制
5. CBAM: 卷积块注意力模块

#### 使用 CrossRef 获取（通过 DOI）

```python
from apiModels import CrossRefBibTeX

fetcher = CrossRefBibTeX(email="your.email@example.com")

# FedMSA
bibtex = fetcher.get_bibtex("10.3390/s22197244")
print(bibtex)

# ECA-Net
bibtex = fetcher.get_bibtex("10.1109/cvpr42600.2020.01155")
print(bibtex)
```

输出示例：
```bibtex
@article{Sun_2022,
  title={FedMSA: A Model Selection and Adaptation System for Federated Learning},
  volume={22},
  ISSN={1424-8220},
  url={http://dx.doi.org/10.3390/s22197244},
  DOI={10.3390/s22197244},
  number={19},
  journal={Sensors},
  publisher={MDPI AG},
  author={Sun, Rui and Li, Yinhao and Shah, Tejal and Sham, Ringo W. H. and Szydlo, Tomasz and Qian, Bin and Thakker, Dhaval and Ranjan, Rajiv},
  year={2022},
  month=sep,
  pages={7244}
}
```

#### 使用 DBLP 获取（通过标题）

```python
from apiModels import DBLPBibTeX

fetcher = DBLPBibTeX()

# CBAM
bibtex = fetcher.get_bibtex("CBAM: Convolutional Block Attention Module")
print(bibtex)
```

输出示例：
```bibtex
@article{DBLP:journals/access/WangZHLL24,
  author       = {Niannian Wang and Zexi Zhang and Haobang Hu and Bin Li and Jianwei Lei},
  title        = {Underground Defects Detection Based on {GPR} by Fusing Simple Linear Iterative Clustering Phash (SLIC-Phash) and Convolutional Block Attention Module (CBAM)-YOLOv8},
  journal      = {{IEEE} Access},
  volume       = {12},
  pages        = {25888--25905},
  year         = {2024},
  url          = {https://doi.org/10.1109/ACCESS.2024.3365959},
  doi          = {10.1109/ACCESS.2024.3365959}
}
```

#### 使用工作流获取多个引用

```python
from apiModels import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

# 创建工作流
workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# 准备查询列表
queries = [
    "FedMSA: A Model Selection and Adaptation System for Federated Learning",
    "Attention Is All You Need",
    "Non-Local Neural Networks",
    "ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks",
    "CBAM: Convolutional Block Attention Module"
]

# 获取所有引用
results = workflow.get_multiple_bibtex(queries)

# 打印结果
for query, bibtex in results.items():
    print(f"\n查询: {query}")
    print(f"引用:\n{bibtex if bibtex else '未找到'}")
```

#### 文件批处理
你可以创建一个工作流来处理包含多个引用的文件。首先，创建工作流并添加数据源:
```python
from apiModels import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# 处理文件
workflow.process_file("papers.txt", "references.bib")
```
输入示例：
papers.txt
```
FedMSA: A Model Selection and Adaptation System for Federated Learning
Attention Is All You Need
Non-Local Neural Networks
ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks
CBAM: Convolutional Block Attention Module
```

输出示例：
references.bib
```
% Query: FedMSA: A Model Selection and Adaptation System for Federated Learning
% Source: CrossRefBibTeX
@article{Sun_2022, title={FedMSA: A Model Selection and Adaptation System for Federated Learning}, volume={22}, ISSN={1424-8220}, url={http://dx.doi.org/10.3390/s22197244}, DOI={10.3390/s22197244}, number={19}, journal={Sensors}, publisher={MDPI AG}, author={Sun, Rui and Li, Yinhao and Shah, Tejal and Sham, Ringo W. H. and Szydlo, Tomasz and Qian, Bin and Thakker, Dhaval and Ranjan, Rajiv}, year={2022}, month=sep, pages={7244} }

% Query: Attention Is All You Need
% Source: DBLPBibTeX
@inproceedings{DBLP:conf/dac/ZhangYY21,
  author       = {Xiaopeng Zhang and
                  Haoyu Yang and
                  Evangeline F. Y. Young},
  title        = {Attentional Transfer is All You Need: Technology-aware Layout Pattern
                  Generation},
  booktitle    = {58th {ACM/IEEE} Design Automation Conference, {DAC} 2021, San Francisco,
                  CA, USA, December 5-9, 2021},
  pages        = {169--174},
  publisher    = {{IEEE}},
  year         = {2021},
  url          = {https://doi.org/10.1109/DAC18074.2021.9586227},
  doi          = {10.1109/DAC18074.2021.9586227},
  timestamp    = {Wed, 03 May 2023 17:06:11 +0200},
  biburl       = {https://dblp.org/rec/conf/dac/ZhangYY21.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}

% Query: Non-Local Neural Networks
% Source: CrossRefBibTeX
@article{Xu_2024, title={Adaptive selection of local and non-local attention mechanisms for speech enhancement}, volume={174}, ISSN={0893-6080}, url={http://dx.doi.org/10.1016/j.neunet.2024.106236}, DOI={10.1016/j.neunet.2024.106236}, journal={Neural Networks}, publisher={Elsevier BV}, author={Xu, Xinmeng and Tu, Weiping and Yang, Yuhong}, year={2024}, month=jun, pages={106236} }

% Query: ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks
% Source: CrossRefBibTeX
@inproceedings{Wang_2020, title={ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks}, url={http://dx.doi.org/10.1109/cvpr42600.2020.01155}, DOI={10.1109/cvpr42600.2020.01155}, booktitle={2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, publisher={IEEE}, author={Wang, Qilong and Wu, Banggu and Zhu, Pengfei and Li, Peihua and Zuo, Wangmeng and Hu, Qinghua}, year={2020}, month=jun, pages={11531–11539} }

% Query: CBAM: Convolutional Block Attention Module
% Source: DBLPBibTeX
@article{DBLP:journals/access/WangZHLL24,
  author       = {Niannian Wang and
                  Zexi Zhang and
                  Haobang Hu and
                  Bin Li and
                  Jianwei Lei},
  title        = {Underground Defects Detection Based on {GPR} by Fusing Simple Linear
                  Iterative Clustering Phash (SLIC-Phash) and Convolutional Block Attention
                  Module (CBAM)-YOLOv8},
  journal      = {{IEEE} Access},
  volume       = {12},
  pages        = {25888--25905},
  year         = {2024},
  url          = {https://doi.org/10.1109/ACCESS.2024.3365959},
  doi          = {10.1109/ACCESS.2024.3365959},
  timestamp    = {Sat, 16 Mar 2024 15:09:59 +0100},
  biburl       = {https://dblp.org/rec/journals/access/WangZHLL24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}


```

## 安装方式

使用 pip：
```bash
pip install get-bibtex
```

使用 Poetry：
```bash
poetry add get-bibtex
```

## 最佳实践

1. **使用邮箱注册**
   ```python
   fetcher = CrossRefBibTeX(email="your.email@example.com")
   ```
   这样可以获得更好的 API 访问优先级

2. **合理使用工作流**
   ```python
   workflow = WorkflowBuilder()
   workflow.add_fetcher(CrossRefBibTeX())  # 主要源
   workflow.add_fetcher(DBLPBibTeX())      # 备用源
   ```
   按照可靠性顺序添加数据源

3. **批量处理时添加延时**
   处理大量引用时，建议使用内置的延时机制，避免触发 API 限制

4. **获取 SerpAPI Key**

   要使用 Google Scholar 功能，你需要一个 SerpAPI key。以下是获取步骤：

   1. **注册 SerpAPI 账号**
      - 访问 [SerpAPI 官网](https://serpapi.com/)
      - 点击右上角的 "Sign Up" 按钮
      - 填写注册信息（邮箱、密码等）

   2. **选择合适的计划**
      - 免费计划：每月 100 次搜索
      - 付费计划：根据需求选择不同级别
      - 对于测试和个人使用，免费计划通常足够

   3. **获取 API Key**
      - 登录后进入 [Dashboard](https://serpapi.com/dashboard)
      - 在 "API Key" 部分找到你的密钥
      - 复制密钥以在代码中使用

   4. **使用示例**
      ```python
      from apiModels import GoogleScholarBibTeX
      
      # 初始化 Google Scholar 获取器
      fetcher = GoogleScholarBibTeX(api_key="your-serpapi-key")
      
      # 获取引用
      bibtex = fetcher.get_bibtex("Deep learning with differential privacy")
      print(bibtex)
      ```

   5. **注意事项**
      - 保护好你的 API key，不要公开分享
      - 监控使用量，避免超出限制
      - 合理设置请求间隔（建议至少 1 秒）
      - 在生产环境中使用环境变量存储 API key
      ```python
      import os
      
      api_key = os.getenv("SERPAPI_KEY")
      fetcher = GoogleScholarBibTeX(api_key=api_key)
      ```

   6. **使用建议**
      - 优先使用 CrossRef 和 DBLP
      - 只在找不到结果时使用 Google Scholar
      - 批量处理时注意 API 使用限制
      ```python
      # 推荐的工作流顺序
      workflow = WorkflowBuilder()
      workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
      workflow.add_fetcher(DBLPBibTeX())
      workflow.add_fetcher(GoogleScholarBibTeX(api_key="your-serpapi-key"))
      ```

## 未来展望

1. 支持更多数据源
2. 添加引用格式转换功能
3. 提供图形用户界面
4. 支持更多自定义选项

## 结语

`get-bibtex` 致力于简化学术写作中的文献管理工作。无论是单篇论文还是文献综述，它都能帮助你高效地获取和管理文献引用。欢迎通过 GitHub 参与项目开发，提出建议或反馈问题。

## 相关链接

- GitHub 仓库：[get-bibtex](https://github.com/UnderTurrets/get_bibtex)
- 问题反馈：[Issues](https://github.com/UnderTurrets/get_bibtex/issues)
- PyPI 页面：[get-bibtex](https://pypi.org/project/get-bibtex/) 