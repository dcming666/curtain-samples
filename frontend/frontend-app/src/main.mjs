import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

// 创建Vue应用实例
const app = createApp(App)

// 使用插件
app.use(createPinia()) // 状态管理
app.use(router) // 路由
app.use(ElementPlus) // UI组件库

// 挂载应用
app.mount('#app')
