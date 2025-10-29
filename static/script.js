// EcoBalance - JavaScript principal

// Utilidades
const EcoBalance = {
    // Formatear números
    formatNumber: (num, decimals = 3) => {
        if (typeof num !== 'number' || isNaN(num)) return '--';
        return num.toFixed(decimals);
    },

    // Obtener color según valor EHI
    getColorByEHI: (value) => {
        if (value > 0.76) return '#22c55e';  // Verde
        if (value >= 0.51) return '#eab308';  // Amarillo
        if (value >= 0.26) return '#f97316';  // Naranja
        if (value >= 0.11) return '#ef4444';  // Rojo
        return '#000000';  // Negro
    },

    // Obtener categoría según valor
    getCategoryByValue: (value) => {
        if (value > 0.76) return 'Excelente';
        if (value >= 0.51) return 'Bueno';
        if (value >= 0.26) return 'Regular';
        if (value >= 0.11) return 'Pobre';
        return 'Crítico';
    },

    // Mostrar notificación
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        const colors = {
            'success': '#22c55e',
            'error': '#ef4444',
            'warning': '#f97316',
            'info': '#3b82f6'
        };

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type]};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    // Animaciones para gráficas circulares
    animateCircularProgress: (element, targetValue) => {
        const circle = element.querySelector('.progress-ring-circle');
        if (!circle) return;
        
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;
        
        const offset = circumference - (targetValue / 100) * circumference;
        circle.style.strokeDashoffset = offset;
    },

    // Hacer petición API con manejo de errores
    apiRequest: async (url, options = {}) => {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    }
};

// Animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
`;
document.head.appendChild(style);

// Funciones de comparación de sitios
const ComparacionSitios = {
    sitiosSeleccionados: [],

    toggleSeleccion: (siteId) => {
        const index = ComparacionSitios.sitiosSeleccionados.indexOf(siteId);
        if (index > -1) {
            ComparacionSitios.sitiosSeleccionados.splice(index, 1);
        } else {
            if (ComparacionSitios.sitiosSeleccionados.length >= 5) {
                EcoBalance.showNotification('Máximo 5 sitios para comparar', 'warning');
                return;
            }
            ComparacionSitios.sitiosSeleccionados.push(siteId);
        }
        ComparacionSitios.actualizarUI();
    },

    actualizarUI: () => {
        const count = ComparacionSitios.sitiosSeleccionados.length;
        const btn = document.getElementById('btnComparar');
        if (btn) {
            btn.textContent = `Comparar (${count})`;
            btn.disabled = count < 2;
        }
    },

    comparar: async () => {
        if (ComparacionSitios.sitiosSeleccionados.length < 2) {
            EcoBalance.showNotification('Selecciona al menos 2 sitios', 'warning');
            return;
        }

        const result = await EcoBalance.apiRequest('/api/comparar', {
            method: 'POST',
            body: JSON.stringify({
                site_ids: ComparacionSitios.sitiosSeleccionados
            })
        });

        if (result.success) {
            ComparacionSitios.mostrarComparacion(result.data);
        } else {
            EcoBalance.showNotification('Error al comparar sitios', 'error');
        }
    },

    mostrarComparacion: (datos) => {
        // Crear modal con comparación
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 900px;">
                <span class="close-modal" onclick="this.closest('.modal').remove()">&times;</span>
                <h3>📊 Comparación de Sitios</h3>
                <div class="comparison-grid">
                    ${datos.map(sitio => `
                        <div class="comparison-card">
                            <h4>${sitio.site_name}</h4>
                            <div class="ehi-value" style="color: ${sitio.color};">
                                ${EcoBalance.formatNumber(sitio.EHI, 4)}
                            </div>
                            <div class="comparison-indices">
                                <div><strong>TFI:</strong> ${EcoBalance.formatNumber(sitio.TFI, 3)}</div>
                                <div><strong>BI:</strong> ${EcoBalance.formatNumber(sitio.BI, 3)}</div>
                                <div><strong>VSI:</strong> ${EcoBalance.formatNumber(sitio.VSI, 3)}</div>
                            </div>
                            <div class="comparison-category" style="background: ${sitio.color}; color: white; padding: 0.5rem; border-radius: 0.5rem; margin-top: 0.5rem;">
                                ${sitio.categoria}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Agregar estilos para la comparación
        const compStyle = document.createElement('style');
        compStyle.textContent = `
            .comparison-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1.5rem;
            }
            .comparison-card {
                background: #f9fafb;
                padding: 1.5rem;
                border-radius: 0.5rem;
                text-align: center;
            }
            .comparison-card h4 {
                margin-bottom: 1rem;
                color: #1f2937;
            }
            .comparison-indices {
                margin: 1rem 0;
                font-size: 0.9rem;
            }
            .comparison-indices > div {
                padding: 0.25rem 0;
            }
        `;
        document.head.appendChild(compStyle);
    }
};

// Exportar datos a CSV
const ExportarDatos = {
    exportarCSV: (data, filename) => {
        const csv = ExportarDatos.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        EcoBalance.showNotification('Archivo descargado exitosamente', 'success');
    },

    convertToCSV: (data) => {
        if (!data || data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvRows = [];
        
        // Agregar encabezados
        csvRows.push(headers.join(','));
        
        // Agregar datos
        for (const row of data) {
            const values = headers.map(header => {
                const value = row[header];
                return typeof value === 'string' && value.includes(',') 
                    ? `"${value}"` 
                    : value;
            });
            csvRows.push(values.join(','));
        }
        
        return csvRows.join('\n');
    },

    exportarResultados: async () => {
        const result = await EcoBalance.apiRequest('/api/zonas');
        
        if (result.success) {
            ExportarDatos.exportarCSV(
                result.data, 
                `ecobalance_resultados_${new Date().toISOString().split('T')[0]}.csv`
            );
        } else {
            EcoBalance.showNotification('Error al exportar datos', 'error');
        }
    }
};

// Búsqueda y filtrado
const Filtros = {
    aplicarFiltros: () => {
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const categoryFilter = document.getElementById('categoryFilter')?.value || 'all';
        
        const cards = document.querySelectorAll('.site-card');
        
        cards.forEach(card => {
            const siteName = card.querySelector('h3')?.textContent.toLowerCase() || '';
            const category = card.querySelector('.ehi-category')?.textContent || '';
            
            const matchesSearch = siteName.includes(searchTerm);
            const matchesCategory = categoryFilter === 'all' || category === categoryFilter;
            
            card.style.display = matchesSearch && matchesCategory ? 'block' : 'none';
        });
    },

    resetFiltros: () => {
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        
        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = 'all';
        
        Filtros.aplicarFiltros();
    }
};

// Gráficas simples con Canvas
const Graficas = {
    crearGraficaBarras: (canvasId, datos, labels) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const barWidth = width / datos.length;
        const maxValue = Math.max(...datos);
        
        // Limpiar canvas
        ctx.clearRect(0, 0, width, height);
        
        // Dibujar barras
        datos.forEach((value, index) => {
            const barHeight = (value / maxValue) * (height - 40);
            const x = index * barWidth;
            const y = height - barHeight - 20;
            
            // Barra
            ctx.fillStyle = EcoBalance.getColorByEHI(value);
            ctx.fillRect(x + 5, y, barWidth - 10, barHeight);
            
            // Valor
            ctx.fillStyle = '#000';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(value.toFixed(3), x + barWidth / 2, y - 5);
            
            // Label
            if (labels && labels[index]) {
                ctx.fillText(labels[index], x + barWidth / 2, height - 5);
            }
        });
    }
};

// Validación de formularios
const Validacion = {
    validarRango: (value, min, max) => {
        const num = parseFloat(value);
        return !isNaN(num) && num >= min && num <= max;
    },

    validarFormulario: (formId) => {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        const inputs = form.querySelectorAll('input[required]');
        let valid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('invalid');
                valid = false;
            } else {
                input.classList.remove('invalid');
            }
        });
        
        return valid;
    }
};

// Atajos de teclado
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Búsqueda rápida
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape: Cerrar modales
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌿 EcoBalance cargado correctamente');
    
    // Agregar listeners para búsqueda en tiempo real
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', Filtros.aplicarFiltros);
    }
    
    // Agregar listeners para filtros
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', Filtros.aplicarFiltros);
    }
    
    // Tooltips simples
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = e.target.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #1f2937;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
            `;
            document.body.appendChild(tooltip);
            
            const rect = e.target.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            
            e.target._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', (e) => {
            if (e.target._tooltip) {
                e.target._tooltip.remove();
                delete e.target._tooltip;
            }
        });
    });
    
    // Auto-actualizar reloj si existe
    const updateClock = () => {
        const clockElement = document.getElementById('currentTime');
        if (clockElement) {
            const now = new Date();
            clockElement.textContent = now.toLocaleTimeString('es-MX', {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    };
    updateClock();
    setInterval(updateClock, 60000); // Actualizar cada minuto
    
    // Animación de entrada para cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.5s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.site-card, .component-card, .stat-card').forEach(card => {
        observer.observe(card);
    });
});

// Hacer disponibles funciones globalmente
window.EcoBalance = EcoBalance;
window.ComparacionSitios = ComparacionSitios;
window.ExportarDatos = ExportarDatos;
window.Filtros = Filtros;
window.Graficas = Graficas;
window.Validacion = Validacion;

// Service Worker para modo offline (opcional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Descomenta si quieres soporte offline
        // navigator.serviceWorker.register('/static/sw.js')
        //     .then(reg => console.log('Service Worker registrado'))
        //     .catch(err => console.log('Error en Service Worker:', err));
    });
}