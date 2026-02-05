"""
CineAI Pro - Film Türü Tahmin API
FastAPI Backend Servisi
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import re
import os
from deep_translator import GoogleTranslator

# FastAPI uygulaması oluştur
app = FastAPI(
    title="CineAI Pro API",
    description="Film türü tahmin servisi - Türkçe açıklamadan tür tahmini yapar",
    version="1.0.0"
)

# CORS ayarları - Frontend'den gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik URL belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model ve Vectorizer yolları
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "final_best_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "final_vectorizer.pkl")

# Model ve Vectorizer'ı yükle
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ Model ve Vectorizer başarıyla yüklendi!")
except Exception as e:
    print(f"❌ Model yükleme hatası: {e}")
    model = None
    vectorizer = None

# Tekil tür bilgileri - Emoji ve açıklamalar (küçük harf key)
GENRE_INFO_SINGLE = {
    "action": {"emoji": "💥", "description": "Adrenalin dolu aksiyon ve heyecan", "tr": "Aksiyon"},
    "comedy": {"emoji": "😂", "description": "Kahkaha dolu eğlenceli anlar", "tr": "Komedi"},
    "drama": {"emoji": "🎭", "description": "Derin duygusal hikayeler", "tr": "Drama"},
    "horror": {"emoji": "👻", "description": "Korku ve gerilim dolu anlar", "tr": "Korku"},
    "romance": {"emoji": "💕", "description": "Aşk ve romantizm hikayeleri", "tr": "Romantik"},
    "sci-fi": {"emoji": "🚀", "description": "Bilim kurgu ve gelecek vizyonu", "tr": "Bilim Kurgu"},
    "scifi": {"emoji": "🚀", "description": "Bilim kurgu ve gelecek vizyonu", "tr": "Bilim Kurgu"},
    "thriller": {"emoji": "🔪", "description": "Gerilim ve gizem dolu", "tr": "Gerilim"},
    "adventure": {"emoji": "🗺️", "description": "Macera ve keşif dolu", "tr": "Macera"},
    "animation": {"emoji": "🎨", "description": "Animasyon dünyasının büyüsü", "tr": "Animasyon"},
    "crime": {"emoji": "🔍", "description": "Suç ve dedektiflik hikayeleri", "tr": "Suç"},
    "documentary": {"emoji": "📹", "description": "Gerçek hayattan hikayeler", "tr": "Belgesel"},
    "fantasy": {"emoji": "🧙", "description": "Fantastik dünyalar ve büyü", "tr": "Fantazi"},
    "mystery": {"emoji": "🕵️", "description": "Gizem ve sırlarla dolu", "tr": "Gizem"},
    "war": {"emoji": "⚔️", "description": "Savaş ve kahramanlık hikayeleri", "tr": "Savaş"},
    "western": {"emoji": "🤠", "description": "Vahşi Batı maceraları", "tr": "Western"},
    "musical": {"emoji": "🎵", "description": "Müzik ve dans şöleni", "tr": "Müzikal"},
    "family": {"emoji": "👨‍👩‍👧‍👦", "description": "Aile dostu içerikler", "tr": "Aile"},
    "history": {"emoji": "📜", "description": "Tarihi olaylar ve dönemler", "tr": "Tarih"},
    "sport": {"emoji": "⚽", "description": "Spor ve rekabet hikayeleri", "tr": "Spor"},
    "sports": {"emoji": "⚽", "description": "Spor ve rekabet hikayeleri", "tr": "Spor"},
    "biography": {"emoji": "📖", "description": "Gerçek hayat hikayeleri", "tr": "Biyografi"},
    "bio": {"emoji": "📖", "description": "Gerçek hayat hikayeleri", "tr": "Biyografi"},
    "romantic": {"emoji": "💕", "description": "Aşk ve romantizm hikayeleri", "tr": "Romantik"},
    "love": {"emoji": "💕", "description": "Aşk ve romantizm hikayeleri", "tr": "Romantik"},
    "suspense": {"emoji": "🔪", "description": "Gerilim ve gizem dolu", "tr": "Gerilim"},
    "noir": {"emoji": "🌑", "description": "Karanlık ve gizemli hikayeler", "tr": "Kara Film"},
    "adult": {"emoji": "🔞", "description": "Yetişkin içerikler", "tr": "Yetişkin"},
    "short": {"emoji": "🎬", "description": "Kısa filmler", "tr": "Kısa Film"},
    "news": {"emoji": "📰", "description": "Haber ve güncel olaylar", "tr": "Haber"},
    "reality": {"emoji": "📺", "description": "Gerçeklik programları", "tr": "Gerçeklik"},
    "tv": {"emoji": "📺", "description": "TV programları", "tr": "TV"},
    "talk": {"emoji": "🎤", "description": "Talk show programları", "tr": "Talk Show"},
    "game": {"emoji": "🎮", "description": "Oyun programları", "tr": "Oyun"},
    "show": {"emoji": "🎭", "description": "Gösteri programları", "tr": "Gösteri"},
}


def get_genre_info(genre_key: str) -> dict:
    """
    Verilen tür anahtarını (tek veya kombine) işler ve Türkçe bilgileri döndürür.
    Örn: "comedy_family" -> {"emoji": "😂👨‍👩‍👧‍👦", "description": "...", "tr": "Komedi & Aile"}
    """
    genre_key_lower = genre_key.lower().strip()
    
    # "_" ile ayrılmış kombine türleri kontrol et
    if "_" in genre_key_lower:
        parts = genre_key_lower.split("_")
        emojis = []
        tr_names = []
        descriptions = []
        
        for part in parts:
            part = part.strip()
            if part in GENRE_INFO_SINGLE:
                info = GENRE_INFO_SINGLE[part]
                emojis.append(info["emoji"])
                tr_names.append(info["tr"])
                descriptions.append(info["description"])
            else:
                # Bilinmeyen tür - ilk harfi büyük yap
                emojis.append("🎬")
                tr_names.append(part.capitalize())
                descriptions.append("Film türü")
        
        return {
            "emoji": "".join(emojis[:2]),  # İlk 2 emoji
            "tr": " & ".join(tr_names),
            "description": " ve ".join(descriptions[:2])
        }
    else:
        # Tekil tür
        if genre_key_lower in GENRE_INFO_SINGLE:
            return GENRE_INFO_SINGLE[genre_key_lower]
        else:
            return {
                "emoji": "🎬",
                "tr": genre_key.capitalize(),
                "description": "Film türü"
            }

# Request ve Response modelleri
class PredictRequest(BaseModel):
    text: str

class ProbabilityItem(BaseModel):
    genre: str
    genre_tr: str
    emoji: str
    probability: float

class PredictResponse(BaseModel):
    success: bool
    predicted_genre: str
    predicted_genre_tr: str
    emoji: str
    description: str
    confidence: float
    top_5_probabilities: list[ProbabilityItem]
    translated_text: str
    original_text: str


def clean_text(text: str) -> str:
    """Metni temizle - lowercase ve noktalama işaretlerini kaldır"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def translate_to_english(text: str) -> str:
    """Türkçe metni İngilizceye çevir"""
    try:
        translator = GoogleTranslator(source='tr', target='en')
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Çeviri hatası: {e}")
        # Çeviri başarısız olursa orijinal metni döndür
        return text


@app.get("/")
async def root():
    """Ana sayfa - API durumu"""
    return {
        "message": "🎬 CineAI Pro API'ye Hoş Geldiniz!",
        "status": "active",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    }


@app.post("/predict", response_model=PredictResponse)
async def predict_genre(request: PredictRequest):
    """
    Film türü tahmini yap
    
    1. Türkçe metni İngilizceye çevir
    2. Metni temizle
    3. Vektörleştir
    4. Model ile tahmin yap
    5. Sonuçları döndür
    """
    
    # Model kontrolü
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=500, 
            detail="Model veya Vectorizer yüklenemedi. Lütfen dosyaların varlığını kontrol edin."
        )
    
    # Boş metin kontrolü
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Lütfen en az 10 karakterlik bir film açıklaması girin."
        )
    
    try:
        original_text = request.text.strip()
        
        # 1. Türkçe metni İngilizceye çevir
        translated_text = translate_to_english(original_text)
        
        # 2. Metni temizle
        cleaned_text = clean_text(translated_text)
        
        # 3. Vektörleştir
        text_vectorized = vectorizer.transform([cleaned_text])
        
        # 4. Tahmin yap
        prediction = model.predict(text_vectorized)[0]
        
        # 5. Olasılıkları al (eğer model destekliyorsa)
        probabilities = {}
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(text_vectorized)[0]
            classes = model.classes_
            probabilities = {cls: float(prob) for cls, prob in zip(classes, proba)}
        elif hasattr(model, 'decision_function'):
            # SVM gibi modeller için decision function kullan
            decision = model.decision_function(text_vectorized)[0]
            classes = model.classes_
            # Softmax uygula
            exp_decision = np.exp(decision - np.max(decision))
            proba = exp_decision / exp_decision.sum()
            probabilities = {cls: float(prob) for cls, prob in zip(classes, proba)}
        
        # İlk 5 olasılığı al
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
        
        top_5 = []
        for genre, prob in sorted_probs:
            genre_data = get_genre_info(genre)
            top_5.append(ProbabilityItem(
                genre=genre,
                genre_tr=genre_data["tr"],
                emoji=genre_data["emoji"],
                probability=round(prob * 100, 2)
            ))
        
        # Tahmin edilen türün bilgileri
        predicted_info = get_genre_info(prediction)
        confidence = probabilities.get(prediction, 0) * 100
        
        return PredictResponse(
            success=True,
            predicted_genre=prediction,
            predicted_genre_tr=predicted_info["tr"],
            emoji=predicted_info["emoji"],
            description=predicted_info["description"],
            confidence=round(confidence, 2),
            top_5_probabilities=top_5,
            translated_text=translated_text,
            original_text=original_text
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Tahmin sırasında bir hata oluştu: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
