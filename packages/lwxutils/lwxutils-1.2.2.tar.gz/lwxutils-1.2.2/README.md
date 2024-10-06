# 主要用于训练结果的文件持久化
## 功能
- 保存训练结果到训练产出目录root/ ```runs```

## 手动安装
```
 	pip install lwxutils -i https://pypi.org/simple
	
	升级
	pip install --upgrade lwxutils -i https://pypi.org/simple
```

## 数据结构

| 字段 | 说明 | 备注 |
| ---- | ----- | ----- |
|   epoch   |    迭代次数   |       |
|   time   |    报告时间   |       |
|   train_loss   |    训练损失   |       |
|   val_map   |    验证mAP   |       |
|   time   |    迭代   |       |