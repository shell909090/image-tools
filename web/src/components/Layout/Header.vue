<template>
  <header class="header">
    <div class="header-left mx-8">
      <h1 class="title">Image Tools</h1>
    </div>
    <div class="header-menu">
      <el-menu
        :default-active="activeMenu"
        mode="horizontal"
        class="header-menu-container"
        @select="handleMenuSelect"
      >
        <el-menu-item index="star-pattern">星星点位绘制工具</el-menu-item>
        <el-menu-item index="puzzle-pattern">拼图工具</el-menu-item>
      </el-menu>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => {
  if (route.path === '/' || route.path === '/star-pattern') {
    return 'star-pattern'
  }
  return route.path
})

const handleMenuSelect = (index) => {
  if (index === 'star-pattern') {
    router.push('/star-pattern')
  }
  if (index === 'puzzle-pattern') {
    router.push('/puzzle-pattern')
  }
}
</script>

<style scoped>
.header {
  height: 60px;
  background: #294970;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.header-left .title {
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  margin: 0px;
}

.header-menu {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-menu-container {
  background: transparent;
  border-bottom: none;
  width: 100%;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
  display: flex;
  flex-wrap: nowrap;
  overflow: visible;
}

:deep(.el-menu--horizontal .el-menu-item) {
  color: rgba(255, 255, 255, 0.8);
  border-bottom: 2px solid transparent;
  height: 60px;
  line-height: 60px;
  white-space: nowrap;
  flex-shrink: 0;
}

:deep(.el-menu--horizontal .el-menu-item:hover) {
  /* color: #fff; */
  color: #ff9800;
  background: rgba(255, 255, 255, 0.1);
}

:deep(.el-menu--horizontal .el-menu-item.is-active) {
  color: #ff9800 !important;
  background: #1b385b;
  border-bottom-width: 2px;
  border-bottom-color: #ff9800;
}

:deep(.el-menu--horizontal .el-submenu) {
  display: none;
}
</style>
