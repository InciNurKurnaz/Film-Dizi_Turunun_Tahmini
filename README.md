# 🎬 CineAI Pro: Yapay Zeka Destekli Senaryo Analiz Sistemi

**CineAI Pro**, kullanıcı tarafından girilen film senaryolarını (Türkçe veya İngilizce) analiz ederek, filmin türünü (Aksiyon, Dram, Bilim Kurgu vb.) yapay zeka ve doğal dil işleme (NLP) yöntemleriyle tahmin eden uçtan uca (end-to-end) bir web uygulamasıdır.

Bu proje, klasik makine öğrenmesi algoritmalarını modern web teknolojileriyle birleştirerek **%78.27** başarı oranına sahip bir tahmin sistemi sunar.

---

## 🚀 Özellikler

* **🧠 Hibrit Yapay Zeka Modeli:** SVM, Naive Bayes ve Random Forest algoritmalarının güçlerini birleştiren **Voting Classifier (Ensemble Learning)** mimarisi.
* **🤖 Generative AI Destekli Veri:** Poe AI (LLM) kullanılarak üretilen sentetik verilerle (Data Augmentation) zenginleştirilmiş eğitim seti.
* **📊 Esnek Doğruluk (Flexible Accuracy):** Çoklu etiketli (multi-label) film türleri için geliştirilmiş, kullanıcı deneyimine odaklı özel başarı metriği.
* **🌍 Çoklu Dil Desteği:** Girilen Türkçe senaryoları otomatik olarak İngilizceye çevirip analiz eden entegre çeviri katmanı.
* **🎨 Cyberpunk & Netflix UI:** Next.js ve Tailwind CSS ile geliştirilmiş, animasyonlu, karanlık mod (dark mode) arayüz.
* **📈 Görsel Analiz:** Tahmin sonuçlarını ve olasılık dağılımlarını gösteren interaktif grafikler (Recharts).

---

## 🛠️ Teknolojiler

### Backend (Yapay Zeka & API)
* **Python 3.10+**
* **FastAPI:** REST API servisi için.
* **Scikit-Learn:** Model eğitimi ve TF-IDF vektörleştirme.
* **Pandas & NumPy:** Veri manipülasyonu.
* **NLTK:** Metin ön işleme (Preprocessing).
* **Deep-Translator:** Dil çevirisi.

### Frontend (Arayüz)
* **Next.js 14 (App Router):** React framework.
* **TypeScript:** Tip güvenliği için.
* **Tailwind CSS:** Stil ve tasarım.
* **Framer Motion:** Animasyonlar.
* **Lucide React:** İkon seti.
* **Recharts:** Veri görselleştirme.

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

### 1. Projeyi Klonlayın
Öncelikle terminalinizi açın ve projeyi bilgisayarınıza indirin:

```bash
git clone [https://github.com/kullaniciadin/cineai-pro.git](https://github.com/kullaniciadin/cineai-pro.git)
cd cineai-pro
```

### 2. Backend Kurulumu (Python)

```bash
cd backend

# Gerekli kütüphaneleri yükleyin
pip install fastapi uvicorn joblib scikit-learn pandas deep-translator

# API sunucusunu başlatın
uvicorn main:app --reload
```

### 3. Frontend Kurulumu (Next.js)
Yeni bir terminal açın ve proje ana dizinine dönün.

```bash
cd frontend

# Paketleri yükleyin
npm install

# Uygulamayı başlatın
npm run dev
```

---

## 📊 Model Performansı
Proje geliştirme sürecinde, ham veri ile %47 seviyesinde olan başarı oranı, uygulanan ileri tekniklerle %78.27 seviyesine çıkarılmıştır.

```bash
Model,Accuracy (Esnek),ROC-AUC
Naive Bayes,%76.33,0.870
Random Forest,%75.00,0.865
Voting Ensemble,%78.27,0.887
```



