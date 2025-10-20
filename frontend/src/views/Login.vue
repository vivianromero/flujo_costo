<template>
  <div class="login-page">
    <div class="login-box">
      <div class="card">
        <div class="card-header">
          <div class="logo-container">
            <img src="@/assets/img/cubatabaco_logo.png" alt="Logo" class="logo" />
          </div>
        </div>

        <div class="card-body">
          <p class="login-msg">Introduzca sus datos para comenzar la sesión</p>
          <p v-if="error" class="error-msg">{{ error }}</p>

          <div class="form-group">
            <div class="input-wrapper">
              <input v-model="username" class="form-input" placeholder="Usuario" />
              <i class="fa fa-user input-icon "></i>
            </div>
          </div>

          <div class="form-group">
            <div class="input-wrapper">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                class="form-input"
                placeholder="Contraseña"
              />
              <i
                :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"
                class="input-icon"
                @click="togglePassword"
                title="Mostrar/Ocultar contraseña"
              ></i>
            </div>
          </div>

          <button class="btn-login" @click="login">Entrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/utils/useAuth'
import '@/assets/css/login.css'

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const router = useRouter()
const auth = useAuth()

function togglePassword() {
  showPassword.value = !showPassword.value
}

async function login() {
  try {
    // 1. Autenticación
    const queryLogin = `
      mutation {
        tokenAuth(username: "${username.value}", password: "${password.value}") {
          token
        }
      }
    `
    const resLogin = await fetch('http://localhost:9090/graphql/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: queryLogin })
    })

    const { data, errors } = await resLogin.json()
    if (errors || !data?.tokenAuth?.token) {
      error.value = 'Por favor, introduzca un nombre de usuario y clave correctos.'
      return
    }

    const token = data.tokenAuth.token

    // 2. Consulta de usuario
    const queryMe = `
      query {
        me {
          username
          ueb
          isAdminempresa
          isOperflujo
          isOpercosto
          isAdmin
        }
      }
    `
    const resMe = await fetch('http://localhost:9090/graphql/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `JWT ${token}`
      },
      body: JSON.stringify({ query: queryMe })
    })

    const resMeJson = await resMe.json()
    const name = resMeJson?.data?.me?.username || 'Usuario'
    const unidad = resMeJson?.data?.me?.ueb || 'Unidad'
    const isOperflujo = resMeJson?.data?.me?.isOperflujo || false
    const isOpercosto = resMeJson?.data?.me?.isOpercosto || false
    const isAdminempresa = resMeJson?.data?.me?.isAdminempresa || false
    const isAdmin = resMeJson?.data?.me?.isAdmin || false

    console.log('isAdmin Login:', isAdmin)
    console.log('isAdminempresa Login:', isAdminempresa)

    // 3. Delegar a useAuth
    auth.login(token, name, unidad, isAdmin, isAdminempresa, isOperflujo, isOpercosto)
    router.push({ name: 'home' })
  } catch (e) {
    error.value = 'Error de red o servidor: ' + String(e)
  }
}
</script>







