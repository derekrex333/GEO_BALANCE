def calcular_vsi(datos_vsi):
    """
    Calcula el Índice de Vulnerabilidad del Suelo (VSI)
    VSI = (Cobertura × 0.6) + (Calidad del Suelo × 0.4)
    """
    if not datos_vsi:
        return {
            'valor': 0,
            'categoria': 'Sin datos',
            'contribucion': 0,
            'detalles': {}
        }
    
    try:
        cobertura = datos_vsi.get('coverage_pct', 0) / 100.0  # Convertir a decimal
        calidad_suelo = datos_vsi.get('soil_quality_pct', 0) / 100.0  # Convertir a decimal
        
        # Calcular VSI
        vsi_valor = (cobertura * 0.6) + (calidad_suelo * 0.4)
        
        # Categorizar
        if vsi_valor > 0.8:
            categoria = "Excelente"
        elif vsi_valor > 0.6:
            categoria = "Bueno"
        elif vsi_valor > 0.4:
            categoria = "Regular"
        elif vsi_valor > 0.2:
            categoria = "Pobre"
        else:
            categoria = "Crítico"
        
        return {
            'valor': vsi_valor,
            'categoria': categoria,
            'contribucion': vsi_valor * 0.2,  # Peso en EHI: 20%
            'detalles': {
                'coverage_pct': cobertura * 100,
                'soil_quality_pct': calidad_suelo * 100,
                'coverage_weighted': cobertura * 0.6,
                'soil_quality_weighted': calidad_suelo * 0.4
            }
        }
    
    except Exception as e:
        print(f"Error calculando VSI: {e}")
        return {
            'valor': 0,
            'categoria': 'Error',
            'contribucion': 0,
            'detalles': {}
        }