<template>
  <!-- Ítem con submenú -->
 <q-expansion-item
  v-if="item.submenu?.length"
  v-model="isExpanded"
  :label="item.name"
  icon=""
  :header-class="`menu-level-${level}`"
  expand-separator
  dense
>
  <template #header>
  <div class="menu-expandable-bg">
    <div class="menu-item-inline">
      <q-icon :name="isExpanded ? 'fa fa-angle-down' : 'fa fa-angle-right'" class="menu-expand-icon" />
      <q-icon :class="[item.icon_class, 'menu-icon-size']" />
      <span class="menu-label">{{ item.name }}</span>
    </div>
  </div>
</template>


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
    <div class="menu-item-inline">
      <q-icon :class="[item.icon_class, 'menu-icon-size']" />
      <span>{{ item.name }}</span>
    </div>
  </q-item>

</template>

<script setup>
import { QExpansionItem, QItem, QItemSection, QIcon } from 'quasar'
import MenuItem from './MenuItem.vue'

import { ref } from 'vue'
const isExpanded = ref(false)

defineProps({
  item: Object,
  level: { type: Number, default: 0 }
})

defineEmits(['navigate'])

function go(url) {
  emit('navigate', url)
}
</script>
