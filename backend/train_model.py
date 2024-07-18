import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Carregar dados pré-processados
eeg_data = np.genfromtxt('eeg_data_processed.csv', delimiter=',', dtype=str, encoding='utf-8')
gsr_data = np.genfromtxt('gsr_data_processed.csv', delimiter=',', dtype=str, encoding='utf-8')

# Extrair recursos e rótulos (categorias de programas de TV)
X_eeg = np.array([list(map(float, row[3:])) for row in eeg_data])  # Dados de EEG
y_eeg = np.array([row[2] for row in eeg_data])                    # Programas de TV correspondentes

X_gsr = np.array([list(map(float, row[3:])) for row in gsr_data])  # Dados de GSR
y_gsr = np.array([row[2] for row in gsr_data])                    # Programas de TV correspondentes

# Dividir dados em treino e teste
X_train_eeg, X_test_eeg, y_train_eeg, y_test_eeg = train_test_split(X_eeg, y_eeg, test_size=0.3, random_state=42)
X_train_gsr, X_test_gsr, y_train_gsr, y_test_gsr = train_test_split(X_gsr, y_gsr, test_size=0.3, random_state=42)

# Treinar modelo para dados de EEG
clf_eeg = RandomForestClassifier(n_estimators=100)
clf_eeg.fit(X_train_eeg, y_train_eeg)

# Treinar modelo para dados de GSR
clf_gsr = RandomForestClassifier(n_estimators=100)
clf_gsr.fit(X_train_gsr, y_train_gsr)

# Avaliar modelo para dados de EEG
y_pred_eeg = clf_eeg.predict(X_test_eeg)
accuracy_eeg = accuracy_score(y_test_eeg, y_pred_eeg)
print("Acurácia EEG:", accuracy_eeg)

# Avaliar modelo para dados de GSR
y_pred_gsr = clf_gsr.predict(X_test_gsr)
accuracy_gsr = accuracy_score(y_test_gsr, y_pred_gsr)
print("Acurácia GSR:", accuracy_gsr)
