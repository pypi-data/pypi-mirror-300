import CyzHub as cyz
import torch

#1.互相关运算例子
X = torch.randint(1, 5, (3,3))
K = torch.tensor([
    [0,1],
    [2,3]
])

print(X)
print(K)

print(cyz.cyzhxg2d(X,K))

#2.二维卷积层示例:通过数据学习核数组

cyzconv = cyz.Cyzconv2d(kernel_size=(1,2))

X = torch.ones(6, 8)
X[:, 2:6] = 0

K = torch.tensor([[1, -1]])

Y = cyzhxg2d(X, K)

step = 50
lr = 0.01
for i in range(step):
    Y_hat = cyzconv(X)
    l = ((Y_hat - Y)**2).sum()
    l.backward()
    cyzconv.kernel.data -= lr * cyzconv.kernel.grad
    cyzconv.bias.data -= lr * cyzconv.bias.grad

    cyzconv.kernel.grad.fill_(0)
    cyzconv.bias.grad.fill_(0)
    if (i + 1) % 5 == 0:
        print('Step %d, loss %.3f' % (i + 1, l.item()))
print("weight: ", cyzconv.kernel.data)
print("bias: ", cyzconv.bias.data)
