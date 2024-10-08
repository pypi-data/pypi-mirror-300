from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression

##########################################################################################################

class LogisticRegressionThreshold(BaseEstimator, ClassifierMixin):
    
    def __init__(self, threshold=0.5, **kwargs):
        self.threshold = threshold
        self.lr = LogisticRegression(**kwargs)
    
    def fit(self, X, y, sample_weight=None):
        # Fit the underlying logistic regression model, passing sample_weight if provided
        self.lr.fit(X, y, sample_weight=sample_weight)
        # Expose the classes_ attribute from the fitted LogisticRegression model
        self.classes_ = self.lr.classes_
        return self
    
    def predict(self, X):
        # Predict the class using the custom threshold
        class_one_proba = self.lr.predict_proba(X)[:, 1]
        pred = (class_one_proba >= self.threshold).astype(int)
        return pred
    
    def predict_proba(self, X):
        # Return the probabilities as given by the logistic regression
        pred_proba =  self.lr.predict_proba(X)
        return pred_proba
    
    def set_params(self, **params):
        # Allow setting parameters, including the threshold and LogisticRegression parameters
        if 'threshold' in params:
            self.threshold = params['threshold'] # Assigning the value of 'threshold' to the self.threshold  parameter
            params.pop('threshold') # Removing 'threshold' from the params dictionary
        self.lr.set_params(**params) # At this point params must not contain 'threshold'
        return self

    def get_params(self, deep=True):
        # Get parameters, including threshold
        return {'threshold': self.threshold, **self.lr.get_params(deep)}
