<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h1>窗帘样本展示</h1>
          <p>浏览我们的精选窗帘样本，为您的家居空间增添美感</p>
        </div>
      </el-col>
    </el-row>
    
    <!-- 分类导航 -->
    <el-row :gutter="20" class="category-nav">
      <el-col :span="24">
        <h2>窗帘分类</h2>
        <div v-if="curtainStore.loading" class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>
        <div v-else-if="curtainStore.error" class="error-message">
          <el-alert :title="curtainStore.error" type="error" show-icon />
        </div>
        <div v-else class="category-list">
          <el-button 
            v-for="category in curtainStore.categories" 
            :key="category.id"
            type="primary"
            plain
            @click="navigateToCategory(category.id)"
          >
            {{ category.name }}
          </el-button>
        </div>
      </el-col>
    </el-row>
    
    <!-- 最新样本展示 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <h2>最新样本</h2>
        <div v-if="curtainStore.loading" class="loading-container">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="curtainStore.error" class="error-message">
          <el-alert :title="curtainStore.error" type="error" show-icon />
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
                <el-tag size="small" type="info">{{ curtain.category_name }}</el-tag>
                <el-tag size="small" type="success" v-if="curtain.in_stock">有库存</el-tag>
                <el-tag size="small" type="danger" v-else>缺货</el-tag>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCurtainStore } from '../stores'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    const curtainStore = useCurtainStore()
    
    onMounted(async () => {
      // 获取分类列表
      await curtainStore.fetchCategories()
      // 获取窗帘样本列表
      await curtainStore.fetchCurtains()
    })
    
    const navigateToCategory = (categoryId) => {
      router.push({ name: 'CategoryList', params: { id: categoryId } })
    }
    
    const navigateToCurtain = (curtainId) => {
      router.push({ name: 'CurtainDetail', params: { id: curtainId } })
    }
    
    return {
      curtainStore,
      navigateToCategory,
      navigateToCurtain
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.category-nav {
  margin-bottom: 40px;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
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
</style>