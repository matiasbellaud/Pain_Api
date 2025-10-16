from services.llama_service import query_llama

def test_query_llama():
    result = query_llama("Bonjour, peux-tu me résumer ce qu'est une IA ?")
    assert isinstance(result, str)
    assert len(result) > 0
