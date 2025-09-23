<template>
  <div class="login-page">
    <div class="login-box">
      <div class="card">
        <div class="card-header">
          <div class="logo-container">
            <img src="/img/cubatabaco_logo.png" alt="Logo" class="logo" />
          </div>
        </div>

        <div class="card-body">
          <p class="login-msg">Introduzca sus datos para comenzar la sesión</p>
          <p v-if="error" class="error-msg">{{ error }}</p>
          <div class="form-group">
            <div class="input-wrapper">
              <input v-model="username" class="form-input" placeholder="Usuario" />
              <i class="fa fa-user input-icon"></i>
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
import '@/assets/css/login.css'
import { useSessionStore } from '@/stores/session'


const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const router = useRouter()
const session = useSessionStore()

function togglePassword() {
  showPassword.value = !showPassword.value
}

async function login() {
  const query = `
    mutation {
      tokenAuth(username: "${username.value}", password: "${password.value}") {
        token
      }
    }
  `

  try {
    const res = await fetch('http://localhost:9090/graphql/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    })

    const { data, errors } = await res.json()

    if (errors) {
      error.value = 'Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.'
    } else {
        session.setToken(data.tokenAuth.token)
        router.push('/')
    }
  } catch (e) {
    error.value = 'Error de red o servidor'
  }

}
</script>


