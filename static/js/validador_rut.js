///////////////////////////////////
// Validador de RUT para JavaScript
///////////////////////////////////

///////////////////////////////////
// Función: validarRut
// Descripción: Valida un RUT chileno con formato XX.XXX.XXX-K o XXXXXXXX-K
// Parámetro: rut (string)
// Retorna: boolean
///////////////////////////////////
function validarRut(rut) {
    rut = rut.replace(/\./g, '').replace(/-/g, '').toUpperCase();
    
    if (!/^\d{7,8}[0-9K]$/.test(rut)) {
        return false;
    }
    
    const numero = parseInt(rut.slice(0, -1));
    const verificador = rut.slice(-1);
    
    const multiplicadores = [2, 3, 4, 5, 6, 7];
    let suma = 0;
    let indice = 0;
    
    for (let i = String(numero).length - 1; i >= 0; i--) {
        suma += parseInt(String(numero)[i]) * multiplicadores[indice % 6];
        indice++;
    }
    
    let resto = 11 - (suma % 11);
    let digitoVerificador;
    
    if (resto === 11) {
        digitoVerificador = '0';
    } else if (resto === 10) {
        digitoVerificador = 'K';
    } else {
        digitoVerificador = String(resto);
    }
    
    return verificador === digitoVerificador;
}

///////////////////////////////////
// Función: formatearRut
// Descripción: Formatea un RUT a XX.XXX.XXX-K
// Parámetro: rut (string)
// Retorna: string formateado o null
///////////////////////////////////
function formatearRut(rut) {
    rut = rut.replace(/\./g, '').replace(/-/g, '').toUpperCase();
    
    if (rut.length < 8) {
        return null;
    }
    
    const numero = rut.slice(0, -1).padStart(8, '0');
    const verificador = rut.slice(-1);
    
    return `${numero.slice(0, 2)}.${numero.slice(2, 5)}.${numero.slice(5, 8)}-${verificador}`;
}