from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from preprocess_data import eeg_filtered
from preprocess_data import eeg_data


# Supondo que eeg_filtered e gsr_data estejam no formato correto para treinamento
X = np.array(eeg_filtered).T  # Ajuste conforme a estrutura dos dados
y = [data[1] for data in eeg_data]  # Etiquetas de categorias visuais

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinar modelo
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Avaliar modelo
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Acurácia:", accuracy)
