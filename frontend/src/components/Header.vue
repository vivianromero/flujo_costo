<template>
  <q-header elevated class="header-institucional">
    <div class="row items-center justify-between full-width q-px-xl q-py-sm">
      <div class="col-auto">
        <LogoEmpresa />
      </div>
      <div class="col-auto">
        <UsuarioPanel />
      </div>
    </div>
  </q-header>
</template>

<script setup lang="ts">
import LogoEmpresa from '@/components/LogoEmpresa.vue'
import UsuarioPanel from '@/components/UsuarioPanel.vue'
</script>









