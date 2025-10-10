<template>
  <!-- Ítem con submenú -->
  <q-expansion-item
    v-if="item.submenu?.length"
    :model-value="isExpanded"
    @update:model-value="onToggle"
    :label="item.name"
    :header-class="`menu-level-${level}`"
    expand-separator
    dense
  >
    <template #header>
      <div class="menu-item-inline">
        <q-icon :name="isExpanded ? 'fa fa-angle-down' : 'fa fa-angle-right'" class="menu-expand-icon" />
        <q-icon :class="[item.icon_class, 'menu-icon-size']" />
        <span class="menu-label">{{ item.name }}</span>
      </div>
    </template>

    <!-- 👇 IMPORTANTE: siempre pasamos item.submenu como parentSubmenu -->
    <MenuItem
      v-for="child in item.submenu"
      :key="child.id"
      :item="child"
      :level="level + 1"
      :open-items="openItems"
      :parent-submenu="item.submenu"
      @toggle="childToggle"
      @navigate="$emit('navigate', $event)"
    />
  </q-expansion-item>

  <!-- Ítem final sin submenú -->
  <q-item
    v-else
    clickable
    @click="$emit('navigate', item.url)"
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
import { computed } from 'vue'
import { QExpansionItem, QItem, QIcon } from 'quasar'
import MenuItem from './MenuItem.vue'

const props = defineProps({
  item: Object,
  level: { type: Number, default: 0 },
  openItems: Array,
  parentSubmenu: Array // 👈 agregado
})

const emit = defineEmits(['navigate', 'toggle'])

const isExpanded = computed(() => props.openItems.includes(props.item.id))

function onToggle() {
  console.log(`[ON TOGGLE] ${props.item.name} | Nivel: ${props.level}`)
  emit('toggle', { item: props.item, parentSubmenu: props.parentSubmenu })
}

function childToggle(payload) {
  emit('toggle', payload)
}
</script>







