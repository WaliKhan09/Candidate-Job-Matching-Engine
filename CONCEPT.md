# 🧠 CONCEPT.md: How I built the Matching Engine

Welcome to the documentation for my technical assignment! Below, I explain the concepts I used to build this "Semantic Matcher" in plain English.

---

## 1. What is "Semantic Matching"?

Normally, if you search for "Java Developer," a computer only looks for those exact words. If a resume says "Experienced Programmer in Java," the computer might miss it.

**My Solution**: I use "Embeddings." I translate every description into a "mathematical meaning." Because the meaning of "Programmer" is close to "Developer," my system connects them automatically.

---

## 2. The "Brain": Embedding Models

I used a library called `SentenceTransformers`. Think of it as a translator that turns English into "Math-ish." 

- **The Model**: I chose `all-MiniLM-L6-v2`. 
- **Why**: It's small and fast enough to run on my own laptop without needing expensive servers, but it's still very smart.

---

## 3. The "Flash": FAISS Search

Even if our "Math-ish" translation is good, we need to find the best match quickly.

- In my code, I use **FAISS**. It's a tool that's really good at comparing thousands of lists of numbers at once.
- When you add a candidate, I "save" their math-position. 
- When you search for a job, FAISS finds the nearest "skill positions" in the blink of an eye.

---

## 4. Keeping Data Safe (Persistence)

I noticed that every time I restarted my computer, the FAISS search would "forget" all the candidates. 

**My Fix**: 
1. I save the basic info (Name, Experience) in a **SQLite database**.
2. I *also* save the AI numbers (the embedding) in that same database.
3. Every time the app starts, my code reads the database and "reminds" FAISS about all the candidates. This makes the system professional and reliable.

---

## 5. The Ranking Rule

Following the project requirements:
1. **Rule #1**: Match by skill first (the AI score).
2. **Rule #2**: If the skills are a tie, the candidate with **higher experience** is always better. 

I implemented this using a simple "sort" in Python that checks the Score first, then the Experience.

---

## 6. Closing Thoughts
I tried to follow clean, modern practices (using **FastAPI** for speed and **Pydantic** for error-free data) while making the code as easy to read as a story. Hope you like it!
