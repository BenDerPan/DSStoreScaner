# DSStoreScaner
通过扫描web站点存在的.DSStore文件，来尝试获取目标站点的物理文件结构。

## 运行所需环境
* python3.5

## 使用方法
`python SSScaner.py http://www.target.com/.DS_Store
`
运行后，通过访问Structures 属性获取结果。

示例输出如下：

`[*]Found File:http://localhost:8000/Report

[*]Found File:http://localhost:8000/index.html

[*]Found File:http://localhost:8000/PPT - 图片.docx

[*]Found File:http://localhost:8000/PPT.docx

[*]Found File:http://localhost:8000/Report/333.pdf

[*]Found File:http://localhost:8000/Report/1.docx

[*]Found File:http://localhost:8000/Report/0707.docx

[*]Found File:http://localhost:8000/Report/流程图素材

=========================Web Physical File Structure==========================

[
   
    "http://localhost:8000",
    
    "http://localhost:8000/Report",
    
    "http://localhost:8000/index.html",
    
    "http://localhost:8000/PPT - 图片.docx",
    
    "http://localhost:8000/PPT.docx",
    
    "http://localhost:8000/Report/333.pdf",
    
    "http://localhost:8000/Report/1.docx",
    
    "http://localhost:8000/Report/0707.docx",
    
    "http://localhost:8000/Report/流程图素材",


]
`