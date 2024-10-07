import pickle
import matplotlib.pyplot as plt
import torch.utils.data as data_utils
from quick_ai.forecast.dataset_characteristics import StatisticalParametersExtractor
from quick_ai.algorithms.neural_network import NeuralNetworkModel
import pandas as pd
from quick_ai.preprocessing import sota_preprocessor
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split


class Best_Model(nn.Module):
    def __init__(self, num_features: int, num_classes: int):
        super(Best_Model, self).__init__()
        self.fc1 = nn.Linear(num_features, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x


def main():
    frame = pd.read_csv('results.csv')
    PARAMETERS = ["name", "task", "task_detailed", "target_features", "target_nans", "num_columns", "num_rows", "number_of_highly_correlated_features", "highest_correlation",
                  "number_of_lowly_correlated_features", "lowest_correlation", "highest_eigenvalue", "lowest_eigenvalue", "share_of_numerical_features", "num_classes", "biggest_class_freq", "smallest_class_freq"]

    Models = ["NeuralNetworkModel", "XGBoostClassifier", "AdaBoostClassifier", "BaggingClassifier", "BernoulliNB", "CalibratedClassifierCV", "CategoricalNB", "ComplementNB", "DecisionTreeClassifier", "DummyClassifier", "ExtraTreeClassifier", "ExtraTreesClassifier", "GaussianNB", "GaussianProcessClassifier", "GradientBoostingClassifier", "HistGradientBoostingClassifier", "KNeighborsClassifier",
              "LabelPropagation", "LabelSpreading", "LinearDiscriminantAnalysis", "LinearSVC", "LogisticRegression", "LogisticRegressionCV", "MLPClassifier", "MultinomialNB", "NearestCentroid", "NuSVC", "PassiveAggressiveClassifier", "Perceptron", "QuadraticDiscriminantAnalysis", "RadiusNeighborsClassifier", "RandomForestClassifier", "RidgeClassifier", "RidgeClassifierCV", "SGDClassifier", "SVC"]
    frame.drop(columns=['name', 'task'], axis=1, inplace=True)
    target = frame[Models]
    frame.drop(Models, axis=1, inplace=True)
    preprocessor = sota_preprocessor()
    pre_frame = preprocessor.fit_transform(frame)

    # dataset = pd.concat([pre_frame, target], axis=1)
    # print(dataset)

    mps_device = torch.device("cuda")

    values = []
    model = Best_Model(len(pre_frame.columns),
                       len(target.columns)).to(mps_device)
    value = 25000
    for epoch in range(value):
        optimizer = optim.Adam(model.parameters(), lr=0.0001)
        criterion = nn.MSELoss()
        x_train, x_test, y_train, y_test = train_test_split(
            pre_frame, target, test_size=0.2)
        train = data_utils.TensorDataset(torch.tensor(x_train.values.astype(
            'float32')).to(mps_device), torch.tensor(y_train.values.astype
                                                     ('float32')).to(mps_device))
        test = data_utils.TensorDataset(torch.tensor(x_test.values.astype(
            'float32')).to(mps_device), torch.tensor(y_test.values.astype
                                                     ('float32')).to(mps_device))
        train_loader = DataLoader(train, batch_size=32)
        test_loader = DataLoader(test, batch_size=32)
        for x, y in train_loader:
            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            for x, y in test_loader:
                output = model(x)
                loss = criterion(output, y)
                if epoch % 100 == 0:
                    print(f'Epoch: {epoch}, Loss: {loss}')
                values.append(float(loss))
    torch.save(model.state_dict(), 'model.pth')
    return model
# plt.plot(values)
# plt.show()
# with open('model.pkl', 'wb') as file:
#     pickle.dump(model, file)
