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

// 🔥 FORMATEADORES PREDEFINIDOS COMUNES
export const formatters = {
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
  })
}