import pandas as pd
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.calibration import CalibratedClassifierCV

print('Loading data...')

train_df = pd.read_csv("training_data.csv")
val_df = pd.read_csv("validation_data.csv")

# Extract queries and labels from the dataframes
train_queries = train_df['query']
train_labels = train_df['label']

val_queries = val_df['query']
val_labels = val_df['label']

print('Removing data duplicates in training...')
unique_train_queries = set()
unique_train_data = []
for query, label in zip(train_queries, train_labels):
    if query not in unique_train_queries:
        unique_train_queries.add(query)
        unique_train_data.append((query, label))
train_queries = [query for query, _ in unique_train_data]
train_labels = [label for _, label in unique_train_data]

print('Removing data duplicates in validation...')
unique_val_queries = set()
unique_val_data = []
for query, label in zip(val_queries, val_labels):
    if query not in unique_val_queries:
        unique_val_queries.add(query)
        unique_val_data.append((query, label))
val_queries = [query for query, _ in unique_val_data]
val_labels = [label for _, label in unique_val_data]

unique_train_queries = set(train_queries)
unique_val_queries = set(val_queries)

# Find common queries between training and validation data
common_queries = unique_train_queries.intersection(unique_val_queries)
print('Checking for data contamination...')
if len(common_queries) > 0:
    print("Warning: Training data leaked into validation data!")
    print("Common Queries:")
    for query in common_queries:
        print(query)
    
    val_queries_cleaned = [query for query in val_queries if query not in common_queries]
    val_labels_cleaned = [label for query, label in zip(val_queries, val_labels) if query not in common_queries]
    
    val_queries = val_queries_cleaned
    val_labels = val_labels_cleaned
    
    print("Validation data has been cleaned.")
else:
    print("No training data leaked into validation data.")

vectorizer = TfidfVectorizer()

# Transform the training and validation data
train_vectors = vectorizer.fit_transform(train_queries)
val_vectors = vectorizer.transform(val_queries)

# Initialize the Naive Bayes classifier
nb_classifier = MultinomialNB(alpha=0.1)

# Fit the classifier on the training data
nb_classifier.fit(train_vectors, train_labels)

# Calibrate the classifier to get better probability estimates
calibrated_classifier = CalibratedClassifierCV(nb_classifier, method='sigmoid')
calibrated_classifier.fit(train_vectors, train_labels)

# Predict on the validation data and get calibrated probabilities
val_predictions = calibrated_classifier.predict(val_vectors)
val_probabilities = calibrated_classifier.predict_proba(val_vectors)

accuracy = accuracy_score(val_labels, val_predictions)
print(f"Validation Accuracy: {accuracy:.2%}")

model_filename = 'naive_bayes_model.pkl'
joblib.dump(nb_classifier, model_filename)
vectorizer_filename = 'tfidf_vectorizer.pkl'
joblib.dump(vectorizer, vectorizer_filename)

print('Done! Trained models saved.')
