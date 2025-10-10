<template>
  <!-- Ítem con submenú -->
  <div v-if="item.submenu?.length">
    <q-expansion-item
      :model-value="isExpanded"
      @update:model-value="toggleExpand"
      expand-separator
      dense
      :header-class="`menu-level-${level}`"
    >
      <template #header>
        <div class="menu-expandable-bg">
          <div class="menu-item-inline">
            <q-icon
              :name="isExpanded ? 'fa fa-angle-down' : 'fa fa-angle-right'"
              class="menu-expand-icon"
            />
            <q-icon :class="[item.icon_class, 'menu-icon-size']" />
            <span class="menu-label">{{ item.name }}</span>
          </div>
        </div>
      </template>

      <!-- 🔹 Renderiza hijos con control local -->
      <MenuItem
        v-for="child in item.submenu"
        :key="child.id"
        :item="child"
        :level="level + 1"
        :open-item="openItem"
        @set-open="setOpen"
        @navigate="emit('navigate', $event)"
      />
    </q-expansion-item>
  </div>

  <!-- Ítem sin submenú -->
  <q-item
    v-else
    clickable
    @click="emit('navigate', item.url)"
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
import { ref, watch } from 'vue'
import MenuItem from './MenuItem.vue'

const props = defineProps({
  item: Object,
  level: { type: Number, default: 0 },
  openItem: { type: [Number, String, null], default: null }
})

const emit = defineEmits(['navigate', 'set-open'])

const isExpanded = ref(false)
const openItem = ref(null) // control para hijos

// cerrar si otro hermano se abre
watch(
  () => props.openItem,
  (val) => {
    if (val !== props.item.id) isExpanded.value = false
  }
)

function toggleExpand(val) {
  isExpanded.value = val
  if (val) emit('set-open', props.item.id)
  else emit('set-open', null)
}

function setOpen(id) {
  openItem.value = id
}
</script>




