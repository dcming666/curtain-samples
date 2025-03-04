<template>
  <div class="detail-container">
    <div v-if="curtainStore.loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    <div v-else-if="curtainStore.error" class="error-message">
      <el-alert :title="curtainStore.error" type="error" show-icon />
      <el-button class="mt-4" type="primary" @click="goBack">返回上一页</el-button>
    </div>
    <div v-else-if="curtainStore.currentCurtain" class="curtain-detail">
      <el-row :gutter="30">
        <!-- 返回按钮 -->
        <el-col :span="24" class="mb-4">
          <el-button @click="goBack" icon="el-icon-arrow-left">返回</el-button>
        </el-col>
        
        <!-- 左侧图片区域 -->
        <el-col :xs="24" :sm="12" :md="10" :lg="8">
          <div class="image-container">
            <el-image 
              :src="curtainStore.currentCurtain.image_url" 
              fit="contain"
              :preview-src-list="[curtainStore.currentCurtain.image_url]"
              class="curtain-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><picture-failed /></el-icon>
                  <span>加载图片失败</span>
                </div>
              </template>
            </el-image>
          </div>
        </el-col>
        
        <!-- 右侧信息区域 -->
        <el-col :xs="24" :sm="12" :md="14" :lg="16">
          <div class="curtain-info">
            <h1 class="curtain-title">{{ curtainStore.currentCurtain.name }}</h1>
            
            <div class="curtain-meta">
              <el-tag size="medium" type="info">{{ curtainStore.currentCurtain.category_name }}</el-tag>
              <el-tag size="medium" type="success" v-if="curtainStore.currentCurtain.in_stock">有库存</el-tag>
              <el-tag size="medium" type="danger" v-else>缺货</el-tag>
              <el-tag size="medium" type="warning" v-if="curtainStore.currentCurtain.is_new">新品</el-tag>
            </div>
            
            <div class="curtain-price" v-if="curtainStore.currentCurtain.price">
              <span class="price-label">价格:</span>
              <span class="price-value">¥{{ curtainStore.currentCurtain.price.toFixed(2) }}</span>
              <span class="price-unit">/米</span>
            </div>
            
            <div class="curtain-specs">
              <h3>产品规格</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="材质">{{ curtainStore.currentCurtain.material || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="宽度">{{ curtainStore.currentCurtain.width || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="图案">{{ curtainStore.currentCurtain.pattern || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="风格">{{ curtainStore.currentCurtain.style || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="功能">{{ curtainStore.currentCurtain.features || '未提供' }}</el-descriptions-item>
              </el-descriptions>
            </div>
            
            <div class="curtain-description">
              <h3>产品描述</h3>
              <p>{{ curtainStore.currentCurtain.description }}</p>
            </div>
            
            <div class="contact-info">
              <h3>联系方式</h3>
              <p>如果您对这款窗帘样本感兴趣，请联系我们:</p>
              <p><el-icon><phone /></el-icon> 电话: 123-4567-8910</p>
              <p><el-icon><message /></el-icon> 邮箱: contact@curtainshop.com</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div v-else class="not-found">
      <el-empty description="未找到窗帘样本信息" />
      <el-button class="mt-4" type="primary" @click="goBack">返回上一页</el-button>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCurtainStore } from '../stores'

export default {
  name: 'CurtainDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const curtainStore = useCurtainStore()
    
    onMounted(async () => {
      const curtainId = route.params.id
      if (curtainId) {
        await curtainStore.fetchCurtainById(curtainId)
      }
    })
    
    const goBack = () => {
      router.back()
    }
    
    return {
      curtainStore,
      goBack
    }
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container, .error-message, .not-found {
  padding: 40px 0;
  text-align: center;
}

.image-container {
  background-color: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.curtain-image {
  width: 100%;
  height: 400px;
  object-fit: contain;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #909399;
}

.curtain-title {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0 0 15px 0;
}

.curtain-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.curtain-price {
  margin: 20px 0;
  font-size: 1.2rem;
}

.price-label {
  color: #606266;
}

.price-value {
  color: #f56c6c;
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0 5px;
}

.price-unit {
  color: #909399;
}

.curtain-specs, .curtain-description, .contact-info {
  margin-top: 30px;
}

.curtain-specs h3, .curtain-description h3, .contact-info h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}

.curtain-description p {
  line-height: 1.6;
  color: #606266;
}

.contact-info p {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 16px;
}
</style>