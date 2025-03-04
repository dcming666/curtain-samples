<template>
  <div class="category-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h1 v-if="currentCategory">{{ currentCategory.name }}</h1>
          <h1 v-else>分类浏览</h1>
          <el-button @click="goBack" icon="el-icon-arrow-left">返回首页</el-button>
        </div>
      </el-col>
    </el-row>
    
    <!-- 加载状态 -->
    <div v-if="curtainStore.loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="curtainStore.error" class="error-message">
      <el-alert :title="curtainStore.error" type="error" show-icon />
    </div>
    
    <!-- 窗帘样本列表 -->
    <div v-else>
      <div v-if="curtainStore.curtains.length === 0" class="empty-state">
        <el-empty description="该分类下暂无窗帘样本" />
      </div>
      <div v-else class="curtain-grid">
        <el-card 
          v-for="curtain in curtainStore.curtains" 
          :key="curtain.id"
          class="curtain-card"
          :body-style="{ padding: '0px' }"
          shadow="hover"
          @click="navigateToCurtain(curtain.id)"
        >
          <img :src="curtain.image_url" class="curtain-image">
          <div class="curtain-info">
            <h3>{{ curtain.name }}</h3>
            <p>{{ curtain.description }}</p>
            <div class="curtain-tags">
              <el-tag size="small" type="success" v-if="curtain.in_stock">有库存</el-tag>
              <el-tag size="small" type="danger" v-else>缺货</el-tag>
              <el-tag size="small" type="warning" v-if="curtain.is_new">新品</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCurtainStore } from '../stores'

export default {
  name: 'CategoryList',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const curtainStore = useCurtainStore()
    
    // 当前分类ID
    const categoryId = computed(() => route.params.id)
    
    // 当前分类信息
    const currentCategory = computed(() => {
      if (!categoryId.value || !curtainStore.categories.length) return null
      return curtainStore.categories.find(c => c.id == categoryId.value) || null
    })
    
    onMounted(async () => {
      // 获取分类列表（如果尚未加载）
      if (!curtainStore.categories.length) {
        await curtainStore.fetchCategories()
      }
      
      // 获取当前分类下的窗帘样本
      if (categoryId.value) {
        await curtainStore.fetchCurtainsByCategory(categoryId.value)
      }
    })
    
    const navigateToCurtain = (curtainId) => {
      router.push({ name: 'CurtainDetail', params: { id: curtainId } })
    }
    
    const goBack = () => {
      router.push({ name: 'Home' })
    }
    
    return {
      curtainStore,
      currentCategory,
      navigateToCurtain,
      goBack
    }
  }
}
</script>

<style scoped>
.category-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
}

.curtain-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.curtain-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.curtain-card:hover {
  transform: translateY(-5px);
}

.curtain-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.curtain-info {
  padding: 15px;
}

.curtain-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
}

.curtain-info p {
  margin: 0 0 10px 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.curtain-tags {
  display: flex;
  gap: 5px;
}

.loading-container {
  padding: 20px;
}

.error-message {
  margin: 20px 0;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}
</style>