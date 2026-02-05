import joblib
import pandas as pd
import os

def compare_and_select():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.abspath(os.path.join(current_dir, '..', 'models'))
    
    pkg_orig_path = os.path.join(models_dir, 'pkg_original.pkl')
    pkg_aug_path = os.path.join(models_dir, 'pkg_augmented.pkl')
    final_model_path = os.path.join(models_dir, 'final_best_model.pkl')
    final_vec_path = os.path.join(models_dir, 'final_vectorizer.pkl')
    report_path = os.path.join(models_dir, 'final_report.csv')

    print("\n⚖️ KARŞILAŞTIRMA VE FİNAL SEÇİMİ")
    
    try:
        pkg_orig = joblib.load(pkg_orig_path)
        pkg_aug = joblib.load(pkg_aug_path)
    except FileNotFoundError:
        print("❌ Eğitim dosyaları eksik! Lütfen 2 ve 3 numaralı dosyaları çalıştırın.")
        return

    res_orig = pkg_orig['results']
    res_aug = pkg_aug['results']
    
    comparison_data = []
    best_score_overall = 0
    winner_package = None
    winner_name = ""

    # Ortak modelleri ve Voting modelini birleştir
    all_models = set(res_orig.keys()).union(set(res_aug.keys()))

    for model_name in all_models:
        # Veri çekme (Eğer model o pakette yoksa 0 ata)
        # Orijinalde Flexible Acc olmadığı için Accuracy'yi baz alıyoruz
        m_orig = res_orig.get(model_name, {"Accuracy": 0}) 
        m_aug = res_aug.get(model_name, {"Accuracy": 0, "Flexible Accuracy": 0})
        
        row = {
            "Algoritma": model_name,
            "Std Acc (Önce)": m_orig.get('Accuracy', 0),
            "Std Acc (Sonra)": m_aug.get('Accuracy', 0),
            "Esnek Acc (Sonra)": m_aug.get('Flexible Accuracy', m_aug.get('Accuracy', 0)), 
        }
        comparison_data.append(row)
        
        # Şampiyonu "Esnek Accuracy" değerine göre seç (Augmented paketinden)
        score = m_aug.get('Flexible Accuracy', 0)
        if score > best_score_overall:
            best_score_overall = score
            winner_package = pkg_aug
            winner_name = f"{model_name} (Augmented)"

    df_report = pd.DataFrame(comparison_data)
    
    # CSV Kaydet (Ham haliyle)
    df_report.to_csv(report_path, index=False)
    
    # --- EKRANA BASMAK İÇİN FORMATLAMA ---
    print("\n📊 KARŞILAŞTIRMA RAPORU:")
    
    # Sadece gösterim için bir kopya alıp formatlayalım
    df_display = df_report.copy()
    
    # Sayısal sütunları yüzdeye çevir
    cols_to_format = ["Std Acc (Önce)", "Std Acc (Sonra)", "Esnek Acc (Sonra)"]
    for col in cols_to_format:
        df_display[col] = df_display[col].apply(lambda x: f"%{x*100:.2f}")
        
    # Tabloyu bas
    print(df_display.to_string(index=False))
    
    print("-" * 50)
    print(f"🏆 ŞAMPİYON MODEL: {winner_name}")
    print(f"🌟 BAŞARI SKORU (Esnek): %{best_score_overall*100:.2f}")
    
    if winner_package:
        joblib.dump(winner_package['best_model'], final_model_path)
        joblib.dump(winner_package['vectorizer'], final_vec_path)
        print("\n✅ Final model 'final_best_model.pkl' olarak kaydedildi.")
        print("✅ GUI kullanımı için hazırsınız!")
    else:
        print("❌ Hata: Şampiyon seçilemedi.")

if __name__ == "__main__":
    compare_and_select()