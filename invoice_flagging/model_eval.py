from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import RandomizedSearchCV 
from sklearn.metrics import accuracy_score, classification_report, make_scorer, f1_score

def train_random_forest(x_train, y_train):
    rf = RandomForestClassifier(
                                random_state=42,
                                n_jobs=-1
                                    )

    param_dist = {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [None, 10, 20, 30, 40],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"]
        }

    scorer = make_scorer(f1_score)

    random_search = RandomizedSearchCV(
        estimator=rf,
        param_distributions=param_dist,
        n_iter=20,         
        scoring=scorer,
        cv=5,
        random_state=42,
        verbose=2,
        n_jobs=-1
        )

    random_search.fit(x_train, y_train) 
    return random_search

def eval_classifier(model, x_test, y_test, model_name): 
    preds = model.predict(x_test)

    accuracy = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)
    
    print(f"\n{model_name} Performance:")
    print(f"Accuracy : {accuracy:.2f}")
    print(report)
    
    