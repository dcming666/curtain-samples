import { defineStore } from 'pinia'

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
        const response = await fetch('/data/curtains.json')
        const data = await response.json()
        this.curtains = data.curtains
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
        const response = await fetch('/data/curtains.json')
        const data = await response.json()
        this.currentCurtain = data.curtains.find(c => c.id === id)
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
        const response = await fetch('/data/curtains.json')
        const data = await response.json()
        this.categories = data.categories
        this.error = null
      } catch (err) {
        this.error = '获取分类失败: ' + err.message
        console.error('获取分类失败:', err)
      } finally {
        this.loading = false
      }
    }
  }
})