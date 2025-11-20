# Data CoP AI 

## Updates

Run the streamlit application with `streamlit run hr_assistant/Home.py`

*Note: windows users may need to supply the full path.*

## Welcome

AI use has grown rapidly over the last few years. Far from being a sci-fi replacement for humans, where it really shines is in automating the boring, repetitive, or slow parts of our day. Most of the value isn’t in building huge, complicated systems, but in streamlining simple ones.

This event is about exploring practical, lightweight uses of AI. What can we build in a few hours that’s actually useful? By the end of the day we should have a better sense of how these tools behave, where they’re strong, where they fall over, and how to use them with minimal effort.

We’re keeping it deliberately simple with one core task and an optional extra:

* A HR chatbot that can answer questions using policy text.

* A recommender that matches staff to roles based on skills.

These are small problems where AI solutions can shine and provide immediate value.

Today is a chance to see how this works in practice and start spotting similar opportunities in our own teams and projects.

## Timetable

*10:00 AM* - Welcome and Introduction

*10:15 AM* - Planning

*10:30 AM* - Build 1

*12:30 PM* - Lunch

*13:30 PM* - Recap & Planning

*13:45 PM* - Build 2

*15:45 PM* - Finishing Touches

*16:00 PM* - Demo & Discuss

*17:00 PM* - It's Over

## Tooling

#### Gemini API
A large language model that handles natural-language tasks. In our case this is answering HR questions and generating recommendations.

#### ChromaDB
A lightweight vector database that stores text as embeddings. ChromaDB finds the most relevant chunks of text based on our questions which we can then include in our prompts. This allows us to avoid uploading documents to Gemini directly.

#### Embeddings
Instead of storing raw text, we convert each chunk into a vector using Google’s embedding model. Distance between vectors tells us how semantically similar two pieces of text are. This is what allows Gemini to answer from the correct policy section.

#### Python
The suggested language to link the component parts together is python. It's popular, simple, and robust.

#### Retrieval-Augmented Generation (RAG)
The 'proper' name for the simple pattern we’re using:

* Retrieve relevant text from ChromaDB.

* Feed it into the Gemini model to answer the question.

## API keys

These will be provided on the day along with a demo of how to obtain them.

## Getting started

#### 1 - Clone the starter pack from [Github](https://github.com/jrh-dev/data_cop_ai_event).

```bash
# https
git clone https://github.com/jrh-dev/data_cop_ai_event.git

# ssh
git clone git@github.com:jrh-dev/data_cop_ai_event.git
```

#### 2 - Create an environment.

***Linux (incl. WSL)***
```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set Gemini API key
export GEMINI_API_KEY=<API KEY>

# 4. Run the demo
cd hr_assistant
python demo.py
```

***Windows (powershell)***
```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2 Install dependencies
pip install -r requirements.txt

# 3. Set Gemini API key
env$GEMINI_API_KEY="<API_KEY>"

# 4. Run the demo
cd hr_assistant
python demo.py
```

## FAQs & gotchas
#### Common issues:

* `Collection already exists` - delete ~/.chromadb/ or `python cleanup_chroma.py`

* Empty responses - increase `n_results` (try 3–5)

* Hallucinations - tighten prompt wording

* API errors - check api key is present in environment

* Slow retrieval - reduce `chunk_size`