# 🌌 NightRunners Search Engine  

-> A new way to visualize search

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/nandhra702/NightRunners__Search_Engine)  

NightRunners is a **full-text search engine** built from scratch with a Django backend, advanced IR (Information Retrieval) techniques, and an ** interesting 3D visualization layer** for exploring search results like never before.  

Designed for both research and fun — blending traditional IR concepts with modern interactive features.  

---

##  Features  

###  Indexing  
- **Lemmatization** for normalizing words  
- **Postings list** creation for efficient retrieval
- **Document vector list** created for ease of scoring
- **Dimensionality reduction** to convert to 3D vectors

### 📑 Query Processing  
- **TF–IDF scoring**  
- **Cosine similarity** ranking  
- **SMART lnc.ltc scheme** implemented:  
  - **Documents**: log tf, cosine normalization, *no idf*  
  - **Queries**: log tf, idf, cosine normalization  

Formula used:  
\[
tfidf = (1 + \log_{10}(tf)) \times \log_{10}(N/df)
\]

###  Ranking & Results  
- Cosine similarity used for ranking documents against queries  
- Free-text queries supported (no operators required)  
- Results rendered with proper ranking and scoring  

###  Output  
- Full demo video included (see below )  

---

##  Novelty  

Unlike a typical search engine clone, NightRunners adds some **next-level features**:  

- 🌀 **Intriguing 3D visualization** of search results  
- 📂 **Direct file opening** from search results  
- ➕ **Support for adding documents** dynamically to the corpus  
- 🌐 **Django backend hosted** for scalability and easy integration  

---

##  Tech Stack  

- **Python** (core IR engine + preprocessing)  
- **Django** (backend + routing)  
- **BabylonJS / 3D rendering** (for result visualization)  
- **HTML/CSS/JS** (frontend integration)  

---

## How It Works  

1. **Indexing**:  
   - Documents in the corpus are processed  
   - Lemmatization + postings lists are created  

2. **Query Processing**:  
   - Free-text query entered  
   - TF–IDF computed using `lnc.ltc` scheme  
   - Cosine similarity with each document  

3. **Ranking & Output**:  
   - Results ranked by similarity score  
   - 3D visualization displays documents
