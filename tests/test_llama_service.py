from services.llama_service import query_llama
from services.resource_monitor import get_system_stats

def test_query_llama():
    """Test de la fonction query_llama avec monitoring des ressources."""
    answer, metrics = query_llama("Bonjour, peux-tu me résumer ce qu'est une IA ?")

    # Vérifier la réponse
    assert isinstance(answer, str)
    assert len(answer) > 0

    # Vérifier les métriques
    assert isinstance(metrics, dict)
    assert "elapsed_time_seconds" in metrics
    assert "cpu_percent" in metrics
    assert "memory_used_mb" in metrics
    assert "estimated_energy_wh" in metrics

    # Vérifier que les valeurs sont positives
    assert metrics["elapsed_time_seconds"] > 0
    assert metrics["estimated_energy_joules"] >= 0

def test_system_stats():
    """Test de la fonction get_system_stats."""
    stats = get_system_stats()

    assert isinstance(stats, dict)
    assert "cpu_percent" in stats
    assert "cpu_count" in stats
    assert "memory_percent" in stats
    assert "memory_total_mb" in stats

    # Vérifier que les valeurs sont cohérentes
    assert stats["cpu_count"] > 0
    assert 0 <= stats["memory_percent"] <= 100
