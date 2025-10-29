def calcular_tfi(datos_troficos):
    """
    Calcula el Índice de Fragmentación del Territorio (TFI)
    TFI = (Conectividad Observada / Conectividad Esperada) × (Longitud Observada / Longitud Esperada)
    """
    if not datos_troficos:
        return {
            'valor': 0,
            'categoria': 'Sin datos',
            'contribucion': 0,
            'detalles': {}
        }
    
    try:
        conn_obs = datos_troficos.get('connectance_observed', 0)
        conn_exp = datos_troficos.get('connectance_expected', 1)  # Evitar división por cero
        len_obs = datos_troficos.get('length_observed', 0)
        len_exp = datos_troficos.get('length_expected', 1)  # Evitar división por cero
        
        # Calcular TFI
        ratio_conn = conn_obs / conn_exp if conn_exp > 0 else 0
        ratio_len = len_obs / len_exp if len_exp > 0 else 0
        tfi_valor = ratio_conn * ratio_len
        
        # Categorizar
        if tfi_valor > 0.8:
            categoria = "Excelente"
        elif tfi_valor > 0.6:
            categoria = "Bueno"
        elif tfi_valor > 0.4:
            categoria = "Regular"
        elif tfi_valor > 0.2:
            categoria = "Pobre"
        else:
            categoria = "Crítico"
        
        return {
            'valor': tfi_valor,
            'categoria': categoria,
            'contribucion': tfi_valor * 0.5,  # Peso en EHI: 50%
            'detalles': {
                'connectance_observed': conn_obs,
                'connectance_expected': conn_exp,
                'length_observed': len_obs,
                'length_expected': len_exp,
                'ratio_connectance': ratio_conn,
                'ratio_length': ratio_len
            }
        }
    
    except Exception as e:
        print(f"Error calculando TFI: {e}")
        return {
            'valor': 0,
            'categoria': 'Error',
            'contribucion': 0,
            'detalles': {}
        }