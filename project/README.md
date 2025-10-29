# Eco-Balance: Sistema de Monitoreo Ambiental en Tiempo Real

#### Video Demo: https://youtu.be/FEDbc3VOjWk

##Descripción

**Eco-Balance** es una aplicación web progresiva (PWA) diseñada para el monitoreo y análisis de la salud de ecosistemas mediante el cálculo del **Índice de Salud Ecológica (EHI)**.  
Este proyecto fue desarrollado como trabajo final para el curso **CS50 de Harvard** y combina ciencia de la computación con sostenibilidad ambiental.

##Propósito del Proyecto

El sistema permite evaluar el estado de conservación de diferentes ecosistemas mediante tres índices científicos principales que se combinan en un indicador global (EHI).

### Objetivos principales:
- **Monitoreo en tiempo real** de múltiples sitios ecológicos  
- **Cálculo automático** de índices científicos validados  
- **Visualización interactiva** mediante mapas y dashboards  
- **Generación de recomendaciones** basadas en el estado ecológico  
- **Almacenamiento persistente** de datos históricos  

##Arquitectura del Sistema

###Tecnologías Utilizadas
- **Backend:** Flask (Python) con API REST  
- **Frontend:** HTML5, CSS3, JavaScript Vanilla  
- **Base de Datos:** Archivos Excel con *pandas* (para simplicidad en el MVP)  
- **Mapas:** Leaflet.js para visualización geográfica  
- **Estilos:** CSS responsivo y personalizado  
- **Cálculos:** Modelos matemáticos para índices ecológicos  

###Estructura de Archivos
```
EcoBalance/
├── app.py
├── models/
│   ├── biodiversidad.py
│   ├── ehi.py
│   ├── tfi.py
│   └── vsi.py
├── templates/
│   ├── index.html
│   ├── admin.html
│   ├── zona.html
│   └── componentes/
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/
└── data/
    └── EcoBalance_Datos.xlsx
```

##Componentes Científicos

### Índices de Evaluación

#### 1. Índice de Biodiversidad (BI) — 30% del EHI
**Fórmula:**  
H' = -Σ(pᵢ × ln(pᵢ)) donde pᵢ = nᵢ/N

```python
def calcular_shannon_wiener(datos_biodiversidad):
    pass  # Implementación del algoritmo científico
```

#### 2. Índice de Fragmentación del Territorio (TFI) — 50%
**Fórmula:**  
TFI = (Conectividad Observada / Conectividad Esperada) × (Longitud Observada / Longitud Esperada)

#### 3. Índice de Vulnerabilidad del Suelo (VSI) — 20%
**Fórmula:**  
VSI = (Cobertura × 0.6) + (Calidad del Suelo × 0.4)

### Índice de Salud Ecológica (EHI)
```
EHI = (TFI × 0.5) + (BI × 0.3) + (VSI × 0.2)
```

#### Escala de Categorización
| Categoría | Rango | Color |
|------------|--------|--------|
| Excelente | >0.76 | 🟢 Verde |
| Bueno | 0.51–0.75 | 🔵 Azul |
| Regular | 0.26–0.50 | 🟡 Amarillo |
| Pobre | 0.11–0.25 | 🔴 Rojo |
| Crítico | <0.11 | ⚫ Negro |

##Explicación Detallada de Archivos

### `app.py`
- Configuración de Flask y rutas  
- Carga de datos desde Excel  
- API REST para cálculos  
- Gestión de sesiones y templates

### `models/`
- `biodiversidad.py`, `ehi.py`, `tfi.py`, `vsi.py` → cálculos científicos

### `templates/`
- `index.html` → dashboard interactivo  
- `zona.html` → detalle de sitios  
- `admin.html` → panel de control

### `static/`
- `style.css` → sistema de diseño y paleta de colores  
- `script.js` → interactividad y visualizaciones

##Cómo Ejecutar

### Requisitos
- Python 3.8+
- Flask 2.0+
- pandas
- openpyxl

### Instalación
```bash
git clone <repo>
pip install flask pandas openpyxl
python app.py
```
Abrir en navegador: http://localhost:5000

### Estructura del Excel
1. 1-sites  
2. 2-biodiversity_data  
3. 3-trophic_data  
4. 4-vsi_data  
5. 5-results_ehi

##Resultados y Validación
| Ecosistema | EHI | Estado |
|------------|-----|-------|
| Bosque Protegido | 0.823 | 🟢 Excelente |
| Humedal Urbano | 0.450 | 🟡 Regular |
| Zona Minera | 0.224 | 🔴 Pobre |

##Futuras Mejoras
- Corto plazo: autenticación, PDF, panel en tiempo real  
- Medio plazo: migración SQL, API pública, alertas por email  
- Largo plazo: ML, sensores IoT, plataforma colaborativa

##Contribución
- Nuevos índices ecológicos  
- Optimización de algoritmos  
- Traducciones

##Conclusión
Eco-Balance combina ciencia de datos y ecología, demostrando cómo la tecnología puede apoyar la conservación ambiental.