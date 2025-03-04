import { createRouter, createWebHistory } from 'vue-router'

// 导入页面组件
const Home = () => import('../views/Home.vue')
const CurtainDetail = () => import('../views/CurtainDetail.vue')
const CategoryList = () => import('../views/CategoryList.vue')
const Admin = () => import('../views/admin/Admin.vue')
const Login = () => import('../views/admin/Login.vue')
const CurtainManage = () => import('../views/admin/CurtainManage.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页 - 窗帘样本展示' }
  },
  {
    path: '/category/:id',
    name: 'CategoryList',
    component: CategoryList,
    meta: { title: '分类浏览 - 窗帘样本展示' }
  },
  {
    path: '/curtain/:id',
    name: 'CurtainDetail',
    component: CurtainDetail,
    meta: { title: '样本详情 - 窗帘样本展示' }
  },
  {
    path: '/admin/login',
    name: 'Login',
    component: Login,
    meta: { title: '管理员登录' }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { title: '后台管理', requiresAuth: true },
    children: [
      {
        path: 'curtains',
        name: 'CurtainManage',
        component: CurtainManage,
        meta: { title: '窗帘样本管理', requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局路由守卫，处理页面标题和身份验证
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 检查是否需要身份验证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    const isLoggedIn = localStorage.getItem('admin_token')
    if (!isLoggedIn) {
      // 如果没有登录，重定向到登录页面
      next({ name: 'Login' })
    } else {
      next() // 已登录，继续导航
    }
  } else {
    next() // 不需要身份验证，继续导航
  }
})

export default router