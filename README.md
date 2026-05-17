# ToxShield — AI-Powered Cyberbullying & Toxic Comment Detection System

A production-grade full-stack AI/ML web application that detects toxic, abusive, hateful, threatening, and bullying comments using Machine Learning and NLP. Built as a final-year AI/ML project with real-time analysis, confidence scores, 6 toxicity categories, analytics dashboard, and smart comment rephrasing.

---

##  Features

| Feature | Description |
|---------|-------------|
|  Real-time analysis | NLP pipeline processes comments in <200ms |
|  6 toxic categories | Toxic, Severe Toxic, Insult, Threat, Obscene, Hate Speech |
|  Confidence scores | Per-category probability bars with visual severity meter |
|  Smart rephrasing | AI suggests polite alternative for toxic input |
|  Analytics dashboard | Pie charts, bar graphs, 7-day trend, sentiment analysis |
|  Persistent history | All analyses saved to MongoDB |
|  Dark/Light mode | System-aware with toggle |
|  Voice input | Web Speech API for hands-free input |

---

##  Folder Structure

```
cyberbullying-detector/
├── README.md
├── backend/
│   ├── app.py                  ← Flask entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   │   └── db.py               ← MongoDB connection & schema
│   ├── routes/
│   │   ├── predict.py          ← POST /predict
│   │   ├── history.py          ← GET  /history
│   │   ├── analytics.py        ← GET  /analytics
│   │   └── rewrite.py          ← POST /rewrite-comment
│   └── utils/
│       ├── preprocessor.py     ← Text cleaning pipeline
│       └── model_loader.py     ← ML model inference
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── index.css
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── ToxicityMeter.jsx
│       │   ├── CategoryBadges.jsx
│       │   ├── HistoryCard.jsx
│       │   └── LoadingAnimation.jsx
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Analyzer.jsx
│       │   ├── Dashboard.jsx
│       │   └── About.jsx
│       ├── hooks/
│       │   └── useTheme.js
│       └── utils/
│           └── api.js
└── ml/
    ├── scripts/
    │   ├── preprocess.py       ← Dataset preprocessing
    │   ├── train_model.py      ← Model training
    │   └── evaluate_model.py   ← Evaluation metrics
    ├── data/                   ← Place train.csv here
    └── saved_models/           ← Auto-generated .pkl files
```

---

##  Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB running locally (or Atlas URI)

---

### 1️ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (auto-happens on first run, or run manually)
python -c "import nltk; [nltk.download(p) for p in ['stopwords','punkt','wordnet','omw-1.4']]"

# Configure environment
cp .env.example .env
# Edit .env → set MONGO_URI if using Atlas

# Start server
python app.py
```
Backend: http://localhost:5000

> **Note:** Without a trained ML model, the backend uses a keyword-based heuristic fallback automatically. It still fully demonstrates the API structure. Train the model for production accuracy.

---

### 2️ Frontend Setup

```bash
cd frontend

npm install

cp .env.example .env
# Verify VITE_API_BASE_URL=http://localhost:5000

npm run dev
```
 Frontend: http://localhost:5173

---

### 3️ Train the ML Model (Optional but Recommended)

```bash
# Download dataset from Kaggle:
# https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
# Place train.csv in:  ml/data/train.csv

cd ml/scripts

# Step 1: Preprocess
python preprocess.py

# Step 2: Train (takes ~5–15 min depending on hardware)
python train_model.py

# Step 3: Evaluate
python evaluate_model.py
```

Trained models saved to `ml/saved_models/` as `.pkl` files. The backend auto-loads them on next restart.

---

##  API Reference

### `POST /predict`
Analyze a comment for toxicity.



##  MongoDB Schema

```javascript
// Collection: comments
{
  _id:            ObjectId,
  text:           String,       // Original input
  toxicity_score: Number,       // 0.0 – 1.0
  is_toxic:       Boolean,
  severity:       String,       // safe | mild | moderate | high | severe
  sentiment:      String,       // positive | negative | neutral
  categories: {
    toxic:        Number,
    severe_toxic: Number,
    insult:       Number,
    threat:       Number,
    obscene:      Number,
    hate_speech:  Number,
  },
  confidence:     Number,       // 0 – 100
  rewritten:      String,       // Polite rewrite if requested
  model_used:     String,       // ml_model | heuristic_fallback
  created_at:     Date,
}
```

---

##  Environment Variables

### `backend/.env`
```
MONGO_URI=mongodb://localhost:27017/toxicdb
FLASK_ENV=development
SECRET_KEY=change-this-in-production
MODEL_PATH=../ml/saved_models/
PORT=5000
```

### `frontend/.env`
```
VITE_API_BASE_URL=http://localhost:5000
```

---

##  ML Model Details

| Property | Value |
|----------|-------|
| Algorithm | Logistic Regression (One-vs-Rest per category) |
| Dataset | Jigsaw Toxic Comment Classification (~160K samples) |
| Vectorizer | TF-IDF (50K features, 1-2 grams, sublinear TF) |
| Class balancing | `class_weight='balanced'` |
| Typical AUC-ROC | 0.96–0.98 (toxic), 0.93–0.96 (other categories) |
| Model size | ~15–30 MB per category (.pkl) |
| Inference time | <50ms per comment |

---

##  Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Run `pip install -r requirements.txt` in venv |
| NLTK data missing | Run `python -c "import nltk; nltk.download('all')"` |
| MongoDB connection error | Check `MONGO_URI` in `.env`; ensure MongoDB is running |
| CORS error in browser | Check `VITE_API_BASE_URL` matches backend port |
| Model not found | System uses heuristic fallback — run `train_model.py` for full accuracy |
| Voice input not working | Only works in Chrome/Edge; requires HTTPS in production |

---

## 📦 Full Dependency List

### Python (backend + ML)
```
flask, flask-cors, pymongo, python-dotenv,
scikit-learn, nltk, pandas, numpy, joblib, gunicorn
```

### Node.js (frontend)
```
react, react-dom, react-router-dom,
axios, recharts, lucide-react,
vite, tailwindcss, autoprefixer, postcss
```
