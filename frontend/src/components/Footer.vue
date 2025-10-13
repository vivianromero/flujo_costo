<template>
  <q-footer reveal bordered class="bg-grey-6 text-white" height-hint="28">
    <q-toolbar dense class="q-pa-none q-pl-sm q-pr-sm" style="height: 28px; min-height: 28px; display: flex; justify-content: space-between; align-items: center;">

      <!-- Izquierda con icono -->
      <div class="footer-left" style="font-size: 11px; display: flex; align-items: center; gap: 4px;">
        <strong>&copy; {{ footerStore.year }}</strong>

        <span v-if="footerStore.site" style="display: flex; align-items: center; gap: 4px;">
          <img v-if="footerStore.site.icon" :src="footerStore.site.icon" alt="Logo" style="height: 16px; width: auto;" />
          <strong>{{ footerStore.site.name }}</strong>
        </span>

        <span>Todos los derechos reservados.</span>
      </div>

      <!-- Derecha -->
      <div class="footer-right" style="font-size: 11px;">
        <b>Version</b> {{ footerStore.version }}
      </div>

    </q-toolbar>
  </q-footer>
</template>

<script setup lang="ts">
import { useFooterStore } from '@/stores/footer'

const footerStore = useFooterStore()
</script>

<style scoped>
a {
  color: inherit;
  text-decoration: underline;
}
</style>


