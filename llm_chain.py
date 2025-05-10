from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from retriever import get_retriever

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

retriever = get_retriever()

def generate_answer(query: str):
    query_lower = query.lower()

    # Determine focus keyword
    focus = None
    if any(k in query_lower for k in ["ipad", "macbook", "iphone", "watch", "airpods", "homepod"]):
        for product in ["ipad", "macbook", "iphone", "watch", "airpods", "homepod"]:
            if product in query_lower:
                focus = product
                break

    # Retrieve documents
    docs = retriever.invoke(query)

    # High-specificity product spec query
    is_high_specificity = "spec" in query_lower and focus and len(query.split()) > 4
    if is_high_specificity:
        docs = [doc for doc in docs if query_lower in doc.page_content.lower()]
    elif focus:
        docs = [doc for doc in docs if focus in doc.page_content.lower()]

    if not docs:
        return {
            "result": "Not enough relevant data found in the documents.",
            "context": ""
        }

    def format_chunk(doc):
        return doc.page_content.strip()

    context = "\n\n---\n\n".join(format_chunk(doc) for doc in docs)

    # 3-Type Prompt Routing
    if any(k in query_lower for k in [
        "types of apple products", "product categories", "apple products list",
        "name all apple products", "different apple products", "list apple devices",
        "all apple products"
    ]):
        # Type 1: General Apple product categories
        prompt_instruction = """
You are a helpful assistant. Your task is to list all Apple product categories and models mentioned in the documents.

Instructions:
- Group the answer by product type: iPhone, iPad, MacBook, Apple Watch, AirPods, HomePod, etc.
- Use this format:
[Product Category]:
- [Model name 1]: [1-line description]
- [Model name 2]: [1-line description]
- Avoid detailed technical specs or overlapping content.
- Remove any duplicates or repeated product names.
"""
    elif any(k in query_lower for k in [
        "types of ipad", "ipad models", "iphone models", "types of iphone",
        "watch models", "types of apple watch"
    ]):
        # Type 2: Product-line specific model list
        prompt_instruction = f"""
You are a helpful assistant. List all {focus.title()} models or variants mentioned in the documents.

Instructions:
- Only include models under the category {focus.title()}.
- Use bullet points with model names and 1-line descriptions.
- Do not include specs or unrelated product categories.
- Avoid repetition and be clear.
"""
    elif "spec" in query_lower:
        # Type 3: Specific model spec query
        if is_high_specificity:
            prompt_instruction = f"""
You are a helpful assistant. Extract specifications for the product mentioned in the query: "{query}".

Instructions:
- Only show the specs for the exact model.
- Use clean bullet points.
- Do not list any other models.
- Say "Not mentioned in the documents" if nothing is found.
"""
        else:
            prompt_instruction = f"""
You are a helpful assistant. List specs of all relevant {focus if focus else 'Apple'} products found in the documents.

Instructions:
- Group specs by model name.
- Use bullet points under each model.
- Do not mix in products from other categories.
"""
    else:
        # Fallback
        prompt_instruction = """
You are a helpful assistant. Use the provided documents to answer the query clearly and accurately.

Instructions:
- Keep the answer concise.
- Structure your response if multiple items are involved.
- Do not include unrelated or unsupported information.
"""

    # Full prompt
    prompt = f"""
You are a helpful assistant that answers questions using only the following documents.

DOCUMENTS:
{context}

QUESTION:
{query}

INSTRUCTIONS:
{prompt_instruction}

STRUCTURED ANSWER:
"""
    output = generator(prompt, max_new_tokens=600, do_sample=True, temperature=0.7)[0]["generated_text"]
    generated = output.replace(prompt, "").strip()

    # Deduplication
    lines = generated.splitlines()
    seen = set()
    final_lines = []
    for line in lines:
        clean = line.strip()
        if clean and clean not in seen:
            seen.add(clean)
            final_lines.append(clean)

    return {
        "result": "\n".join(final_lines),
        "context": context
    }
