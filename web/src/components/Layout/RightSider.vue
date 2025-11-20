<template>
  <aside class="right-sider">
    <div class="right-sidebar-content">
      <!-- 动态加载路由对应的设置组件 -->
      <component :is="routeComponent" v-if="routeComponent" />
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Settings from '@/views/star/Settings.vue'

const route = useRoute()

// 根据路由动态加载设置组件
const routeComponent = computed(() => {
  const path = route.path
  if (path === '/star-pattern' || path.startsWith('/star-pattern')) {
    return Settings
  }
  return null
})
</script>

<style scoped>
.right-sider {
  width: 250px;
  background: white;
  border-left: 1px solid #e4e7ed;
  overflow-y: auto;
}

.right-sidebar-content {
  padding: 20px;
}
</style>
