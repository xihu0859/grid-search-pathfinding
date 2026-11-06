# 网格寻路与搜索算法比较

[English README](README.md) · [代码](hidden_path.py) · [示例](examples/) · [结果](results/)

实现 BFS、DFS、UCS、贪心搜索、A* 与爬山算法，在带墙、不同地形成本和传送门的二维地图中寻找目标。
程序输出节点展开顺序、找到的路径和总成本，并按坐标与入队顺序处理优先级相同的节点。

这个项目展示的重点是：步数少不一定成本低，依赖启发式也不一定能找到解。在地形／传送门示例中，
BFS 和 DFS 的路径成本是 6，UCS、贪心与 A* 得到 5，爬山算法因无法严格降低启发值而停在平台。
这是一张示例地图的结果，不是所有输入上的算法排名。

只需 Python 标准库，不需要下载数据。运行 `python hidden_path.py U examples/terrain_portal.txt`，
或用 `python scripts/compare_searches.py` 比较全部策略。测试命令是 `python -m unittest discover -s tests -v`。

README 同时说明传送门下 Manhattan 启发式的局限，没有宣称本实现的 A* 对任意传送地图都保证最优。
