## 使用方法：
```python
from simple_util import SUtil


# 比较两个列表，返回删除的列表和新增的列表
print(SUtil.parse_diffrent_list([1,2,3], [1,2,3,4]))
([], [4])


# 安全删除列表中的元素
from simple_util import DeleteSafeList
a=[1,2,3,45,6,56,78]
safeDelete = DeleteSafeList(a)

for item in safeDelete:
    if item ==45:
        safeDelete.RemoveCurrent()
print(a)
# [1, 2, 3, 6, 56, 78]

```


<!-- 
python setup.py sdist bdist_wheel
twine upload dist/*
 -->