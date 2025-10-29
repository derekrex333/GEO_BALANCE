def calcular_ehi_completo(tfi, bi, vsi):
    """
    Calcula el Índice de Salud Ecológica (EHI) completo
    EHI = (TFI × 0.5) + (BI × 0.3) + (VSI × 0.2)
    """
    # Asegurarse de que tenemos valores válidos
    valor_tfi = tfi.get('valor', 0) if isinstance(tfi, dict) else (tfi if tfi else 0)
    valor_bi = bi.get('valor', 0) if isinstance(bi, dict) else (bi if bi else 0)
    valor_vsi = vsi.get('valor', 0) if isinstance(vsi, dict) else (vsi if vsi else 0)
    
    # Calcular contribuciones
    contribucion_tfi = valor_tfi * 0.5
    contribucion_bi = valor_bi * 0.3
    contribucion_vsi = valor_vsi * 0.2
    
    # Calcular EHI total
    ehi_valor = contribucion_tfi + contribucion_bi + contribucion_vsi
    
    # Categorizar
    categoria, color, interpretacion = categorizar_ehi(ehi_valor)
    
    return {
        'valor': ehi_valor,
        'categoria': categoria,
        'color': color,
        'interpretacion': interpretacion,
        'componentes': {
            'TFI': {
                'valor': valor_tfi,
                'contribucion': contribucion_tfi,
                'categoria': tfi.get('categoria', 'N/A') if isinstance(tfi, dict) else 'N/A'
            },
            'BI': {
                'valor': valor_bi,
                'contribucion': contribucion_bi,
                'categoria': bi.get('categoria', 'N/A') if isinstance(bi, dict) else 'N/A'
            },
            'VSI': {
                'valor': valor_vsi,
                'contribucion': contribucion_vsi,
                'categoria': vsi.get('categoria', 'N/A') if isinstance(vsi, dict) else 'N/A'
            }
        }
    }

def categorizar_ehi(valor):
    """Categoriza el valor EHI"""
    if valor > 0.76:
        return "Excelente", "#3B9A6F", "El ecosistema se encuentra en excelente estado de salud"
    elif valor > 0.51:
        return "Bueno", "#36A2EB", "El ecosistema presenta buena salud con algunos aspectos a mejorar"
    elif valor > 0.26:
        return "Regular", "#FFC107", "El ecosistema requiere atención y posibles intervenciones"
    elif valor > 0.11:
        return "Pobre", "#DC3545", "El ecosistema está en estado pobre, requiere intervención urgente"
    else:
        return "Crítico", "#0F1D1F", "El ecosistema está en estado crítico, necesita restauración inmediata"