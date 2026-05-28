# Flujo Costo - Frontend

Aplicación frontend para el sistema de gestión de flujo de costos, desarrollada con **Vue 3**, **Quasar** y **TypeScript**.

## 🚀 Tecnologías Principales

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| **Vue.js** | 3.5.18 | Framework progresivo para la interfaz de usuario |
| **Vite** | 7.1.2 | Build tool y servidor de desarrollo ultrarrápido |
| **Quasar** | 2.18.5 | Framework UI con componentes listos para usar |
| **TypeScript** | 5.8.3 | Tipado estático para JavaScript |
| **Pinia** | 3.0.3 | Manejo de estado (reemplaza Vuex) |
| **Vue Router** | 4.5.1 | Enrutamiento oficial para Vue.js |
| **Apollo Client** | 3.14.0 | Cliente GraphQL para comunicación con el backend |
| **GraphQL** | 16.11.0 | Lenguaje de consulta para APIs |

## 📋 Requisitos Previos

### Node.js
- **Versión requerida:** 20.19.0 o superior (recomendada 22.22.1)
- **Opción A (recomendada):** Usar NVM (Node Version Manager)
- **Opción B:** Instalar Node.js directamente desde [nodejs.org](https://nodejs.org) (versión LTS)

### NPM
- **Versión:** 10.x o superior (incluida con Node.js)

## 🔧 Configuración del Entorno

### Backend (requisito previo)
El frontend espera un backend corriendo en el puerto `9090` con el endpoint `/api`.

```bash
# El backend debe estar corriendo en:
http://localhost:9090

## 🔧 Configuración del Entorno

### 1. Instalar npm (si no lo tienes)
```bash
npm install

### 2. 🚀 Ejecución en Desarrollo
```bash

npm run dev

La aplicación estará disponible en http://localhost:5173