from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from datetime import datetime
from models.ehi import calcular_ehi_completo, categorizar_ehi
from models.biodiversidad import calcular_shannon_wiener
from models.tfi import calcular_tfi
from models.vsi import calcular_vsi

app = Flask(__name__)

# Configuración
app.config['DATA_FOLDER'] = 'data'
app.config['EXCEL_FILE'] = 'EcoBalance_Datos.xlsx'
app.config['SECRET_KEY'] = 'eco-balance-2025'

'''Funciones auxiliares para cargar y guardar datos Excel ayuda por gemini.ia'''
def cargar_datos_excel():
    """Carga todos los DataFrames desde el archivo Excel y devuelve un diccionario."""
    try:
        excel_path = os.path.join(app.config['DATA_FOLDER'], app.config['EXCEL_FILE'])
        
        datos = {
            'sites': pd.read_excel(excel_path, sheet_name='1-sites'),
            'biodiversity': pd.read_excel(excel_path, sheet_name='2-biodiversity_data'),
            'trophic': pd.read_excel(excel_path, sheet_name='3-trophic_data'),
            'vsi': pd.read_excel(excel_path, sheet_name='4-vsi_data'),
            'results': pd.read_excel(excel_path, sheet_name='5-results_ehi')
        }

        for key in datos:
            if 'site_id' in datos[key].columns:
                datos[key]['site_id'] = datos[key]['site_id'].astype(str)
        return datos
    
    except FileNotFoundError:
        print(f"\n❌ ERROR: Archivo Excel no encontrado en la ruta esperada: {excel_path}")
        return None
        
    except Exception as e:
        print(f"\n❌ ERROR inesperado al cargar el Excel: {e}")
        return None

def transformar_datos(datos):
    """Transforma los datos del Excel a la estructura que espera el código"""
    if datos is None:
        return None
    
    # Renombrar columnas de sites para que coincidan con lo que el código espera
    sites = datos['sites'].copy()
    sites.rename(columns={
        'nombre': 'site_name',
        'latitud': 'latitude', 
        'longitud': 'longitude'
    }, inplace=True)
    
    # Agregar columnas que el código espera pero no están en el Excel
    sites['location'] = sites.apply(lambda row: f"{row['latitude']}, {row['longitude']}", axis=1)
    sites['ecosystem_type'] = sites['site_name'].apply(
        lambda x: 'Bosque' if 'Bosque' in x else 'Humedal' if 'Humedal' in x else 'Zona Minera'
    )
    
    # Transformar biodiversity_data
    biodiversity = datos['biodiversity'].copy()
    biodiversity.rename(columns={
        'especie_nombre': 'species',
        'abundancia': 'abundance'
    }, inplace=True)
    
    # Transformar trophic_data  
    trophic = datos['trophic'].copy()
    trophic.rename(columns={
        'conn_obs': 'connectance_observed',
        'conn_exp': 'connectance_expected', 
        'len_obs': 'length_observed',
        'len_exp': 'length_expected'
    }, inplace=True)
    
    # Transformar vsi_data
    vsi = datos['vsi'].copy()
    vsi.rename(columns={
        'cobertura_pct': 'coverage_pct',
        'calidad_suelo_pct': 'soil_quality_pct'
    }, inplace=True)
    
    return {
        'sites': sites,
        'biodiversity': biodiversity,
        'trophic': trophic,
        'vsi': vsi,
        'results': datos['results']
    }

def guardar_resultados_ehi(resultados_df):
    """Guarda los resultados calculados en la hoja results_ehi"""
    try:
        excel_path = os.path.join(app.config['DATA_FOLDER'], app.config['EXCEL_FILE'])
        
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            resultados_df.to_excel(writer, sheet_name='5-results_ehi', index=False)
        
        return True
    except Exception as e:
        print(f"Error guardando resultados: {e}")
        return False

# SOLO UNA DEFINICIÓN DE ESTA RUTA
@app.route('/')
def index():
    """Página principal con resumen de todos los sitios"""
    datos = cargar_datos_excel()
    datos_transformados = transformar_datos(datos)
    
    if datos_transformados is None:
        return render_template('index.html', error="No se pudo cargar el archivo de datos", zonas=[])
    
    # Combinar datos de sitios con resultados
    sites = datos_transformados['sites']
    results = datos_transformados['results'] if not datos_transformados['results'].empty else None
    
    if results is not None:
        zonas = pd.merge(sites, results, on='site_id', how='left')
    else:
        zonas = sites
    
    zonas_list = zonas.to_dict('records')
    
    return render_template('index.html', zonas=zonas_list)


@app.route('/zona/<site_id>')
def zona_detalle(site_id):
    """Vista detallada de un sitio específico con todos sus índices"""
    datos = cargar_datos_excel()
    datos_transformados = transformar_datos(datos)
    
    if datos_transformados is None:
        return "Error cargando datos", 500
    
    # Buscar el sitio
    site = datos_transformados['sites'][datos_transformados['sites']['site_id'] == site_id]
    
    if site.empty:
        return "Sitio no encontrado", 404
    
    site_data = site.iloc[0].to_dict()
    
    # Obtener datos de biodiversidad para este sitio (usar datos transformados)
    biodiv_data = datos_transformados['biodiversity'][datos_transformados['biodiversity']['site_id'] == site_id]
    
    # Obtener datos tróficos
    trophic_data = datos_transformados['trophic'][datos_transformados['trophic']['site_id'] == site_id]
    
    # Obtener datos VSI
    vsi_data = datos_transformados['vsi'][datos_transformados['vsi']['site_id'] == site_id]
    
    # Calcular índices
    bi = calcular_shannon_wiener(biodiv_data)
    tfi = calcular_tfi(trophic_data.iloc[0].to_dict() if not trophic_data.empty else {})
    vsi = calcular_vsi(vsi_data.iloc[0].to_dict() if not vsi_data.empty else {})
    ehi_result = calcular_ehi_completo(tfi, bi, vsi)
    
    # Buscar resultados guardados
    resultado_guardado = datos_transformados['results'][datos_transformados['results']['site_id'] == site_id]
    if not resultado_guardado.empty:
        resultado_guardado = resultado_guardado.iloc[0].to_dict()
    else:
        resultado_guardado = None
    
    # Pasar los datos de biodiversidad transformados
    return render_template('zona.html', 
                         zona=site_data,
                         bi=bi,
                         tfi=tfi,
                         vsi=vsi,
                         ehi=ehi_result,
                         resultado_guardado=resultado_guardado,
                         biodiv_especies=biodiv_data.to_dict('records') if not biodiv_data.empty else [])

@app.route('/admin')
def admin():
    """Panel administrativo para recalcular todos los índices"""
    datos = cargar_datos_excel()
    
    if datos is None:
        return render_template('admin.html', error="No se pudo cargar el archivo de datos")
    
    sites = datos['sites'].to_dict('records')
    results = datos['results'].to_dict('records') if not datos['results'].empty else []
    
    return render_template('admin.html', zonas=sites, resultados=results)

@app.route('/api/calcular/<site_id>', methods=['POST'])
def api_calcular_sitio(site_id):
    """Calcula todos los índices para un sitio específico"""
    try:
        datos = cargar_datos_excel()
        
        if datos is None:
            return jsonify({'error': 'No se pudo cargar datos'}), 500
        
        # Obtener datos del sitio
        biodiv_data = datos['biodiversity'][datos['biodiversity']['site_id'] == site_id]
        trophic_data = datos['trophic'][datos['trophic']['site_id'] == site_id]
        vsi_data = datos['vsi'][datos['vsi']['site_id'] == site_id]
        
        # Calcular índices
        bi = calcular_shannon_wiener(biodiv_data)
        tfi = calcular_tfi(trophic_data.iloc[0].to_dict() if not trophic_data.empty else {})
        vsi = calcular_vsi(vsi_data.iloc[0].to_dict() if not vsi_data.empty else {})
        ehi_result = calcular_ehi_completo(tfi, bi, vsi)
        
        return jsonify({
            'site_id': site_id,
            'BI': bi,
            'TFI': tfi,
            'VSI': vsi,
            'EHI': ehi_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calcular_todos', methods=['POST'])
def api_calcular_todos():
    """Recalcula EHI para todos los sitios y guarda en Excel"""
    try:
        datos = cargar_datos_excel()
        datos_transformados = transformar_datos(datos)
        
        if datos_transformados is None:
            return jsonify({'error': 'No se pudo cargar datos'}), 500
        
        resultados = []
        
        for _, site in datos_transformados['sites'].iterrows():
            site_id = site['site_id']
            
            # Obtener datos específicos
            biodiv_data = datos_transformados['biodiversity'][datos_transformados['biodiversity']['site_id'] == site_id]
            trophic_data = datos_transformados['trophic'][datos_transformados['trophic']['site_id'] == site_id]
            vsi_data = datos_transformados['vsi'][datos_transformados['vsi']['site_id'] == site_id]
            
            # Calcular índices
            bi = calcular_shannon_wiener(biodiv_data)
            tfi = calcular_tfi(trophic_data.iloc[0].to_dict() if not trophic_data.empty else {})
            vsi = calcular_vsi(vsi_data.iloc[0].to_dict() if not vsi_data.empty else {})
            ehi_result = calcular_ehi_completo(tfi, bi, vsi)
            
            resultados.append({
                'site_id': site_id,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'BI': bi['valor'],
                'TFI': tfi['valor'], 
                'VSI': vsi['valor'],
                'EHI': ehi_result['valor'],
                'categoria': ehi_result['categoria']
            })
        
        # Crear DataFrame y guardar
        resultados_df = pd.DataFrame(resultados)
        
        # Guardar en Excel (usando nombres de columnas consistentes)
        if guardar_resultados_ehi(resultados_df):
            return jsonify({
                'success': True,
                'total_sitios': len(datos_transformados['sites']),
                'resultados_calculados': len(resultados)
            })
        else:
            return jsonify({'error': 'Error guardando resultados'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas')
def api_estadisticas():
    """Devuelve estadísticas generales del ecosistema"""
    try:
        datos = cargar_datos_excel()
        
        if datos is None or datos['results'].empty:
            return jsonify({'error': 'No hay datos disponibles'}), 404
        
        results = datos['results']
        
        # Usar nombres de columnas en minúsculas (como están en el Excel)
        stats = {
            'total_sitios': len(results),
            'ehi_promedio': float(results['ehi'].mean()),
            'ehi_max': float(results['ehi'].max()),
            'ehi_min': float(results['ehi'].min()),
            'por_categoria': results['categoria'].value_counts().to_dict(),
            'bi_promedio': float(results['bi'].mean()),
            'tfi_promedio': float(results['tfi'].mean()),
            'vsi_promedio': float(results['vsi'].mean())
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparar', methods=['POST'])
def api_comparar_sitios():
    """Compara múltiples sitios"""
    try:
        site_ids = request.json.get('site_ids', [])
        
        if not site_ids:
            return jsonify({'error': 'No se proporcionaron site_ids'}), 400
        
        datos = cargar_datos_excel()
        results = datos['results'][datos['results']['site_id'].isin(site_ids)]
        sites = datos['sites'][datos['sites']['site_id'].isin(site_ids)]
        
        comparacion = pd.merge(sites, results, on='site_id', how='left')
        
        return jsonify(comparacion.to_dict('records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Crear carpeta de datos si no existe
    os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)