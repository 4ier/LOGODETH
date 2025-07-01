# LOGODETH 开发计划

## 项目概述

LOGODETH 是一个基于AI的金属乐队Logo识别引擎，通过爬取 Metal Archives 网站的数据，使用 CLIP 模型进行图像特征提取和相似度匹配，帮助用户识别难以辨认的金属乐队Logo。

## 技术架构

### 整体架构图
```
用户界面 (React/Vue) 
    ↓
API网关 (FastAPI)
    ↓
业务逻辑层
    ├── 图像处理服务
    ├── 特征提取服务 (CLIP)
    ├── 相似度匹配服务
    └── 数据管理服务
    ↓
数据存储层
    ├── 向量数据库 (Qdrant/Pinecone)
    ├── 关系数据库 (PostgreSQL)
    ├── 对象存储 (S3/MinIO)
    └── 缓存层 (Redis)
```

### 核心组件

1. **数据采集模块** (`scraper/`)
   - Metal Archives 爬虫
   - 图像下载器
   - 数据验证器
   - 速率限制器

2. **数据处理模块** (`processing/`)
   - 图像预处理管道
   - CLIP 特征提取器
   - 向量数据库操作

3. **API服务模块** (`backend/`)
   - RESTful API 接口
   - 图像上传处理
   - Logo 匹配算法
   - 结果排序和过滤

4. **前端界面** (`frontend/`)
   - 图像上传界面
   - 结果展示
   - 管理后台

## 详细开发计划

### Phase 1: 数据采集与基础设施 (第1-2周)

#### 1.1 Metal Archives 爬虫开发
**目标**: 从 Metal Archives 网站爬取乐队信息和Logo图片

**技术栈**: 
- `requests` + `BeautifulSoup` 用于网页解析
- `aiohttp` 用于异步请求
- `fake-useragent` 用于User-Agent轮换
- `tenacity` 用于重试机制

**实现细节**:
```python
# scraper/metal_archives_scraper.py
class MetalArchivesScraper:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.rate_limiter = RateLimiter(requests_per_second=1.5)
        
    async def scrape_band_list(self, start_page=1, max_pages=1000):
        """爬取乐队列表页面"""
        
    async def scrape_band_details(self, band_url):
        """爬取单个乐队详细信息"""
        
    async def download_logo(self, logo_url, band_name):
        """下载Logo图片"""
```

**数据结构**:
```json
{
    "band_id": "12345",
    "name": "Mayhem",
    "logo_url": "https://...",
    "logo_path": "data/raw_logos/mayhem_logo.jpg",
    "genre": "Black Metal",
    "country": "Norway",
    "formed_year": 1984,
    "status": "Active",
    "themes": ["Death", "Anti-Christianity"],
    "scraped_at": "2024-01-15T10:30:00Z"
}
```

#### 1.2 数据验证与清洗
**目标**: 确保爬取数据的质量和一致性

```python
# scraper/data_validator.py
class DataValidator:
    def validate_image(self, image_path):
        """验证图像文件完整性和格式"""
        
    def detect_duplicates(self, image_hash_db):
        """检测重复图像"""
        
    def filter_low_quality(self, min_resolution=(100, 100)):
        """过滤低质量图像"""
```

#### 1.3 基础设施搭建
- 数据库设计 (PostgreSQL)
- 对象存储配置 (MinIO/S3)
- Redis 缓存配置
- 日志系统配置

**数据库Schema**:
```sql
-- bands 表
CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    genre VARCHAR(100),
    country VARCHAR(100),
    formed_year INTEGER,
    status VARCHAR(50),
    logo_path VARCHAR(500),
    logo_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- logo_embeddings 表  
CREATE TABLE logo_embeddings (
    id SERIAL PRIMARY KEY,
    band_id INTEGER REFERENCES bands(id),
    embedding VECTOR(512),  -- 使用 pgvector 扩展
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Phase 2: 图像处理与AI管道 (第3-4周)

#### 2.1 图像预处理管道
**目标**: 标准化Logo图像，提高识别准确率

```python
# processing/logo_processor.py
class LogoProcessor:
    def __init__(self):
        self.target_size = (224, 224)
        self.background_remover = rembg.remove
        
    def preprocess_image(self, image_path):
        """图像预处理流水线"""
        # 1. 加载图像
        # 2. 背景移除
        # 3. 尺寸标准化
        # 4. 对比度增强
        # 5. 噪声去除
        
    def create_augmentations(self, image):
        """数据增强"""
        # 旋转、缩放、颜色变换等
```

#### 2.2 CLIP 特征提取
**目标**: 使用CLIP模型提取Logo的语义特征

```python
# processing/clip_embedder.py
class CLIPEmbedder:
    def __init__(self, model_name="ViT-B/32"):
        self.model = clip.load(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def embed_image(self, image_tensor):
        """提取单张图像的特征向量"""
        
    def batch_embed(self, image_paths, batch_size=32):
        """批量处理图像特征提取"""
        
    def embed_text(self, text_descriptions):
        """提取文本描述的特征向量"""
```

#### 2.3 向量数据库集成
**目标**: 高效存储和检索图像特征向量

```python
# processing/vector_db.py
class VectorDatabase:
    def __init__(self, db_type="qdrant"):
        if db_type == "qdrant":
            self.client = QdrantClient(host="localhost", port=6333)
        elif db_type == "pinecone":
            self.client = pinecone.init()
            
    def create_collection(self, collection_name, vector_size=512):
        """创建向量集合"""
        
    def insert_vectors(self, vectors, metadata):
        """批量插入向量"""
        
    def search_similar(self, query_vector, top_k=10):
        """相似度搜索"""
```

### Phase 3: 后端API开发 (第5-6周)

#### 3.1 FastAPI 服务架构
**目标**: 构建高性能的API服务

```python
# backend/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LOGODETH API", version="1.0.0")

@app.post("/api/v1/recognize")
async def recognize_logo(file: UploadFile = File(...)):
    """Logo识别接口"""
    
@app.get("/api/v1/bands/{band_id}")
async def get_band_info(band_id: int):
    """获取乐队信息"""
    
@app.get("/api/v1/stats")
async def get_statistics():
    """获取系统统计信息"""
```

#### 3.2 核心匹配算法
**目标**: 实现高准确率的Logo匹配算法

```python
# backend/logo_matcher.py
class LogoMatcher:
    def __init__(self):
        self.embedder = CLIPEmbedder()
        self.vector_db = VectorDatabase()
        self.confidence_threshold = 0.7
        
    async def match_logo(self, image_data):
        """Logo匹配主流程"""
        # 1. 图像预处理
        # 2. 特征提取
        # 3. 向量搜索
        # 4. 后处理和排序
        # 5. 置信度计算
        
    def calculate_confidence(self, similarity_score, metadata):
        """计算匹配置信度"""
        
    def filter_results(self, results, filters):
        """结果过滤 (按流派、年代等)"""
```

#### 3.3 异步任务处理
**目标**: 处理长时间运行的任务 (批量处理、数据更新等)

```python
# backend/tasks.py
from celery import Celery

celery_app = Celery("logodeth")

@celery_app.task
def batch_process_logos(logo_paths):
    """批量处理Logo特征提取"""
    
@celery_app.task  
def update_vector_database():
    """更新向量数据库"""
```

### Phase 4: 前端集成与测试 (第7-8周)

#### 4.1 前端重构
**目标**: 从mock数据迁移到真实API

**主要修改**:
- 替换 `script.js` 中的mock数据生成
- 集成文件上传API
- 添加实时处理状态显示
- 错误处理和用户反馈

```javascript
// script.js - 新的API集成
class LogoRecognizer {
    constructor() {
        this.apiBase = '/api/v1';
        this.uploadEndpoint = `${this.apiBase}/recognize`;
    }
    
    async recognizeLogo(imageFile) {
        const formData = new FormData();
        formData.append('file', imageFile);
        
        const response = await fetch(this.uploadEndpoint, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
}
```

#### 4.2 高级功能开发
- 批量Logo识别
- 搜索历史记录
- 乐队信息详情页
- 用户偏好设置
- 结果导出功能

#### 4.3 测试框架
**目标**: 确保系统稳定性和准确性

```python
# tests/test_scraper.py
class TestMetalArchivesScraper:
    def test_band_list_parsing(self):
        """测试乐队列表解析"""
        
    def test_logo_download(self):
        """测试Logo下载功能"""
        
# tests/test_matcher.py  
class TestLogoMatcher:
    def test_similarity_calculation(self):
        """测试相似度计算"""
        
    def test_confidence_scoring(self):
        """测试置信度评分"""
```

### Phase 5: 部署与优化 (第9-10周)

#### 5.1 容器化部署
**目标**: 使用Docker进行容器化部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - qdrant
      
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: logodeth
      POSTGRES_USER: logodeth
      POSTGRES_PASSWORD: password
      
  redis:
    image: redis:7-alpine
    
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
```

#### 5.2 性能优化
- 图像处理并行化
- 向量搜索索引优化
- API响应缓存
- CDN配置
- 数据库查询优化

#### 5.3 监控与日志
```python
# backend/monitoring.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('logodeth_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('logodeth_request_duration_seconds', 'Request latency')

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response
```

## 技术挑战与解决方案

### 1. 反爬虫应对
**挑战**: Metal Archives 可能有反爬虫机制
**解决方案**: 
- 随机User-Agent
- 请求间隔控制
- 代理IP轮换
- 模拟人类行为

### 2. 图像质量差异
**挑战**: Logo图像质量、尺寸、格式差异很大
**解决方案**:
- 智能图像预处理
- 多尺度特征提取
- 数据增强技术

### 3. 相似Logo识别
**挑战**: 某些金属乐队Logo非常相似
**解决方案**:
- 多模态特征融合 (图像+文本)
- 层次化匹配策略
- 上下文信息利用

### 4. 实时性能要求
**挑战**: 用户期望快速响应
**解决方案**:
- 向量索引优化
- 异步处理架构
- 智能缓存策略

## 数据集规模估算

- **目标乐队数量**: 50,000+
- **Logo图像**: 50,000+
- **存储需求**: 
  - 原始图像: ~10GB
  - 处理后图像: ~5GB
  - 向量数据: ~100MB
  - 元数据: ~50MB

## 性能指标

- **识别准确率**: Top-1 > 70%, Top-3 > 85%
- **响应时间**: < 500ms (99th percentile)
- **并发处理**: 100+ 用户
- **系统可用性**: 99.9%

## 风险控制

1. **法律风险**: 遵守网站ToS，fair use原则
2. **技术风险**: 多重备份，容错设计
3. **性能风险**: 负载测试，自动扩容
4. **数据风险**: 定期备份，版本控制

## 后续扩展计划

1. **多语言支持**: 支持其他语言的金属网站
2. **移动应用**: iOS/Android 原生应用
3. **浏览器插件**: Chrome/Firefox 扩展
4. **API开放**: 提供公开API服务
5. **社区功能**: 用户贡献、评分系统 