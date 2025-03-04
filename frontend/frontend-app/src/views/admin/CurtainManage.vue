<template>
  <div class="curtain-manage-container">
    <div class="page-header">
      <h2>窗帘样本管理</h2>
      <el-button type="primary" @click="showAddDialog">添加新样本</el-button>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="样本名称">
          <el-input v-model="filterForm.name" placeholder="输入名称关键词" clearable />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filterForm.category_id" placeholder="选择分类" clearable>
            <el-option 
              v-for="category in curtainStore.categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="库存状态">
          <el-select v-model="filterForm.in_stock" placeholder="库存状态" clearable>
            <el-option label="有库存" :value="true" />
            <el-option label="缺货" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据表格 -->
    <el-card class="table-card">
      <div v-if="curtainStore.loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="curtainStore.error" class="error-message">
        <el-alert :title="curtainStore.error" type="error" show-icon />
      </div>
      <div v-else>
        <el-table 
          :data="curtainStore.curtains" 
          border 
          style="width: 100%"
          v-loading="tableLoading"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column label="图片" width="120">
            <template #default="{row}">
              <el-image 
                :src="row.image_url" 
                style="width: 80px; height: 80px"
                fit="cover"
                :preview-src-list="[row.image_url]"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><picture-failed /></el-icon>
                  </div>
                </template>
              </el-image>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="category_name" label="分类" width="120" />
          <el-table-column label="库存状态" width="100">
            <template #default="{row}">
              <el-tag :type="row.in_stock ? 'success' : 'danger'">
                {{ row.in_stock ? '有库存' : '缺货' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="新品" width="80">
            <template #default="{row}">
              <el-tag v-if="row.is_new" type="warning">新品</el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{row}">
              <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
              <el-popconfirm 
                title="确定要删除这个窗帘样本吗？" 
                @confirm="handleDelete(row.id)"
              >
                <template #reference>
                  <el-button size="small" type="danger">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      :title="dialogType === 'add' ? '添加窗帘样本' : '编辑窗帘样本'" 
      v-model="dialogVisible"
      width="600px"
    >
      <el-form 
        ref="curtainFormRef" 
        :model="curtainForm" 
        :rules="curtainRules" 
        label-width="100px"
      >
        <el-form-item label="样本名称" prop="name">
          <el-input v-model="curtainForm.name" placeholder="请输入窗帘样本名称" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="curtainForm.category_id" placeholder="请选择分类">
            <el-option 
              v-for="category in curtainStore.categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="样本图片" prop="image">
          <el-upload
            class="image-upload"
            action="#"
            :http-request="handleImageUpload"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
          >
            <img v-if="imageUrl" :src="imageUrl" class="preview-image" />
            <el-icon v-else class="upload-icon"><plus /></el-icon>
            <div class="upload-text">点击上传图片</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="curtainForm.price" :precision="2" :step="10" :min="0" />
        </el-form-item>
        <el-form-item label="材质" prop="material">
          <el-input v-model="curtainForm.material" placeholder="请输入窗帘材质" />
        </el-form-item>
        <el-form-item label="宽度" prop="width">
          <el-input v-model="curtainForm.width" placeholder="请输入窗帘宽度" />
        </el-form-item>
        <el-form-item label="图案" prop="pattern">
          <el-input v-model="curtainForm.pattern" placeholder="请输入窗帘图案" />
        </el-form-item>
        <el-form-item label="风格" prop="style">
          <el-input v-model="curtainForm.style" placeholder="请输入窗帘风格" />
        </el-form-item>
        <el-form-item label="功能" prop="features">
          <el-input v-model="curtainForm.features" placeholder="请输入窗帘功能特点" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="curtainForm.description" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入窗帘样本描述"
          />
        </el-form-item>
        <el-form-item label="库存状态" prop="in_stock">
          <el-switch v-model="curtainForm.in_stock" />
        </el-form-item>
        <el-form-item label="新品" prop="is_new">
          <el-switch v-model="curtainForm.is_new" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useCurtainStore } from '../../stores'
import { ElMessage } from 'element-plus'

export default {
  name: 'CurtainManage',
  setup() {
    const curtainStore = useCurtainStore()
    const curtainFormRef = ref(null)
    const dialogVisible = ref(false)
    const dialogType = ref('add') // 'add' 或 'edit'
    const submitLoading = ref(false)
    const tableLoading = ref(false)
    const imageUrl = ref('')
    const imageFile = ref(null)
    
    // 筛选表单
    const filterForm = reactive({
      name: '',
      category_id: '',
      in_stock: ''
    })
    
    // 窗帘样本表单
    const curtainForm = reactive({
      id: null,
      name: '',
      category_id: '',
      price: 0,
      material: '',
      width: '',
      pattern: '',
      style: '',
      features: '',
      description: '',
      in_stock: true,
      is_new: false
    })
    
    // 表单验证规则
    const curtainRules = {
      name: [
        { required: true, message: '请输入窗帘样本名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度应为2-50个字符', trigger: 'blur' }
      ],
      category_id: [
        { required: true, message: '请选择分类', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入窗帘样本描述', trigger: 'blur' }
      ]
    }
    
    // 初始化数据
    onMounted(async () => {
      // 获取分类列表
      if (!curtainStore.categories.length) {
        await curtainStore.fetchCategories()
      }
      // 获取窗帘样本列表
      await curtainStore.fetchCurtains()
    })
    
    // 显示添加对话框
    const showAddDialog = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 显示编辑对话框
    const showEditDialog = (row) => {
      dialogType.value = 'edit'
      resetForm()
      
      // 填充表单数据
      Object.keys(curtainForm).forEach(key => {
        if (key in row) {
          curtainForm[key] = row[key]
        }
      })
      
      // 设置图片预览
      if (row.image_url) {
        imageUrl.value = row.image_url
      }
      
      dialogVisible.value = true
    }
    
    // 重置表单
    const resetForm = () => {
      if (curtainFormRef.value) {
        curtainFormRef.value.resetFields()
      }
      
      // 重置表单数据
      Object.assign(curtainForm, {
        id: null,
        name: '',
        category_id: '',
        price: 0,
        material: '',
        width: '',
        pattern: '',
        style: '',
        features: '',
        description: '',
        in_stock: true,
        is_new: false
      })
      
      // 清除图片
      imageUrl.value = ''
      imageFile.value = null
    }
    
    // 图片上传前的验证
    const beforeImageUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2
      
      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过2MB!')
        return false
      }
      
      return true
    }
    
    // 处理图片上传
    const handleImageUpload = (options) => {
      const file = options.file
      imageFile.value = file
      
      // 创建本地预览URL
      const reader = new FileReader()
      reader.onload = (e) => {
        imageUrl.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
    
    // 提交表单
    const handleSubmit = async () => {
      if (!curtainFormRef.value) return
      
      await curtainFormRef.value.validate(async (valid) => {
        if (valid) {
          submitLoading.value = true
          
          try {
            // 创建FormData对象
            const formData = new FormData()
            
            // 添加表单字段
            Object.keys(curtainForm).forEach(key => {
              if (key !== 'id') {
                formData.append(key, curtainForm[key])
              }
            })
            
            // 添加图片文件（如果有）
            if (imageFile.value) {
              formData.append('image', imageFile.value)
            }
            
            // 根据对话框类型执行添加或更新操作
            if (dialogType.value === 'add') {
              await curtainStore.addCurtain(formData)
              ElMessage.success('添加窗帘样本成功')
            } else {
              await curtainStore.updateCurtain(curtainForm.id, formData)
              ElMessage.success('更新窗帘样本成功')
            }
            
            // 关闭对话框并重置表单
            dialogVisible.value = false
            resetForm()
          } catch (error) {
            ElMessage.error(error.message || '操作失败')
          } finally {
            submitLoading.value = false
          }
        }
      })
    }
    
    // 处理删除
    const handleDelete = async (id) => {
      try {
        tableLoading.value = true
        await curtainStore.deleteCurtain(id)
        ElMessage.success('删除窗帘样本成功')
      } catch (error) {
        ElMessage.error(error.message || '删除失败')
      } finally {
        tableLoading.value = false
      }
    }
    
    // 处理筛选
    const handleFilter = async () => {
      // 这里简化处理，实际应该调用API进行筛选
      // 在真实环境中，应该将筛选条件传递给后端API
      tableLoading.value = true
      try {
        await curtainStore.fetchCurtains()
        // 前端筛选（临时方案）
        if (filterForm.name) {
          curtainStore.curtains = curtainStore.curtains.filter(item => 
            item.name.toLowerCase().includes(filterForm.name.toLowerCase())
          )
        }
        if (filterForm.category_id) {
          curtainStore.curtains = curtainStore.curtains.filter(item => 
            item.category_id === filterForm.category_id
          )
        }
        if (filterForm.in_stock !== '') {
          curtainStore.curtains = curtainStore.curtains.filter(item => 
            item.in_stock === filterForm.in_stock
          )
        }
      } catch (error) {
        ElMessage.error('筛选失败: ' + error.message)
      } finally {
        tableLoading.value = false
      }
    }
    
    // 重置筛选
    const resetFilter = () => {
      Object.assign(filterForm, {
        name: '',
        category_id: '',
        in_stock: ''
      })
      curtainStore.fetchCurtains()
    }
    
    return {
      curtainStore,
      curtainForm,
      curtainRules,
      curtainFormRef,
      dialogVisible,
      dialogType,
      submitLoading,
      tableLoading,
      imageUrl,
      filterForm,
      showAddDialog,
      showEditDialog,
      handleSubmit,
      handleDelete,
      handleFilter,
      resetFilter,
      beforeImageUpload,
      handleImageUpload
    }
  }
}
</script>

<style scoped>
.curtain-manage-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
}

.table-card {
  margin-bottom: 20px;
}

.image-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.image-upload:hover {
  border-color: #409EFF;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-icon {
  font-size: 28px;
  color: #8c939d;
}

.upload-text {
  color: #8c939d;
  font-size: 14px;
  margin-top: 8px;
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
}
</style>