import torch
import torchvision
import sys
import matplotlib
import matplotlib.pyplot as plt
# 设置字体为 SimHei（黑体）
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
import CyzHub


# 加载数据
def cyzgetimagdata(batch_size=256, resize=None):
    trans = [torchvision.transforms.ToTensor()]
    if resize:
        trans.insert(0, torchvision.transforms.Resize(resize))

    trans = torchvision.transforms.Compose(trans)

    if sys.platform.startswith('win'):
        num_workers = 0  # 0表示不用额外的进程来加速读取数据
    else:
        num_workers = 4

    # 获取图像数据
    test_data = torchvision.datasets.FashionMNIST(root="../root/imagedata", train=True, download=True,
                                                  transform=torchvision.transforms.ToTensor())
    train_data = torchvision.datasets.FashionMNIST(root="../root/imagedata", train=False, download=True,
                                                   transform=torchvision.transforms.ToTensor())
    return (torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=True, num_workers=num_workers),
            torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=num_workers))

#softmax
"""
该函数的目的就是为了让原来的模型结果，都保证为正，而且都分布在[0,1]区间内，和为1
index:是对特征与权值的线性求和的结果的指数
"""
def cyzsoftmax(O):
    index = torch.exp(O)
    return index/index.sum(1, keepdim=True)

#损失函数
"""
假设 y_hat 是如下的概率输出：
y_hat = torch.tensor([[0.7, 0.2, 0.1],  # 第 0 个样本对 3 个类别的预测概率
                      [0.1, 0.6, 0.3],  # 第 1 个样本对 3 个类别的预测概率
                      [0.4, 0.5, 0.1]]) # 第 2 个样本对 3 个类别的预测概率

如果 y 是 [2, 1]，那么 y_hat[[0, 1], y] 的结果将是：
    从 y_hat 中选择第 0 个样本的第 2 个类别的概率（0.1）
    从 y_hat 中选择第 1 个样本的第 1 个类别的概率（0.6）
"""
def cyzcrossfunction(y_hat, y):
    return -torch.log(y_hat[range(len(y_hat)),y])

#优化算法SGD梯度下降
"""
params:里面是权值和偏置
batch_size:是样本个数用来取平均值
"""
def cyzsgd(params, lr, batch_size):
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()


# 计算分类准确率
def cyzaccuracy(data_iter, net, device = None):
    if device is None and isinstance(net, torch.nn.Module):
        # 如果没指定device就使用net的device
        device = list(net.parameters())[0].device
    acc_sum, n = 0.0, 0
    with torch.no_grad():
        for X, y in data_iter:
            if isinstance(net, torch.nn.Module):
                net.eval()  # 评估模式, 这会关闭dropout
                acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
                net.train()  # 改回训练模式
            else:
                if ('is_training' in net.__code__.co_varnames):  # 如果有is_training这个参数is_training设置成False
                    acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
                else:
                    acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
            n += y.shape[0]
    return acc_sum / n

#训练
# num_epochs, lr = 5, 0.0256

def cyztrain(net, train_data, test_data, loss=None, num_epochs=5, batch_size=256, params=None, lr=None, optimizer=None,device=None):
    funplo = []
    train_loss_list = []
    test_acc_list = []
    train_acc_list = []
    """训练次数"""
    answer = 0
    net = net.to(device)
    print("training on ", device)
    for epoch in range(num_epochs):
        train_l_sum, train_acc_sum, n, count = 0.0, 0.0, 0,0
        for X, y in train_data:
            X, y = X.to(device), y.to(device)
            y_hat = net(X)
            los = loss(y_hat, y)
            los.sum().backward()
            #梯度下降
            if optimizer is None:
                cyzsgd(params, lr, batch_size)
            else:
                optimizer.step()
            train_l_sum += los.sum().cpu().item()
        #训练的损失值的和/每个批次的
        #训练的准确率
            train_acc_sum += (y_hat.argmax(dim=1) == y).sum().cpu().item()
            n += y.shape[0]
            count += 1
        #测试的准确率
        test_acc_sum = cyzaccuracy(test_data, net)
        train_loss_list.append(train_l_sum / n)
        train_acc_list.append(train_acc_sum / n)
        test_acc_list.append(test_acc_sum)
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>CYZ[{epoch+1}]<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(f"第[{epoch+1}]次训练：损失值：{train_l_sum/count}    训练准确率：{train_acc_sum/n}    测试准确率：{test_acc_sum}")
    if answer <= 0.9:
        print(f":):):):):):)这个模型一般般(:(:(:(:(:(:(:")
    funplo = [train_loss_list, train_acc_list, test_acc_list]
    data_x = range(1,num_epochs+1)
    CyzHub.cyzplt(data_x, '训练次数', '损失/准确率(值)', "训练结果", ['训练损失', '训练准确率', '测试准确率'], (5, 4), funplo,
                  ['blue', 'red', 'orange'])

#定义一个作图的方法
def cyzplt(x,xlabel, ylabel, title, legend, figsize, function, color=None):
    """设置图形大小"""
    plt.figure(figsize=figsize)
    """设置图标的标题"""
    plt.title(title)
    """设置x，y轴标签"""
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    """绘制多条线"""
    index = 0
    if color is None:
        color = []
        for i in legend:
            color.append('red')
            index += 1
    if type(function[0]) is not list:
        for fun, lab, color1 in zip(function, legend, color):
            plt.plot(x, fun(x), color=color1, label=lab)
    else:
        for fun, lab, color1 in zip(function, legend, color):
            plt.plot(x, fun, color=color1, label=lab)
    """显示图形"""
    plt.legend()
    plt.grid()
    plt.show()
"""
使用描述：
参数：
x: 对应的x轴的数据
x必须是一个tensor
xlabel：x轴的名称
ylable：y轴的名称
title：图表的标题
legend：图例，每条线的标注名称
figsize：图表的大小
function：函数的列表
color：每条线的颜色,默认是红色
"""

#定义Droput函数
def cyzdroupt(X, droupt):
    assert 0<= droupt <=1, '你输入的droupt的范围应该在[1,0]里面'
    if droupt == 1:
        return torch.zeros_like(X)
    elif droupt == 0:
        return X
    mask = (torch.randn(X.shape) > droupt)
    return x*mask/(1.0-droupt)

#-----------------------------------------卷积网络的相关的工具--------------------------------------------------
#1.互相关运算
def cyzhxg2d(X,K):
    h, w = K.shape
    #定义输出矩阵
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    """
    输出矩阵的大小：
        行数：输入矩阵的行数 - 核数组的行数 + 1
        列数：输入矩阵的列数 - 核数组的列数 + 1
    """
    #开始进行互相关运算,互相关运算的次数，就是输出矩阵的元素的个数
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i: i + h, j: j + w] * K).sum()

    return Y

#2.二维卷积层
class Cyzconv2d(nn.Module):
    def __init__(self, kernel_size):
        super(Cyzconv2d, self).__init__()
        self.kernel = nn.Parameter(torch.randn(kernel_size))
        self.bias = nn.Parameter(torch.randn(1))

    def forward(self, x):
        return cyzhxg2d(x, self.kernel) + self.bias

#3.多输入通道
def cyzmult(X, k):
    res = cyzhxg2d(X[0,:,:], k[0,:,:])
    for i in range(1, X.shape[0]):
        res += cyzhxg2d(X[i,:,:], k[i,:,:])
    return res

