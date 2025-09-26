from app.api.const_c import const_celdas


def map_node_to_name(node_id: str) -> str:
    # Reutiliza el mapping del proyecto existente si aplica
    return const_celdas.get(node_id, node_id)


