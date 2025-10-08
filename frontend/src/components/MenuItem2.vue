<template>
  <q-expansion-item
      v-if="item.submenu?.length"
      :label="`${item.name}`"
      :icon="item.icon_class"
      :header-class="`menu-level-${level}`"
      expand-separator
  >

    <MenuItem
      v-for="child in item.submenu"
      :key="child.id"
      :item="child"
      :level="level + 1"
      @navigate="go"
    />

  </q-expansion-item>

  <q-item
      v-else
      clickable
      @click="go(item.url)"
      :class="`menu-level-${level}`"
  >
  <q-item-section avatar v-if="item.icon_class">
      <div class="menu-icon-wrapper">
        <q-icon :class="item.icon_class" />
      </div>
    </q-item-section>
  <q-item-section :class="`menu-level-${level}`">
    {{ item.name }}
  </q-item-section>
</q-item>
</template>

<script setup>
import { QExpansionItem, QItem, QItemSection, QIcon } from 'quasar'
import MenuItem from './MenuItem.vue'

defineProps({
  item: Object,
  level: { type: Number, default: 0 }
})

defineEmits(['navigate'])

function go(url) {
  emit('navigate', url)
}
</script>
