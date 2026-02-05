import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score, 
                             roc_auc_score, confusion_matrix, classification_report, roc_curve, auc)
from sklearn.preprocessing import LabelBinarizer

def plot_confusion_matrix(y_true, y_pred, classes, model_name, save_dir):
    """Confusion Matrix çizer ve kaydeder."""
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('Gerçek Tür')
    plt.xlabel('Tahmin Edilen Tür')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'cm_{model_name.replace(" ", "_")}.png'))
    plt.close()

def plot_roc_curve(y_true, y_proba, classes, model_name, save_dir):
    """ROC-AUC Eğrisini çizer ve kaydeder."""
    lb = LabelBinarizer()
    lb.fit(classes)
    y_true_bin = lb.transform(y_true)
    
    n_classes = len(classes)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    plt.figure(figsize=(10, 8))
    for i in range(n_classes):
        if y_true_bin.shape[1] == y_proba.shape[1]: 
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_proba[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
            plt.plot(fpr[i], tpr[i], label=f'{classes[i]} (area = {roc_auc[i]:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(save_dir, f'roc_{model_name.replace(" ", "_")}.png'))
    plt.close()

def calculate_metrics(y_true, y_pred, y_proba, classes):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    try:
        lb = LabelBinarizer()
        lb.fit(classes)
        y_true_bin = lb.transform(y_true)
        if y_true_bin.shape[1] == y_proba.shape[1]:
            roc = roc_auc_score(y_true_bin, y_proba, multi_class='ovr', average='weighted')
        else: roc = 0.0
    except: roc = 0.0
    
    return {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1, "ROC-AUC": roc}

def train_original():
    # --- YOL AYARLAMASI ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))
    models_dir = os.path.abspath(os.path.join(current_dir, '..', 'models'))
    plots_dir = os.path.join(models_dir, 'plots_original')
    
    if not os.path.exists(models_dir): os.makedirs(models_dir)
    if not os.path.exists(plots_dir): os.makedirs(plots_dir)

    csv_path = os.path.join(data_dir, 'processed_original.csv')
    save_path = os.path.join(models_dir, 'pkg_original.pkl')

    print("\n🚀 EGITIM 1: Orijinal Veri Seti (Full Analiz)")
    
    if not os.path.exists(csv_path):
        print(f"❌ HATA: Dosya bulunamadı -> {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # 1. YETERSİZ VERİ TEMİZLİĞİ (En az 50 örnek)
    min_count = 50
    v_counts = df['genre'].value_counts()
    valid_genres = v_counts[v_counts >= min_count].index.tolist()
    print(f"ℹ️ Yetersiz verisi olan türler çıkarılıyor (<{min_count}): {[g for g in df['genre'].unique() if g not in valid_genres]}")
    df = df[df['genre'].isin(valid_genres)]
    
    X = df['clean_text'].fillna("")
    y = df['genre']
    classes = y.unique()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 2. GÜÇLÜ VEKTÖRLEŞTİRME
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)
    
    # 3. DENGESİZLİK AYARLI MODELLER
    models = {
        "Naive Bayes": MultinomialNB(alpha=0.01), 
        "SVM": CalibratedClassifierCV(LinearSVC(class_weight='balanced', dual=False)),
        "Random Forest": RandomForestClassifier(n_estimators=200, class_weight='balanced', n_jobs=-1, random_state=42)
    }
    
    results = {}
    best_f1 = 0
    best_model_obj = None
    
    for name, model in models.items():
        print(f"\n⚙️  {name} EĞİTİLİYOR VE ANALİZ EDİLİYOR...")
        
        # Cross-Validation Skoru (Gerçek başarı)
        cv_scores = cross_val_score(model, X_train_vec, y_train, cv=5, scoring='f1_weighted')
        val_f1 = cv_scores.mean()

        # Tam Eğitim
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        y_proba = model.predict_proba(X_test_vec)
        
        # Metrikler
        metrics = calculate_metrics(y_test, y_pred, y_proba, classes)
        metrics["Validation F1"] = val_f1
        results[name] = metrics
        
        print(f"📊 {name} Sonuçları:")
        print(f"   Accuracy:      %{metrics['Accuracy']*100:.2f}")
        print(f"   Test F1-Score: {metrics['F1']:.4f}")
        print(f"   Val F1-Score:  {val_f1:.4f} (CV)")
        print(f"   ROC-AUC:       {metrics['ROC-AUC']:.4f}")
        print("-" * 50)
        
        # --- EKSİK OLAN KISIMLAR GERİ EKLENDİ ---
        print("📝 Sınıflandırma Raporu:")
        print(classification_report(y_test, y_pred, zero_division=0)) 
        
        plot_confusion_matrix(y_test, y_pred, classes, name, plots_dir)
        plot_roc_curve(y_test, y_proba, classes, name, plots_dir)
        print(f"🖼️  Grafikler kaydedildi: {plots_dir}")

        if metrics['F1'] > best_f1:
            best_f1 = metrics['F1']
            best_model_obj = model

    data_to_save = {
        "results": results,
        "best_model": best_model_obj,
        "vectorizer": tfidf
    }
    joblib.dump(data_to_save, save_path)
    print(f"\n✅ Eğitim tamamlandı. Paket: {save_path}")

if __name__ == "__main__":
    train_original()