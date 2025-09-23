<template>
  <header class="header">
    <div class="usuario-area">
      <i class="fas fa-user"></i>
      <span>{{ session.username }}</span>
      <button @click="logout">Salir</button>
    </div>

    <div class="logo-area">
      <img src="/img/cubatabaco_logo.png" alt="Logo" class="logo" />
      <div class="empresa">
        <h1>TABACUBA</h1>
        <p>Empresa de Tabaco Torcido Villa Clara</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
    import { useSessionStore } from '@/stores/session'
    import { useRouter } from 'vue-router'

    const session = useSessionStore()
    const router = useRouter()

    function logout() {
      session.clearSession()
      router.push('/login')
    }
</script>


<style scoped>
.header {
  position: relative;
  background-color: #eab676;
  color: #003366;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 1rem;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  width: 60px;
  height: auto;
}

.empresa h1 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: bold;
}

.empresa p {
  margin: 0;
  font-size: 0.9rem;
}

.usuario-area {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
}

.usuario-area span {
  font-weight: 500;
  color: #003366;
  margin-left: 0.2rem;
  margin-right: 1rem;
}

button {
  background-color: #703d03;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
}

</style>

