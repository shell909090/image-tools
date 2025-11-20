<template>
  <div>
    <!-- 星星点位输入 -->
    <div class="section">
      <div>
        <h3 class="section-title">星星点位数据</h3>
      </div>
      
      <!-- JSON输入框 -->
      <div class="json-input-section">
        <el-input
          v-model="jsonInput"
          type="textarea"
          :rows="14"
          placeholder="请输入JSON格式的星星点位数据"
          :class="{ 'input-error': jsonError }"
        />
        <div v-if="jsonError" class="error-message">{{ jsonError }}</div>
        <!-- 示例数据 -->
        <div class="text-right">
          <el-button text @click="loadExample">加载示例数据</el-button>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="generateStars" :disabled="!jsonInput.trim()">
          生成星星
        </el-button>
        <el-button @click="clearInput">清空</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useCanvasStore } from '@/stores/canvas'

const canvasStore = useCanvasStore()

// 响应式数据
const jsonInput = ref('')
const jsonError = ref('')

// 示例数据
const exampleData = `{
  "points": [
    {"id": 1, "x": 0.21, "y": 0.25},
    {"id": 2, "x": 0.2838, "y": 0.2817},
    {"id": 3, "x": 0.1, "y": 0.4428},
    {"id": 4, "x": 0.425, "y": 0.526},
    {"id": 5, "x": 0.3387, "y": 0.7812},
    {"id": 6, "x": 0.3925, "y": 0.85},
    {"id": 7, "x": 0.705, "y": 0.593},
    {"id": 8, "x": 0.6675, "y": 0.7324},
    {"id": 9, "x": 0.7838, "y": 0.6183},
    {"id": 10, "x": 0.9, "y": 0.6681}
  ],
  "connections": [[1, 2], [2, 3], [2, 4], [4, 5], [4, 6], [4, 7], [7, 8], [8, 9], [7, 9], [9, 10]]
}`

const validateJSON = (jsonStr) => {
  try {
    const data = JSON.parse(jsonStr)
    
    if (!data || typeof data !== 'object') {
      return '数据必须是对象格式'
    }

    if (!Array.isArray(data.points)) {
      return '数据必须包含 points 数组'
    }

    if (!Array.isArray(data.connections)) {
      return '数据必须包含 connections 数组'
    }

    // 验证 points
    for (let i = 0; i < data.points.length; i++) {
      const point = data.points[i]
      if (typeof point.id !== 'number') {
        return `points[${i}] 缺少有效的 id`
      }
      if (typeof point.x !== 'number' || typeof point.y !== 'number') {
        return `points[${i}] 缺少有效的 x 或 y 坐标`
      }
    }

    // 验证 connections
    for (let i = 0; i < data.connections.length; i++) {
      const conn = data.connections[i]
      if (!Array.isArray(conn) || conn.length !== 2) {
        return `connections[${i}] 格式错误，应为 [id1, id2] 格式`
      }
      if (typeof conn[0] !== 'number' || typeof conn[1] !== 'number') {
        return `connections[${i}] 中的 id 必须是数字`
      }
      // 验证连接的点是否存在
      const pointIds = data.points.map(p => p.id)
      if (!pointIds.includes(conn[0]) || !pointIds.includes(conn[1])) {
        return `connections[${i}] 引用了不存在的点 id`
      }
    }

    return null
  } catch (error) {
    return 'JSON 格式错误'
  }
}

const generateStars = () => {
  const error = validateJSON(jsonInput.value)
  if (error) {
    jsonError.value = error
    ElMessage.error(error)
    return
  }
  
  jsonError.value = ''
  
  try {
    const data = JSON.parse(jsonInput.value)
    // 转换 points 中的相对坐标为绝对坐标
    const convertedPoints = canvasStore.convertRelativeToAbsolute(data.points)
    // 传递 points 和 connections 给 store
    canvasStore.setStars(convertedPoints, data.connections)
    ElMessage.success(`成功生成 ${data.points.length} 个星星`)
  } catch (error) {
    ElMessage.error('生成星星失败')
  }
}

const clearInput = () => {
  jsonInput.value = ''
  jsonError.value = ''
  canvasStore.clearCanvas()
}

const loadExample = () => {
  jsonInput.value = exampleData
  jsonError.value = ''
}

// 监听JSON输入变化，实时验证
watch(jsonInput, (newValue) => {
  if (newValue.trim()) {
    jsonError.value = validateJSON(newValue) || ''
  } else {
    jsonError.value = ''
  }
})

// 监听星星数据变化，当画布被清空时，同时清空输入框
watch(() => canvasStore.stars, (newStars) => {
  if (newStars.length === 0 && jsonInput.value.trim()) {
    jsonInput.value = ''
    jsonError.value = ''
  }
})
</script>

<style scoped>
.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 15px;
  border-bottom: 2px solid var(--el-color-primary);
  padding-bottom: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}

.section-title:hover {
  color: var(--el-color-primary);
}

.json-input-section {
  margin-bottom: 15px;
}

.input-error {
  border-color: #f56c6c !important;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}
</style>

