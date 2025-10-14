<template>
  <q-footer reveal bordered class="bg-grey-6 text-white" height-hint="28">
    <q-toolbar dense class="q-pa-none q-pl-sm q-pr-sm footer-toolbar">

      <!-- Izquierda con icono -->
      <div class="footer-left" >
        <strong>&copy; {{ footerStore.year }}</strong>

        <span v-if="footerStore.site" class="footer-site">
          <img v-if="footerStore.site.icon" :src="footerStore.site.icon" alt="Logo" class="footer-img rotacion-derecha"/>
          <strong>{{ footerStore.site.name }}</strong>
        </span>

        <span>Todos los derechos reservados.</span>
      </div>

      <!-- Derecha -->
      <div class="footer-right">
        <b>Versión</b> {{ footerStore.version }}
      </div>

    </q-toolbar>
  </q-footer>
</template>


<script setup lang="ts">
import { useFooterStore } from '@/stores/footer'

const footerStore = useFooterStore()
</script>



