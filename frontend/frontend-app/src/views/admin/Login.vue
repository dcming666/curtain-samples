<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>管理员登录</h2>
          <p>窗帘样本管理系统</p>
        </div>
      </template>
      
      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="loginRules" 
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <!-- 用户名输入框 -->
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="el-icon-user"
            placeholder="请输入管理员用户名"
            clearable
          />
        </el-form-item>
        
        <!-- 密码输入框 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password" 
            prefix-icon="el-icon-lock"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        
        <!-- 错误信息提示 -->
        <div v-if="authStore.error" class="login-error">
          <el-alert :title="authStore.error" type="error" show-icon />
        </div>
        
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="authStore.loading"
            class="login-button"
          >
            登录
          </el-button>
        </el-form-item>
        
        <!-- 返回前台链接 -->
        <div class="back-to-home">
          <router-link :to="{name: 'Home'}">返回前台首页</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const loginFormRef = ref(null)
    
    // 登录表单数据
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    // 表单验证规则
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
      ]
    }
    
    // 处理登录
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      await loginFormRef.value.validate(async (valid) => {
        if (valid) {
          const success = await authStore.login(loginForm)
          if (success) {
            // 登录成功，跳转到管理后台
            router.push({ name: 'Admin' })
          }
        }
      })
    }
    
    return {
      loginForm,
      loginRules,
      loginFormRef,
      authStore,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  max-width: 90%;
}

.login-header {
  text-align: center;
}

.login-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #2c3e50;
}

.login-header p {
  margin: 5px 0 0;
  color: #7f8c8d;
  font-size: 1rem;
}

.login-button {
  width: 100%;
  margin-top: 10px;
}

.login-error {
  margin-bottom: 15px;
}

.back-to-home {
  text-align: center;
  margin-top: 15px;
}

.back-to-home a {
  color: #409eff;
  text-decoration: none;
}

.back-to-home a:hover {
  text-decoration: underline;
}
</style>