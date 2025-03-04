<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <el-header class="admin-header">
      <div class="logo">
        <h1>窗帘样本管理系统</h1>
      </div>
      <div class="user-info">
        <span v-if="authStore.user">{{ authStore.user.username }}</span>
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="32" icon="el-icon-user" />
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container class="main-container">
      <!-- 侧边栏导航 -->
      <el-aside width="200px" class="admin-aside">
        <el-menu
          :router="true"
          :default-active="activeMenu"
          class="admin-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/admin/curtains">
            <el-icon><document /></el-icon>
            <span>窗帘样本管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/categories">
            <el-icon><folder /></el-icon>
            <span>分类管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区域 -->
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores'

export default {
  name: 'Admin',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    // 获取当前激活的菜单项
    const activeMenu = computed(() => route.path)
    
    // 组件挂载时获取用户信息
    onMounted(async () => {
      if (!authStore.user) {
        await authStore.fetchCurrentUser()
      }
    })
    
    // 处理下拉菜单命令
    const handleCommand = (command) => {
      if (command === 'logout') {
        authStore.logout()
        router.push({ name: 'Login' })
      }
    }
    
    return {
      authStore,
      activeMenu,
      handleCommand
    }
  }
}
</script>

<style scoped>
.admin-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo h1 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.admin-aside {
  background-color: #304156;
  height: 100%;
  overflow-y: auto;
}

.admin-menu {
  border-right: none;
}

.admin-main {
  padding: 20px;
  background-color: #f0f2f5;
  height: 100%;
  overflow-y: auto;
}
</style>