<template>
  <div class="flex flex-center column q-pa-xl text-center text-grey-8">
    <!-- Ícono animado -->
    <q-icon
      name="fa-solid fa-tools"
      size="80px"
      color="ocre"
      class="animate-bounce"
    />

    <!-- Mensaje principal -->
    <h3 class="q-mt-md text-h5 text-weight-medium">Página en construcción</h3>
    <p class="text-subtitle2 text-grey-7 q-mt-xs">
      Aún no hay una vista disponible para:
      <strong class="text-primary">{{ $route.path }}</strong>
    </p>

    <!-- Botón volver -->
    <q-btn
      color="primary"
      icon="fa-solid fa-house"
      label="Volver al inicio"
      class="q-mt-lg"
      @click="goHome"
      unelevated
      rounded
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { QBtn, QIcon } from 'quasar'

const router = useRouter()

function goHome() {
  router.push('/')
}

</script>


