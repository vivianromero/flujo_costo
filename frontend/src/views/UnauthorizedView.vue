<template>
  <q-page class="flex flex-center column q-pa-xl">
    <q-card flat bordered class="q-pa-lg q-mt-xl" style="max-width: 400px; width: 100%;">
      <div class="text-center">
        <q-icon name="fas fa-user-lock" size="64px" class="text-negative q-mb-md" />
        <div class="text-h5 text-weight-bold text-grey-9 q-mb-sm">
          Acceso no autorizado
        </div>
        <div class="text-body2 text-grey-7 q-mb-lg">
          No tienes permisos para acceder a esta sección o tu sesión ha expirado.
        </div>
        <q-btn
          label="Ir al login"
          color="primary"
          icon="fas fa-sign-in-alt"
          unelevated
          @click="$router.push({ name: 'login' })"
        />

      </div>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
// No requiere lógica adicional
</script>
