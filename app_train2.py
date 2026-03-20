from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import joblib
import pickle
X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
model = LinearRegression()
model.fit(X, y)

#모델 저장

joblib.dump(model, 'linear_model.pkl')
print('모델 저장 완료')



with open('linear_model2.pkl', 'wb') as f:
    pickle.dump(model, f)


print('save ok')
