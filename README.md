# 🤖 Semantic Candidate–Job Matching Engine

Hi! This is my 24-hour technical assignment project. I've built a system that matches candidates to jobs using **AI embeddings**. This means the computer understands the "meaning" of a job description, not just the keywords!

---

## 🏗 Project Structure
I've organized the code into small, easy-to-read folders:
```text
.
├── main.py             # The engine's ignition! Start here.
├── app/
│   ├── api/            # Where our API links (URLs) are defined.
│   ├── services/       # The "Brain" - where AI and matching happens.
│   ├── db/             # Database setup (SQLite).
│   ├── models/         # What our data looks like in the database.
│   ├── schemas/        # Rules for what users can send us.
│   └── config.py       # General settings.
├── requirements.txt    # Fast-install for all tools I used.
└── scripts/
    └── verify_matcher.py # My automated test script.
```

---

## 🚀 How to Run (Setup)

1. **Install everything**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python3 main.py
   ```
   *Note: If you are on a Mac/Linux, you might need to run `export PYTHONPATH=$PYTHONPATH:$(pwd)` first.*

---

## 📐 How it Works (Simply)

### 1. The AI part
I use a model called `all-MiniLM-L6-v2`. It turns a sentence like *"I am a nurse"* into a long list of numbers. In geometry, similar sentences end up very close to each other.

### 2. The Search part
I use **FAISS** (made by Facebook). It's a special search tool that can look through millions of those number-lists in a fraction of a second to find the best match.

### 3. The tie-breaker
If two people have the exact same skill score, I wrote a small rule: **The candidate with more years of experience is ranked higher.**

---

## 🧪 Testing it out!
I wrote a script to register 9 candidates and 5 jobs automatically to show you it works:
```bash
python3 scripts/verify_matcher.py
```
It tests different scenarios like medical, tech, and kitchen jobs!
