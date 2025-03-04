import { defineStore } from 'pinia'
import axios from 'axios'

// 定义API基础URL
const API_URL = 'http://localhost:5000/api'

// 窗帘样本状态管理
export const useCurtainStore = defineStore('curtain', {
  state: () => ({
    curtains: [],
    categories: [],
    currentCurtain: null,
    loading: false,
    error: null
  }),
  
  actions: {
    // 获取所有窗帘样本
    async fetchCurtains() {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/curtains`)
        this.curtains = response.data
        this.error = null
      } catch (err) {
        this.error = '获取窗帘样本失败: ' + err.message
        console.error('获取窗帘样本失败:', err)
      } finally {
        this.loading = false
      }
    },
    
    // 获取单个窗帘样本详情
    async fetchCurtainById(id) {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/curtains/${id}`)
        this.currentCurtain = response.data
        this.error = null
      } catch (err) {
        this.error = '获取窗帘样本详情失败: ' + err.message
        console.error('获取窗帘样本详情失败:', err)
      } finally {
        this.loading = false
      }
    },
    
    // 获取所有分类
    async fetchCategories() {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/categories`)
        this.categories = response.data
        this.error = null
      } catch (err) {
        this.error = '获取分类失败: ' + err.message
        console.error('获取分类失败:', err)
      } finally {
        this.loading = false
      }
    },
    
    // 获取分类下的窗帘样本
    async fetchCurtainsByCategory(categoryId) {
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/categories/${categoryId}/curtains`)
        this.curtains = response.data
        this.error = null
      } catch (err) {
        this.error = '获取分类窗帘样本失败: ' + err.message
        console.error('获取分类窗帘样本失败:', err)
      } finally {
        this.loading = false
      }
    },
    
    // 添加窗帘样本（管理员功能）
    async addCurtain(curtainData) {
      this.loading = true
      try {
        const response = await axios.post(`${API_URL}/curtains`, curtainData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        this.curtains.push(response.data)
        this.error = null
        return response.data
      } catch (err) {
        this.error = '添加窗帘样本失败: ' + err.message
        console.error('添加窗帘样本失败:', err)
        throw err
      } finally {
        this.loading = false
      }
    },
    
    // 更新窗帘样本（管理员功能）
    async updateCurtain(id, curtainData) {
      this.loading = true
      try {
        const response = await axios.put(`${API_URL}/curtains/${id}`, curtainData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        
        // 更新本地数据
        const index = this.curtains.findIndex(c => c.id === id)
        if (index !== -1) {
          this.curtains[index] = response.data
        }
        if (this.currentCurtain && this.currentCurtain.id === id) {
          this.currentCurtain = response.data
        }
        
        this.error = null
        return response.data
      } catch (err) {
        this.error = '更新窗帘样本失败: ' + err.message
        console.error('更新窗帘样本失败:', err)
        throw err
      } finally {
        this.loading = false
      }
    },
    
    // 删除窗帘样本（管理员功能）
    async deleteCurtain(id) {
      this.loading = true
      try {
        await axios.delete(`${API_URL}/curtains/${id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
          }
        })
        
        // 从本地数据中移除
        this.curtains = this.curtains.filter(c => c.id !== id)
        if (this.currentCurtain && this.currentCurtain.id === id) {
          this.currentCurtain = null
        }
        
        this.error = null
        return true
      } catch (err) {
        this.error = '删除窗帘样本失败: ' + err.message
        console.error('删除窗帘样本失败:', err)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})

// 用户认证状态管理
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || null,
    user: null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    // 管理员登录
    async login(credentials) {
      this.loading = true
      try {
        const response = await axios.post(`${API_URL}/auth/login`, credentials)
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('admin_token', this.token)
        this.error = null
        return true
      } catch (err) {
        this.error = '登录失败: ' + err.message
        console.error('登录失败:', err)
        return false
      } finally {
        this.loading = false
      }
    },
    
    // 管理员登出
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('admin_token')
    },
    
    // 获取当前用户信息
    async fetchCurrentUser() {
      if (!this.token) return null
      
      this.loading = true
      try {
        const response = await axios.get(`${API_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })
        this.user = response.data
        this.error = null
        return this.user
      } catch (err) {
        this.error = '获取用户信息失败: ' + err.message
        console.error('获取用户信息失败:', err)
        // 如果是401错误，清除token
        if (err.response && err.response.status === 401) {
          this.logout()
        }
        return null
      } finally {
        this.loading = false
      }
    }
  }
})