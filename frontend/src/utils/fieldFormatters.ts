// 🔥 FORMATEADOR PARA CAMPOS BOOLEANOS
export const booleanFormatter = (value: boolean, options: {
  trueText?: string,
  falseText?: string
} = {}) => {
  const {
    trueText = '✅ Activa',
    falseText = '❌ Inactiva'
  } = options

  return value ? trueText : falseText
}

// 🔥 FORMATEADOR PARA CAMPOS DE TEXTO (E/S, etc.)
export const textFormatter = (value: string, mappings: Record<string, string>) => {
  return mappings[value] || value // Devuelve el mapeo o el valor original si no existe
}

// 🔥 FORMATEADORES PREDEFINIDOS COMUNES
export const formatters = {
  // Booleanos
  activa: (value: boolean) => booleanFormatter(value, {
    trueText: '✅ Activa',
    falseText: '❌ Inactiva'
  }),

  empresa: (value: boolean) => booleanFormatter(value, {
    trueText: '🏢 Empresa',
    falseText: ''
  }),

  comercializadora: (value: boolean) => booleanFormatter(value, {
    trueText: '💰 Comercializadora',
    falseText: ''
  }),

  estado: (value: boolean) => booleanFormatter(value, {
    trueText: '✅ Activo',
    falseText: '❌ Inactivo'
  }),

  siNo: (value: boolean) => booleanFormatter(value, {
    trueText: '✅ Sí',
    falseText: '❌ No'
  }),

  aumentoDisminucion: (value: boolean) => booleanFormatter(value, {
    trueText: 'Aumento',
    falseText: 'Disminución'
  }),

  // 🔥 NUEVO: FORMATEADOR PARA ENTRADA/SALIDA
  entradaSalida: (value: string) => textFormatter(value, {
    'E': 'Entrada',
    'S': 'Salida',
  }),
}
