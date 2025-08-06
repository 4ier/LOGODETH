# 🚄 Railway部署快速指南

最低成本方案：使用Railway免费套餐 + OpenRouter按需付费

## 💰 成本说明
- **Railway**: $5免费额度/月
- **OpenRouter**: 按实际使用付费，Gemini Pro Vision约$0.0003/logo
- **预计月成本**: $0-3（1000次识别以内）

## 🚀 一键部署

### 1. 准备OpenRouter API Key
```bash
# 注册OpenRouter并获取API Key
# https://openrouter.ai/keys
```

### 2. 部署到Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/DDKHTX)

或者手动部署：

```bash
# 1. Fork此仓库到你的GitHub
# 2. 在Railway中连接你的GitHub仓库
# 3. 设置环境变量：
LOGODETH_OPENAI_API_KEY=sk-or-v1-your-openrouter-key
```

### 3. 验证部署
```bash
# 部署完成后测试
curl https://your-app.railway.app/health

# 测试logo识别
curl -X POST https://your-app.railway.app/api/v1/recognize \
  -F "file=@your-logo.jpg"
```

## ⚙️ 环境变量配置

Railway会自动使用以下配置：

| 变量 | 值 | 说明 |
|------|------|------|
| `LOGODETH_USE_OPENROUTER` | `true` | 启用OpenRouter |
| `LOGODETH_OPENAI_MODEL` | `google/gemini-pro-vision` | 成本优化模型 |
| `LOGODETH_CACHE_TTL` | `172800` | 48小时缓存 |
| `LOGODETH_OPENAI_API_KEY` | `sk-or-v1-...` | **需要手动设置** |

## 🔧 成本优化配置

### 开发/测试环境
```env
LOGODETH_OPENAI_MODEL=google/gemini-pro-vision  # $0.25/1M tokens
```

### 生产环境
```env
LOGODETH_OPENAI_MODEL=openai/gpt-4o  # $5/1M tokens，更准确
```

### 极低成本
```env
LOGODETH_OPENAI_MODEL=haotian-liu/llava-13b  # 免费开源模型
```

## 📊 成本预测

| 月使用量 | Railway成本 | AI成本 | 总成本 |
|----------|-------------|--------|--------|
| 100次识别 | $0 | $0.03 | $0.03 |
| 500次识别 | $0 | $0.15 | $0.15 |
| 1000次识别 | $0-2 | $0.30 | $0.30-2.30 |
| 5000次识别 | $3-5 | $1.50 | $4.50-6.50 |

## 🔄 升级路径

### 当Railway免费额度不够时
1. **Railway Pro**: $5/月，无额度限制
2. **迁移到VPS**: 使用 `scripts/deploy-vps.sh`

### 当需要更高准确率时
```bash
# 在Railway环境变量中修改
LOGODETH_OPENAI_MODEL=openai/gpt-4o
```

## 🚨 故障排除

### 部署失败
```bash
# 检查构建日志
railway logs --deployment
```

### API调用失败
```bash
# 检查环境变量
railway variables

# 验证OpenRouter key
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer sk-or-v1-your-key"
```

### 超出额度
```bash
# 检查Railway使用情况
railway status

# 检查OpenRouter使用情况
# https://openrouter.ai/activity
```

## 📈 监控与告警

Railway提供内置监控，可在Dashboard查看：
- CPU/内存使用率
- 请求量统计
- 错误率监控
- 成本追踪

## 🎯 生产就绪检查清单

- [ ] OpenRouter API Key已配置
- [ ] 健康检查正常 (`/health`)
- [ ] 缓存配置生效（48小时TTL）
- [ ] CORS配置允许你的域名
- [ ] 日志级别设为INFO
- [ ] 监控告警已设置

---

**💡 提示**: 部署完成后，建议先用Gemini Pro Vision测试功能，确认无误后再考虑升级到更准确的模型！