// ============================================
// COMPONENTES REUTILIZABLES - MÓDULO PACIENTES
// ============================================

/**
 * Configuración de roles del sistema
 * @type {Object}
 */
const ROLES_CONFIG = {
    admin: {
        label: 'Administrativo',
        icon: 'bi-person-badge',
        color: '#6366f1',
        colorDark: '#4f46e5',
        stats: [
            { icon: 'bi-file-earmark-text', label: 'Ingresos Hoy', value: 0, key: 'ingresos_hoy' },
            { icon: 'bi-people', label: 'Registros Pendientes', value: 0, key: 'registros_pendientes' }
        ]
    },
    matrona: {
        label: 'Matrona',
        icon: 'bi-heart-pulse',
        color: '#ec4899',
        colorDark: '#be185d',
        stats: [
            { icon: 'bi-person-heart', label: 'Pacientes Activos', value: 0, key: 'pacientes_activos' },
            { icon: 'bi-calendar2-check', label: 'Controles Pendientes', value: 0, key: 'controles_pendientes' }
        ]
    },
    medico: {
        label: 'Médico',
        icon: 'bi-stethoscope',
        color: '#3b82f6',
        colorDark: '#1e40af',
        stats: [
            { icon: 'bi-door-open', label: 'Admisiones Hoy', value: 0, key: 'admisiones_hoy' },
            { icon: 'bi-exclamation-circle', label: 'Alertas Activas', value: 0, key: 'alertas_activas' }
        ]
    },
    sistema: {
        label: 'Sistema',
        icon: 'bi-gear',
        color: '#8b5cf6',
        colorDark: '#6d28d9',
        stats: [
            { icon: 'bi-wifi2', label: 'APIs Activas', value: 6, key: 'apis_activas' },
            { icon: 'bi-database', label: 'Base de Datos', value: '100%', key: 'db_status' }
        ]
    }
};

/**
 * Clase para gestionar estadísticas por rol
 */
class DashboardStats {
    constructor(containerId = 'dashboard-container') {
        this.container = document.getElementById(containerId);
        this.data = {};
        this.init();
    }

    /**
     * Inicializa el dashboard
     */
    init() {
        this.render();
        this.attachEventListeners();
    }

    /**
     * Renderiza todas las secciones de roles
     */
    render() {
        let html = '<div class="container-fluid py-4">';
        html += '<h1 class="mb-4" style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">Dashboard - Módulo Gestión de Pacientes</h1>';

        Object.entries(ROLES_CONFIG).forEach(([roleKey, roleConfig]) => {
            html += this.renderRoleSection(roleKey, roleConfig);
        });

        html += '</div>';
        this.container.innerHTML = html;
    }

    /**
     * Renderiza una sección de rol
     */
    renderRoleSection(roleKey, roleConfig) {
        const statsHtml = roleConfig.stats
            .map(stat => this.renderStatCard(roleKey, stat))
            .join('');

        return `
            <div class="role-section">
                <div class="role-title" style="border-color: ${roleConfig.color};">
                    <i class="bi ${roleConfig.icon}"></i> ${roleConfig.label}
                </div>
                <div class="row g-3">
                    ${statsHtml}
                </div>
            </div>
        `;
    }

    /**
     * Renderiza una tarjeta de estadística
     */
    renderStatCard(roleKey, stat) {
        const gradient = `linear-gradient(135deg, ${ROLES_CONFIG[roleKey].color} 0%, ${ROLES_CONFIG[roleKey].colorDark} 100%)`;
        
        return `
            <div class="col-md-6 col-lg-3">
                <div class="stat-card" style="background: ${gradient};">
                    <i class="bi ${stat.icon}"></i>
                    <div class="stat-content">
                        <p class="stat-number" data-key="${stat.key}">${stat.value}</p>
                        <p class="stat-label">${stat.label}</p>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Actualiza el valor de una estadística
     * @param {string} key - Identificador de la estadística
     * @param {number|string} value - Nuevo valor
     */
    updateStat(key, value) {
        const element = document.querySelector(`[data-key="${key}"]`);
        if (element) {
            element.textContent = value;
            this.animateUpdate(element);
        }
    }

    /**
     * Anima la actualización de un valor
     */
    animateUpdate(element) {
        element.style.opacity = '0.5';
        setTimeout(() => {
            element.style.opacity = '1';
        }, 200);
    }

    /**
     * Actualiza múltiples estadísticas
     * @param {Object} updates - Objeto con clave-valor
     */
    updateStats(updates) {
        Object.entries(updates).forEach(([key, value]) => {
            this.updateStat(key, value);
        });
    }

    /**
     * Adjunta event listeners
     */
    attachEventListeners() {
        // Aquí irían listeners para eventos de actualización en tiempo real
    }

    /**
     * Obtiene la configuración de un rol
     */
    getRoleConfig(roleKey) {
        return ROLES_CONFIG[roleKey];
    }

    /**
     * Obtiene todos los roles
     */
    getAllRoles() {
        return Object.keys(ROLES_CONFIG);
    }
}

// ============================================
// USO EN APLICACIÓN
// ============================================

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardStats('dashboard-container');

    // Ejemplo: Actualizar estadísticas después de obtener datos
    // (Simularía una llamada a API)
    setTimeout(() => {
        dashboard.updateStats({
            'ingresos_hoy': 5,
            'registros_pendientes': 3,
            'pacientes_activos': 12,
            'controles_pendientes': 8,
            'admisiones_hoy': 2,
            'alertas_activas': 1
        });
    }, 500);
});
