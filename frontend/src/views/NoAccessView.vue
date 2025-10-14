<template>
  <q-page class="flex flex-center column q-pa-xl">
    <q-card flat bordered class="q-pa-lg q-mt-xl" style="max-width: 400px; width: 100%;">
      <div class="text-center">
        <q-icon name="fas fa-user-lock" size="64px" class="text-negative q-mb-md" />
        <div class="text-h5 text-weight-bold text-grey-9 q-mb-sm">
          Acceso no autorizado
        </div>
        <div class="text-body2 text-grey-7 q-mb-lg">
          Usted está tratando de acceder a una opción que no existe o no tiene permisos.
        </div>
        <q-btn
          color="primary"
          icon="fa-solid fa-house"
          label="Volver al inicio"
          class="q-mt-lg"
          unelevated
          rounded
          @click="$router.push({ name: 'home' })"
        />
      </div>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
// No requiere lógica adicional
</script>
