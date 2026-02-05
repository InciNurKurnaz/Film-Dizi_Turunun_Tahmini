"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import {
  Sparkles,
  Film,
  ChevronDown,
  ChevronUp,
  Loader2,
  Send,
  Zap,
  Code2,
  TrendingUp,
} from "lucide-react";

// API Response Tipi
interface ProbabilityItem {
  genre: string;
  genre_tr: string;
  emoji: string;
  probability: number;
}

interface PredictResponse {
  success: boolean;
  predicted_genre: string;
  predicted_genre_tr: string;
  emoji: string;
  description: string;
  confidence: number;
  top_5_probabilities: ProbabilityItem[];
  translated_text: string;
  original_text: string;
}

// Grafik renkleri
const CHART_COLORS = [
  "#FF4B2B",
  "#FF6B4A",
  "#FF8B6A",
  "#FFAB8A",
  "#FFCBAA",
];

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showDebug, setShowDebug] = useState(false);

  const handleAnalyze = async () => {
    if (!inputText.trim() || inputText.length < 10) {
      setError("Lütfen en az 10 karakterlik bir film açıklaması girin.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post<PredictResponse>(
        "http://localhost:8000/predict",
        { text: inputText },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setResult(response.data);
    } catch (err: any) {
      console.error("API Error:", err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError(
          "Sunucuya bağlanılamadı. Backend servisinin çalıştığından emin olun."
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleAnalyze();
    }
  };

  // Grafik verisi hazırla
  const chartData = result?.top_5_probabilities.map((item) => ({
    name: `${item.emoji} ${item.genre_tr}`,
    value: item.probability,
    genre: item.genre_tr,
  }));

  return (
    <main className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="flex flex-col md:flex-row items-center justify-between mb-8 md:mb-12"
      >
        <div className="flex items-center gap-3 mb-4 md:mb-0">
          <div className="relative">
            <Film className="w-10 h-10 text-cine-red" />
            <Sparkles className="w-4 h-4 text-cine-pink absolute -top-1 -right-1" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold">
            <span className="gradient-text">CineAI</span>
            <span className="text-white ml-2">Pro</span>
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="glass px-4 py-2 rounded-full flex items-center gap-2"
          >
            <TrendingUp className="w-4 h-4 text-green-400" />
            <span className="text-sm text-gray-300">Model Doğruluğu:</span>
            <span className="text-green-400 font-bold">%78.2</span>
          </motion.div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
        {/* Input Section - Sol Taraf */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="glass-strong rounded-2xl p-6 md:p-8 h-full">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cine-red to-cine-pink flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Film Açıklaması</h2>
                <p className="text-sm text-gray-400">
                  Filmin konusunu Türkçe olarak yazın
                </p>
              </div>
            </div>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Örnek: Uzak bir galakside, genç bir çiftçi kendini galaksiler arası bir savaşın ortasında bulur. Gizemli bir prensesi kurtarmak için efsanevi bir şövalyenin yolculuğuna çıkar..."
              className="textarea-cine w-full h-48 md:h-64 p-4 rounded-xl text-white placeholder-gray-500 resize-none text-base"
            />

            <div className="flex items-center justify-between mt-4">
              <span className="text-xs text-gray-500">
                {inputText.length} karakter • Ctrl+Enter ile gönder
              </span>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleAnalyze}
                disabled={isLoading || inputText.length < 10}
                className={`btn-primary px-6 py-3 rounded-xl font-semibold text-white flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed ${
                  isLoading ? "pulse-glow" : ""
                }`}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analiz Ediliyor...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Analiz Et 🚀
                  </>
                )}
              </motion.button>
            </div>

            {/* Error Message */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400"
                >
                  ⚠️ {error}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Result Section - Sağ Taraf */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <div className="glass-strong rounded-2xl p-6 md:p-8 h-full min-h-[500px]">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cine-pink to-cine-red flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Tahmin Sonucu</h2>
                <p className="text-sm text-gray-400">
                  AI destekli tür analizi
                </p>
              </div>
            </div>

            <AnimatePresence mode="wait">
              {!result && !isLoading && (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center h-80 text-center"
                >
                  <Film className="w-20 h-20 text-gray-700 mb-4" />
                  <p className="text-gray-500 text-lg">
                    Film açıklaması girin ve
                  </p>
                  <p className="text-gray-600">
                    <span className="gradient-text font-semibold">
                      Analiz Et
                    </span>{" "}
                    butonuna basın
                  </p>
                </motion.div>
              )}

              {isLoading && (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center h-80"
                >
                  <div className="relative">
                    <div className="w-24 h-24 rounded-full border-4 border-cine-card border-t-cine-red animate-spin" />
                    <Sparkles className="w-8 h-8 text-cine-red absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                  </div>
                  <p className="text-gray-400 mt-6 animate-pulse">
                    AI modeli analiz yapıyor...
                  </p>
                </motion.div>
              )}

              {result && (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ type: "spring", duration: 0.6 }}
                >
                  {/* Ana Sonuç Kartı */}
                  <div className="text-center mb-6">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{
                        type: "spring",
                        stiffness: 200,
                        delay: 0.2,
                      }}
                      className="text-8xl mb-4 emoji-bounce inline-block"
                    >
                      {result.emoji}
                    </motion.div>

                    <motion.h3
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                      className="text-3xl md:text-4xl font-bold gradient-text mb-2"
                    >
                      {result.predicted_genre_tr}
                    </motion.h3>

                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.4 }}
                      className="text-gray-400 text-lg mb-4"
                    >
                      {result.description}
                    </motion.p>

                    <motion.div
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.5 }}
                      className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass"
                    >
                      <span className="text-gray-400">Güven Skoru:</span>
                      <span
                        className={`font-bold ${
                          result.confidence > 70
                            ? "text-green-400"
                            : result.confidence > 40
                            ? "text-yellow-400"
                            : "text-red-400"
                        }`}
                      >
                        %{result.confidence.toFixed(1)}
                      </span>
                    </motion.div>
                  </div>

                  {/* Grafik */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="mt-8 p-4 rounded-xl bg-cine-darker/50 border border-cine-border/30"
                  >
                    <h4 className="text-base font-semibold text-gray-300 mb-6 flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-cine-red" />
                      Olasılık Dağılımı
                    </h4>

                    <div className="h-72">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={chartData}
                          layout="vertical"
                          margin={{ left: 20, right: 30, top: 10, bottom: 10 }}
                          barSize={28}
                        >
                          <XAxis
                            type="number"
                            domain={[0, 100]}
                            tickFormatter={(v) => `%${v}`}
                            tick={{ fill: "#9ca3af", fontSize: 13 }}
                            axisLine={{ stroke: "#30363d" }}
                            tickLine={{ stroke: "#30363d" }}
                          />
                          <YAxis
                            type="category"
                            dataKey="name"
                            width={140}
                            tick={{ fill: "#e5e7eb", fontSize: 14, fontWeight: 500 }}
                            axisLine={{ stroke: "#30363d" }}
                            tickLine={false}
                          />
                          <Tooltip
                            contentStyle={{
                              background: "rgba(22, 27, 34, 0.98)",
                              border: "1px solid #FF4B2B",
                              borderRadius: "12px",
                              padding: "14px 18px",
                              boxShadow: "0 4px 20px rgba(255, 75, 43, 0.2)",
                            }}
                            labelStyle={{ color: "#fff", fontWeight: "bold", fontSize: 14 }}
                            formatter={(value: number) => [
                              `%${value.toFixed(1)}`,
                              "Olasılık",
                            ]}
                            cursor={{ fill: "rgba(255, 75, 43, 0.1)" }}
                          />
                          <Bar dataKey="value" radius={[0, 8, 8, 0]} animationDuration={800}>
                            {chartData?.map((entry, index) => (
                              <Cell
                                key={`cell-${index}`}
                                fill={CHART_COLORS[index % CHART_COLORS.length]}
                                style={{ filter: index === 0 ? "drop-shadow(0 0 8px rgba(255, 75, 43, 0.5))" : "none" }}
                              />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </motion.div>

                  {/* Debug Section - Accordion */}
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                    className="mt-6"
                  >
                    <button
                      onClick={() => setShowDebug(!showDebug)}
                      className="w-full flex items-center justify-between p-4 rounded-xl glass hover:bg-cine-card/50 transition-colors"
                    >
                      <span className="text-gray-400 flex items-center gap-2">
                        <Code2 className="w-4 h-4" />
                        Sistemin Arka Planı
                      </span>
                      {showDebug ? (
                        <ChevronUp className="w-5 h-5 text-gray-500" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-gray-500" />
                      )}
                    </button>

                    <AnimatePresence>
                      {showDebug && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3 }}
                          className="overflow-hidden"
                        >
                          <div className="p-4 mt-2 rounded-xl bg-cine-darker/50 border border-cine-border/30 text-sm">
                            <div className="mb-3">
                              <span className="text-gray-500">
                                Orijinal Metin:
                              </span>
                              <p className="text-gray-300 mt-1">
                                {result.original_text}
                              </p>
                            </div>
                            <div className="mb-3">
                              <span className="text-gray-500">
                                Çevrilen Metin (EN):
                              </span>
                              <p className="text-blue-400 mt-1">
                                {result.translated_text}
                              </p>
                            </div>
                            <div>
                              <span className="text-gray-500">
                                Tahmin Edilen Sınıf:
                              </span>
                              <p className="text-cine-red mt-1 font-mono">
                                {result.predicted_genre}
                              </p>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="text-center mt-12 text-gray-600 text-sm"
      >
        <p>
          Yapay Zeka ile güçlendirilmiştir 🤖 •{" "}
          <span className="gradient-text">CineAI Pro</span> © 2026
        </p>
      </motion.footer>
    </main>
  );
}
