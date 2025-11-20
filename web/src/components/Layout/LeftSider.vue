<template>
  <aside class="left-sider">
    <div class="left-sidebar-content">
      <!-- 画布大小设置 -->
      <div class="section">
        <h3 class="section-title" @click="toggleCanvasConfig">
          <span>画布设置</span>
          <el-icon class="collapse-icon" :class="{ 'collapsed': !canvasConfigExpanded }">
            <ArrowDown v-if="canvasConfigExpanded" />
            <ArrowUp v-else />
          </el-icon>
        </h3>
        <div v-show="canvasConfigExpanded" class="canvas-size-options">
          <el-radio-group v-model="selectedAspectRatio" @change="handleAspectRatioChange">
            <el-radio value="9:16">竖屏 (9:16)</el-radio>
            <el-radio value="3:4">标准 (3:4)</el-radio>
            <el-radio value="1:1">正方形 (1:1)</el-radio>
            <el-radio value="auto">自适应</el-radio>
          </el-radio-group>
        </div>
      </div>

      <!-- 背景设置 -->
      <div class="section">
        <h3 class="section-title" @click="toggleBackgroundConfig">
          <span>背景设置</span>
          <el-icon class="collapse-icon" :class="{ 'collapsed': !backgroundConfigExpanded }">
            <ArrowDown v-if="backgroundConfigExpanded" />
            <ArrowUp v-else />
          </el-icon>
        </h3>
        <div v-show="backgroundConfigExpanded">
          <!-- 背景类型选择 -->
          <div class="background-type-selector">
            <el-radio-group v-model="backgroundType" @change="handleBackgroundTypeChange">
              <el-radio value="grid">空 (网格)</el-radio>
              <el-radio value="image">图片</el-radio>
              <el-radio value="color">纯色</el-radio>
            </el-radio-group>
          </div>

          <!-- 图片上传 -->
          <div v-if="backgroundType === 'image'" class="background-image-section">
            <el-upload
              class="image-uploader"
              :show-file-list="false"
              :on-success="handleImageSuccess"
              :before-upload="beforeImageUpload"
              action="#"
              :http-request="handleImageUpload"
            >
              <div class="upload-content">
                <img v-if="backgroundImageUrl && !imageUploading" :src="backgroundImageUrl" class="uploaded-image" />
                <el-icon v-else-if="!imageUploading" class="image-uploader-icon"><Plus /></el-icon>
                <div v-if="imageUploading" class="upload-loading">
                  <el-icon class="loading-icon"><Loading /></el-icon>
                  <span class="loading-text">上传中...</span>
                </div>
              </div>
            </el-upload>
            <div class="upload-tip">支持 JPG、PNG 格式，最大 5MB</div>
          </div>

          <!-- 纯色选择 -->
          <div v-if="backgroundType === 'color'" class="background-color-section">
            <span class="text-sm mx-2 style-label !inline">选择背景颜色</span>
            <el-color-picker v-model="backgroundColor" @change="handleBackgroundColorChange" />
          </div>
        </div>
      </div>

      <!-- 动态加载路由对应的配置组件 -->
      <component :is="routeComponent" v-if="routeComponent" />
    </div>
  </aside>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Plus, ArrowDown, ArrowUp, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useCanvasStore } from '@/stores/canvas'
import StarConf from '@/views/star/StarConf.vue'

const route = useRoute()
const canvasStore = useCanvasStore()

// 根据路由动态加载配置组件
const routeComponent = computed(() => {
  const path = route.path
  if (path === '/star-pattern' || path.startsWith('/star-pattern')) {
    return StarConf
  }
  return null
})

// 响应式数据
const selectedAspectRatio = ref('9:16')
const backgroundType = ref('grid')
const backgroundImageUrl = ref('')
const backgroundColor = ref('#ffffff')
const imageUploading = ref(false)

// 折叠状态 - 默认全部展开
const canvasConfigExpanded = ref(true)
const backgroundConfigExpanded = ref(true)

// 方法
const handleAspectRatioChange = (value) => {
  canvasStore.updateCanvasConfig({ aspectRatio: value })
}

const handleBackgroundTypeChange = (type) => {
  if (type === 'color') {
    // 切换到纯色时，设置默认背景色为 #2f303d
    backgroundColor.value = '#2f303d'
    canvasStore.updateBackgroundConfig({
      type: 'color',
      color: '#2f303d'
    })
  } else {
    canvasStore.updateBackgroundConfig({ type })
  }
  if (type !== 'image') {
    backgroundImageUrl.value = ''
    imageUploading.value = false
  }
}

const handleImageUpload = (options) => {
  const file = options.file
  const reader = new FileReader()
  
  // 开始上传，显示loading
  imageUploading.value = true

  reader.onload = (e) => {
    backgroundImageUrl.value = e.target.result
    canvasStore.updateBackgroundConfig({
      type: 'image',
      imageUrl: e.target.result
    })
    
    // 如果选择了自适应，更新画布尺寸
    if (selectedAspectRatio.value === 'auto') {
      const img = new Image()
      img.onload = () => {
        canvasStore.updateCanvasConfig({
          width: img.width,
          height: img.height
        })
        // 图片加载完成，隐藏loading
        imageUploading.value = false
      }
      img.onerror = () => {
        // 图片加载失败，隐藏loading
        imageUploading.value = false
        ElMessage.error('图片加载失败')
      }
      img.src = e.target.result
    } else {
      // 非自适应模式，直接隐藏loading
      imageUploading.value = false
    }
  }
  
  reader.onerror = () => {
    // 文件读取失败，隐藏loading
    imageUploading.value = false
    ElMessage.error('图片读取失败')
  }

  reader.readAsDataURL(file)
  return false // 阻止默认上传行为
}

const handleImageSuccess = () => {
  ElMessage.success('图片上传成功')
}

const beforeImageUpload = (file) => {
  const isValidType = file.type === 'image/jpeg' || file.type === 'image/png'
  const isValidSize = file.size / 1024 / 1024 < 5

  if (!isValidType) {
    ElMessage.error('只支持 JPG 和 PNG 格式的图片')
    return false
  }
  if (!isValidSize) {
    ElMessage.error('图片大小不能超过 5MB')
    return false
  }
  return true
}

const handleBackgroundColorChange = (color) => {
  console.log(color)
  canvasStore.updateBackgroundConfig({
    type: 'color',
    color: color
  })
}


// 折叠切换方法
const toggleCanvasConfig = () => {
  canvasConfigExpanded.value = !canvasConfigExpanded.value
}

const toggleBackgroundConfig = () => {
  backgroundConfigExpanded.value = !backgroundConfigExpanded.value
}

// 监听背景配置变化，同步到本地状态
watch(() => canvasStore.backgroundConfig, (newConfig) => {
  backgroundType.value = newConfig.type
  backgroundImageUrl.value = newConfig.imageUrl || ''
  backgroundColor.value = newConfig.color || '#ffffff'
}, { deep: true })

// 初始化
canvasStore.updateCanvasConfig({ aspectRatio: selectedAspectRatio.value })
canvasStore.updateBackgroundConfig({ type: backgroundType.value })
</script>

<style scoped>
.left-sider {
  width: 350px;
  background: white;
  border-right: 1px solid #e4e7ed;
  overflow-y: auto;
}

.left-sidebar-content {
  padding: 20px;
}

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

.collapse-icon {
  font-size: 14px;
  color: #909399;
  transition: transform 0.3s, color 0.2s;
}

.section-title:hover .collapse-icon {
  color: var(--el-color-primary);
}

.canvas-size-options {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 10px;
}

.background-type-selector {
  margin-bottom: 15px;
  display: flex;
  flex-direction: row;
}

.background-image-section {
  margin-top: 15px;
}

.image-uploader {
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.image-uploader:hover {
  border-color: var(--el-color-primary);
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 309px;
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-content {
  position: relative;
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.uploaded-image {
  /* width: 309px; */
  height: 120px;
  object-fit: cover;
  display: block;
}

.upload-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
}

.loading-icon {
  font-size: 32px;
  color: var(--el-color-primary);
  animation: rotating 2s linear infinite;
}

.loading-text {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.upload-tip {
  font-size: 12px;
  color: #606266;
  margin-top: 8px;
}

.background-color-section {
  margin-top: 15px;
}


:deep(.el-radio) {
  margin-bottom: 0;
  margin-right: 15px;
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

:deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

:deep(.el-upload:hover) {
  border-color: var(--el-color-primary);
}
</style>
