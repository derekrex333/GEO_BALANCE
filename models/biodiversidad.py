import math

def calcular_shannon_wiener(datos_biodiversidad):
    """
    Calcula el Índice de Biodiversidad de Shannon-Wiener
    H' = -Σ(pᵢ × ln(pᵢ)) donde pᵢ = nᵢ/N
    """
    if datos_biodiversidad.empty:
        return {
            'valor': 0,
            'categoria': 'Sin datos',
            'contribucion': 0,
            'detalles': {}
        }
    
    try:
        # Calcular abundancia total
        abundancia_total = datos_biodiversidad['abundance'].sum()
        
        if abundancia_total == 0:
            return {
                'valor': 0,
                'categoria': 'Sin especies',
                'contribucion': 0,
                'detalles': {'num_especies': 0, 'abundancia_total': 0, 'shannon_index': 0}
            }
        
        # Calcular índice de Shannon-Wiener
        shannon_index = 0
        for _, fila in datos_biodiversidad.iterrows():
            proporcion = fila['abundance'] / abundancia_total
            if proporcion > 0:
                shannon_index -= proporcion * math.log(proporcion)
        
        # Normalizar (el máximo teórico es ln(número de especies))
        num_especies = len(datos_biodiversidad)
        max_posible = math.log(num_especies) if num_especies > 0 else 0
        bi_valor = shannon_index / max_posible if max_posible > 0 else 0
        
        # Categorizar
        if bi_valor > 0.8:
            categoria = "Excelente"
        elif bi_valor > 0.6:
            categoria = "Bueno"
        elif bi_valor > 0.4:
            categoria = "Regular"
        elif bi_valor > 0.2:
            categoria = "Pobre"
        else:
            categoria = "Crítico"
        
        return {
            'valor': bi_valor,
            'categoria': categoria,
            'contribucion': bi_valor * 0.3,  # Peso en EHI: 30%
            'detalles': {
                'num_especies': num_especies,
                'abundancia_total': abundancia_total,
                'shannon_index': shannon_index,
                'max_posible': max_posible
            }
        }
    
    except Exception as e:
        print(f"Error calculando BI: {e}")
        return {
            'valor': 0,
            'categoria': 'Error',
            'contribucion': 0,
            'detalles': {}
        }