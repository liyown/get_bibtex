"""
Example usage of get-bibtex library
使用示例：从多个来源获取文献引用
"""

from apiModels import (
    CrossRefBibTeX,
    DBLPBibTeX,
    GoogleScholarBibTeX,
    WorkflowBuilder
)

def example_crossref():
    """
    Example 1: Using CrossRef
    示例1：使用 CrossRef 获取引用
    """
    print("\n=== CrossRef Example ===")
    print("=== CrossRef 示例 ===\n")
    
    # Initialize with email (recommended)
    # 使用邮箱初始化（推荐）
    fetcher = CrossRefBibTeX(email="your.email@example.com")
    
    # Get citation by DOI
    # 通过 DOI 获取引用
    doi = "10.1145/3292500.3330919"
    print(f"Fetching DOI: {doi}")
    print(f"获取 DOI：{doi}")
    bibtex = fetcher.get_bibtex(doi)
    print("\nResult 结果：\n")
    print(bibtex)

def example_dblp():
    """
    Example 2: Using DBLP
    示例2：使用 DBLP 获取引用
    """
    print("\n=== DBLP Example ===")
    print("=== DBLP 示例 ===\n")
    
    fetcher = DBLPBibTeX()
    
    # Search by title
    # 通过标题搜索
    title = "Attention is all you need"
    print(f"Searching: {title}")
    print(f"搜索：{title}")
    bibtex = fetcher.get_bibtex(title)
    print("\nResult 结果：\n")
    print(bibtex)

def example_google_scholar():
    """
    Example 3: Using Google Scholar (requires API key)
    示例3：使用 Google Scholar（需要 API 密钥）
    """
    print("\n=== Google Scholar Example ===")
    print("=== Google Scholar 示例 ===\n")
    
    # Replace with your SerpAPI key
    # 替换为您的 SerpAPI 密钥
    api_key = "cbb23f2e312f9f3e3ea272c4903781db4540cb36afee4063b4ad8df3421edee7"
    
    try:
        fetcher = GoogleScholarBibTeX(api_key=api_key)
        title = "Deep learning with differential privacy"
        print(f"Searching: {title}")
        print(f"搜索：{title}")
        bibtex = fetcher.get_bibtex(title)
        print("\nResult 结果：\n")
        print(bibtex)
    except ValueError as e:
        print("Error: Please provide a valid SerpAPI key")
        print("错误：请提供有效的 SerpAPI 密钥")

def example_workflow():
    """
    Example 4: Using Workflow (multiple sources)
    示例4：使用工作流（多个来源）
    """
    print("\n=== Workflow Example ===")
    print("=== 工作流示例 ===\n")
    
    # Create workflow
    # 创建工作流
    workflow = WorkflowBuilder()
    
    # Add fetchers in order of preference
    # 按优先级添加获取器
    workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
    workflow.add_fetcher(DBLPBibTeX())
    
    # Process multiple queries
    # 处理多个���询
    queries = [
        "10.1145/3292500.3330919",  # DOI
        "Attention is all you need",  # Title 标题
        "Deep learning with differential privacy"  # Title 标题
    ]
    
    print("Processing queries:")
    print("处理查询：")
    for query in queries:
        print(f"- {query}")
    
    results = workflow.get_multiple_bibtex(queries)
    
    print("\nResults 结果：\n")
    for query, bibtex in results.items():
        print(f"Query 查询: {query}")
        print("BibTeX:")
        print(bibtex if bibtex else "Not found 未找到")
        print()

def example_file_processing():
    """
    Example 5: File Processing
    示例5：文件处理
    """
    print("\n=== File Processing Example ===")
    print("=== 文件处理示例 ===\n")
    
    # Create workflow
    # 创建工作流
    workflow = WorkflowBuilder()
    workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
    workflow.add_fetcher(DBLPBibTeX())
    
    # Process file
    # 处理文件
    input_file = "D:\\Workspace\\PYTHON\\get_bibtex\\test\\inputfile\\Bibliographyraw.txt"  # One query per line 每行一个查询
    output_file = "references.bib"
    
    print(f"Processing file: {input_file}")
    print(f"处理文件：{input_file}")
    print(f"Output to: {output_file}")
    print(f"输出到：{output_file}")
    
    try:
        workflow.process_file(input_file, output_file)
        print("\nSuccess! 处理成功！")
    except FileNotFoundError:
        print("\nError: Input file not found")
        print("错误：未找到输入文件")
        print("Please create a file named 'papers.txt' with your queries")
        print("请创建一个名为 'papers.txt' 的文件，包含您的查询")

def main():
    """
    Run all examples
    运行所有示例
    """
    print("Get BibTeX Examples")
    print("BibTeX 获取示例")
    print("=" * 50)
    
    example_crossref()
    example_dblp()
    example_google_scholar()
    example_workflow()
    example_file_processing()

if __name__ == "__main__":
    main()

