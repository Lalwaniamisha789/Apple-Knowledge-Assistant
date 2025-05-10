def run_agent(query: str) -> dict:
    from tools import simple_calculator, simple_define, compare_specs
    from llm_chain import generate_answer

    query_lower = query.lower()
    response = {"route": "", "result": "", "context": ""}

    if any(op in query_lower for op in ["calculate", "*", "/", "+", "-"]):
        response["route"] = "calculator"
        math_expr = query_lower.replace("calculate", "").strip()
        response["result"] = simple_calculator(math_expr)

    elif "define" in query_lower:
        response["route"] = "dictionary"
        term = query_lower.replace("define", "").strip()
        response["result"] = simple_define(term)

    elif any(k in query_lower for k in ["compare", "difference", "vs"]):
        response["route"] = "compare"
        response["result"] = compare_specs(query_lower)

    else:
        response["route"] = "rag"
        rag_response = generate_answer(query_lower)
        response.update(rag_response)

    return response
