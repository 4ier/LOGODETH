# 🚄 LOGODETH Railway手动部署指南

由于CLI限制，这里是完整的手动部署步骤。

## 📋 部署准备

### 1. OpenRouter API Key
```bash
# 1. 访问 https://openrouter.ai
# 2. 注册账户并登录
# 3. 前往 https://openrouter.ai/keys
# 4. 创建新API Key（格式：sk-or-v1-...）
```

### 2. Railway账户准备
```bash
# 1. 访问 https://railway.app
# 2. 使用GitHub账户登录
# 3. 连接你的GitHub仓库
```

## 🚀 Railway部署步骤

### 步骤1: 创建新项目
1. 在Railway Dashboard点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你的 `LOGODETH` 仓库
4. 选择 `main` 分支

### 步骤2: 配置环境变量
在Railway项目的 **Variables** 标签页添加以下变量：

#### 必需变量
```env
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
```

#### 自动配置变量（Railway会自动设置）
```env
PORT=8000                    # Railway自动设置
REDIS_URL=redis://...        # 添加Redis服务时自动设置
RAILWAY_PUBLIC_DOMAIN=...    # Railway自动设置
SECRET_KEY=...               # Railway自动生成
```

### 步骤3: 添加Redis服务
1. 在项目中点击 **"+ New"**
2. 选择 **"Database"** → **"Add Redis"**
3. Redis服务会自动配置并设置 `REDIS_URL`

### 步骤4: 配置部署设置
Railway会自动检测以下配置文件：
- `railway.toml` - Railway部署配置
- `nixpacks.toml` - 构建配置
- `Dockerfile` - 容器配置（备用）

### 步骤5: 触发部署
1. 推送代码到GitHub仓库
2. Railway会自动触发构建和部署
3. 等待部署完成（约3-5分钟）

## ✅ 部署验证

### 检查部署状态
```bash
# 1. 在Railway Dashboard查看部署日志
# 2. 确认服务状态为 "Active"
# 3. 获取公共域名（格式：xxx.railway.app）
```

### 健康检查
```bash
# 替换 your-app.railway.app 为实际域名
curl https://your-app.railway.app/health
```

预期响应：
```json
{
  "status": "healthy",
  "timestamp": "2025-01-XX...",
  "version": "2.0.0",
  "environment": "production"
}
```

### 测试API端点
```bash
# 测试API文档
curl https://your-app.railway.app/docs

# 测试提供商信息
curl https://your-app.railway.app/api/v1/provider-info
```

## 📊 成本监控

### Railway使用量监控
1. 在Railway Dashboard查看 **"Metrics"** 标签
2. 监控CPU、内存、网络使用量
3. 跟踪月度成本

### OpenRouter使用量监控
1. 访问 https://openrouter.ai/activity
2. 查看API调用统计
3. 监控成本和使用量

## 🔧 故障排除

### 常见问题

#### 1. 部署失败
```bash
# 检查构建日志
# 常见问题：依赖安装失败、内存不足
```

**解决方案**：
- 检查 `requirements_multimodal.txt` 是否正确
- 确认Railway资源限制
- 查看详细错误日志

#### 2. 环境变量未设置
```bash
# 错误：KeyError: 'LOGODETH_OPENAI_API_KEY'
```

**解决方案**：
- 确认在Railway Variables中设置了 `OPENROUTER_API_KEY`
- 检查变量名称是否正确
- 重新部署应用

#### 3. Redis连接失败
```bash
# 错误：Redis connection refused
```

**解决方案**：
- 确保已添加Redis数据库服务
- 检查 `REDIS_URL` 是否正确设置
- 重启Redis服务

#### 4. API调用失败
```bash
# 错误：OpenRouter authentication failed
```

**解决方案**：
- 验证OpenRouter API Key格式（sk-or-v1-...）
- 检查OpenRouter账户余额
- 确认API Key权限

## 🚀 部署后优化

### 1. 配置自定义域名
```bash
# 在Railway项目设置中
# 1. 点击 "Settings" → "Domains"
# 2. 添加自定义域名
# 3. 配置DNS记录
```

### 2. 设置监控告警
```bash
# 在Railway Dashboard
# 1. 配置CPU/内存告警
# 2. 设置错误率监控
# 3. 启用日志告警
```

### 3. 优化成本
```bash
# 调整环境变量以降低成本
LOGODETH_OPENAI_MODEL=google/gemini-pro-vision  # 最低成本
LOGODETH_CACHE_TTL=259200                       # 3天缓存
LOGODETH_API_RATE_LIMIT=10                      # 限制请求频率
```

## 📈 扩展选项

### 升级到更好的模型
```bash
# 生产环境建议
LOGODETH_OPENAI_MODEL=openai/gpt-4o
```

### 添加备用服务
```bash
# 设置Anthropic作为备用
LOGODETH_ANTHROPIC_API_KEY=sk-ant-your-key
```

### 启用监控
```bash
# 可选：添加Sentry错误追踪
LOGODETH_SENTRY_DSN=https://...
```

---

## 📝 部署清单

- [ ] OpenRouter API Key已获取
- [ ] Railway项目已创建
- [ ] GitHub仓库已连接
- [ ] 环境变量已设置
- [ ] Redis服务已添加
- [ ] 部署成功完成
- [ ] 健康检查通过
- [ ] API测试通过
- [ ] 成本监控已启用

**🎉 部署完成！你的LOGODETH现在运行在 Railway 上，使用 OpenRouter 提供成本优化的AI服务。**