import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import csv

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

def clean_text_english(text):
    if pd.isna(text) or text == "": return ""
    text = str(text)[:2500]
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    cleaned = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(cleaned)

# --- STRATEJİ: TÜRLERİ GRUPLA ---
def group_genres(genre):
    g = str(genre).strip()
    # 1. Grup: Aksiyon ve Macera çok benzer
    if g in ['Action', 'Adventure', 'War']:
        return 'Action_Adventure'
    # 2. Grup: Bilim Kurgu, Fantastik ve Animasyon (Genelde hayal ürünü)
    elif g in ['Sci-Fi', 'Fantasy', 'Animation']:
        return 'SciFi_Fantasy'
    # 3. Grup: Dram, Biyografi ve Tarih
    elif g in ['Drama', 'Biography', 'History', 'Romance']:
        return 'Drama_Romance'
    # 4. Grup: Suç ve Gizem
    elif g in ['Crime', 'Mystery', 'Thriller', 'Horror']: # Korkuyu da buraya veya ayrı alabilirsin
        return 'Crime_Thriller_Horror'
    # 5. Grup: Komedi ve Aile
    elif g in ['Comedy', 'Family', 'Musical']:
        return 'Comedy_Family'
    else:
        return 'Other'

def process_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))
    
    imdb_path = os.path.join(data_dir, 'Top_10000_Movies_IMDb.csv')
    poe_path = os.path.join(data_dir, 'poe_verisi.csv')
    out_orig_path = os.path.join(data_dir, 'processed_original.csv')
    out_aug_path = os.path.join(data_dir, 'processed_augmented.csv')

    print(f"📂 Çalışma Dizini: {data_dir}")
    print("\n⏳ ADIM 1: Veriler Hazırlanıyor ve GRUPLANIYOR...")

    # --- 1. ORİJİNAL VERİ ---
    if not os.path.exists(imdb_path):
        print(f"❌ HATA: {imdb_path} bulunamadı!")
        return

    df_imdb = pd.read_csv(imdb_path, on_bad_lines='skip')
    df_orig = df_imdb[['Plot', 'Genre']].rename(columns={'Plot': 'plot', 'Genre': 'all_genres'})
    df_orig.dropna(inplace=True)
    
    # İLK TÜRÜ AL
    df_orig['raw_genre'] = df_orig['all_genres'].apply(lambda x: str(x).split(',')[0].strip())
    
    # GRUPLAMA YAP (Magic Touch)
    df_orig['genre'] = df_orig['raw_genre'].apply(group_genres)
    
    # 'Other' olanları at (Çok nadir türler)
    df_orig = df_orig[df_orig['genre'] != 'Other']
    
    # Temizlik
    df_orig['clean_text'] = df_orig['plot'].apply(clean_text_english)
    df_orig = df_orig[df_orig['clean_text'].str.len() > 2]
    
    # Orijinali kaydet
    df_orig.to_csv(out_orig_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"✅ Orijinal Veri (Gruplanmış) Hazır: {len(df_orig)} satır.")

    # --- 2. POE VERİSİ ---
    print("\n⏳ ADIM 2: Poe Verisi Ekleniyor...")
    df_combined = df_orig.copy()

    if os.path.exists(poe_path):
        df_poe = pd.read_csv(poe_path, on_bad_lines='skip')
        df_poe.columns = [c.strip().lower() for c in df_poe.columns]
        
        rename_map = {}
        for col in df_poe.columns:
            if col in ['ozet', 'text', 'plot']: rename_map[col] = 'plot'
            if col in ['tur', 'label', 'genre']: rename_map[col] = 'all_genres'
        
        df_poe.rename(columns=rename_map, inplace=True)
        
        if 'plot' in df_poe.columns and 'all_genres' in df_poe.columns:
            # Poe verisi için de aynı gruplamayı yap
            df_poe['raw_genre'] = df_poe['all_genres'].apply(lambda x: str(x).split(',')[0].strip())
            df_poe['genre'] = df_poe['raw_genre'].apply(group_genres)
            df_poe = df_poe[df_poe['genre'] != 'Other']
            
            # Birleştir
            cols = ['plot', 'all_genres', 'genre'] # Gerekli sütunlar
            df_combined = pd.concat([df_orig[cols], df_poe[cols]], ignore_index=True)
            
            # Temizle
            df_combined['clean_text'] = df_combined['plot'].apply(clean_text_english)
            df_combined = df_combined[df_combined['clean_text'].str.len() > 2]
            
            print(f"✅ Poe verisi eklendi. Toplam: {len(df_combined)} satır.")
        else:
            print("❌ Poe sütunları uyuşmadı.")
    else:
        print("⚠️ Poe dosyası yok.")

    # KAYDET
    df_combined.to_csv(out_aug_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"✅ Birleştirilmiş Veri (Gruplanmış) Hazır: {out_aug_path}")

if __name__ == "__main__":
    process_data()