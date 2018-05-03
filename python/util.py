# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim

# maxFeatIndex = 560869
# def makeSparseTensor(feature):
#   index = []
#   value = [1] * len(feature)
#   for key in feature:
#     index.append(key)

#   index = torch.LongTensor([index])
#   value = torch.ByteTensor(value)
#   return torch.sparse.ByteTensor(index, value, torch.Size([maxFeatIndex]))

# class ctrClassifier(nn.Module):
#   #code from https://pytorch.org/tutorials/beginner/nlp/deep_learning_tutorial.html
#   def __init__(self, n_labels, n_examples):
#       super(ctrClassifier, self).__init__()

#       self.linear = nn.Linear(n_examples, n_labels)

#   def forward(self, feature_tensor):
#       return F.log_softmax(self.linear(feature_tensor), dim=1)