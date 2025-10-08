<template>
  <!-- Ítem con submenú -->
  <q-expansion-item
    v-if="item.submenu?.length"
    :label="item.name"
    :icon="item.icon_class"
    :header-class="`menu-level-${level}`"
    expand-separator
    dense
  >
    <MenuItem
      v-for="child in item.submenu"
      :key="child.id"
      :item="child"
      :level="level + 1"
      @navigate="go"
    />
  </q-expansion-item>

  <!-- Ítem final sin submenú -->
  <q-item
    v-else
    clickable
    @click="go(item.url)"
    :class="`menu-level-${level}`"
    dense
  >
    <q-item-section avatar v-if="item.icon_class">
      <q-icon :class="item.icon_class" />
    </q-item-section>

    <q-item-section>
      {{ item.name }}
    </q-item-section>
  </q-item>
</template>

<script setup>
import Menu from '@/components/Menu.vue'

defineProps({
  item: Object,
  level: { type: Number, default: 0 }
})

defineEmits(['navigate'])

function go(url) {
  emit('navigate', url)
}
</script>
