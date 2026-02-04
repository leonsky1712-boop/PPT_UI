import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './index.css';

// 后端 API 地址（开发时可为 http://localhost:5000）
const API_BASE = process.env.REACT_APP_API_URL || '';

// 模板配置
const TEMPLATES = [
  {
    id: 'modern-elegant',
    name: '现代优雅',
    description: '渐变背景，现代排版',
    icon: '🎨',
    preview: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
    industries: ['科技', '创业', '创意'],
    complexity: '中等'
  },
  {
    id: 'corporate-blue',
    name: '企业蓝调',
    description: '专业商务风格',
    icon: '💼',
    preview: 'linear-gradient(180deg, #1a365d 0%, #2b6cb0 100%)',
    industries: ['金融', '企业', '咨询'],
    complexity: '简单'
  },
  {
    id: 'minimal-clean',
    name: '极简纯净',
    description: '极简主义设计',
    icon: '✨',
    preview: '#ffffff',
    industries: ['技术', '学术', '研究'],
    complexity: '简单'
  },
  {
    id: 'creative-bold',
    name: '创意大胆',
    description: '赛博朋克风格',
    icon: '🚀',
    preview: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%)',
    industries: ['创意', '游戏', '营销'],
    complexity: '复杂'
  }
];

// 演示类型
const PRESENTATION_TYPES = [
  { id: 'business_presentation', name: '商业汇报', icon: '📊', desc: '季度总结、进度汇报' },
  { id: 'investor_pitch', name: '投资路演', icon: '🎯', desc: '创业融资、VC 演示' },
  { id: 'product_launch', name: '产品发布', icon: '🚀', desc: '新品发布、功能介绍' },
  { id: 'training_workshop', name: '培训研讨', icon: '📚', desc: '企业培训、工作坊' },
  { id: 'webinar', name: '在线讲座', icon: '🎥', desc: '网络研讨会、直播' },
  { id: 'keynote', name: '主题演讲', icon: '🎤', desc: '会议演讲、论坛' },
  { id: 'sales_pitch', name: '销售演示', icon: '💰', desc: '客户提案、商务洽谈' }
];

// 受众群体
const AUDIENCES = [
  { id: 'general_employees', name: '普通员工', icon: '👥' },
  { id: 'senior_executives', name: '高管领导', icon: '👔' },
  { id: 'investors', name: '投资人士', icon: '💼' },
  { id: 'clients', name: '客户伙伴', icon: '🤝' },
  { id: 'technical_team', name: '技术团队', icon: '💻' },
  { id: 'students', name: '学生群体', icon: '🎓' }
];

// 时长选项
const DURATIONS = [
  { value: 5, label: '5 分钟' },
  { value: 10, label: '10 分钟' },
  { value: 15, label: '15 分钟' },
  { value: 20, label: '20 分钟' },
  { value: 30, label: '30 分钟' },
  { value: 45, label: '45 分钟' },
  { value: 60, label: '60 分钟' }
];

// 色调风格
const TONES = [
  { id: 'professional', name: '专业', color: '#667eea' },
  { id: 'casual', name: '轻松', color: '#48bb78' },
  { id: 'persuasive', name: '说服力', color: '#ed8936' },
  { id: 'inspirational', name: '激励性', color: '#f093fb' },
  { id: 'educational', name: '教育性', color: '#4299e1' }
];

function App() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    topic: '',
    template: 'modern-elegant',
    type: 'business_presentation',
    audience: 'general_employees',
    duration: 15,
    tone: 'professional',
    industry: '',
    author: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = async () => {
    if (!formData.topic.trim()) {
      alert('请输入演示主题');
      return;
    }

    setIsGenerating(true);
    setResult(null);

    try {
      const url = API_BASE ? `${API_BASE}/api/generate` : '/api/generate';
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: formData.topic,
          template: formData.template,
          type: formData.type,
          audience: formData.audience,
          duration: formData.duration,
          tone: formData.tone,
          industry: formData.industry || '',
          author: formData.author || ''
        })
      });
      const data = await res.json().catch(() => ({}));

      if (res.ok && data.success) {
        const previewUrl = data.data?.url
          ? (API_BASE ? `${API_BASE}${data.data.url}` : data.data.url)
          : null;
        setResult({
          success: true,
          message: data.message || '演示文稿生成成功！',
          url: previewUrl,
          filename: data.data?.filename,
          title: data.data?.title,
          slide_count: data.data?.slide_count
        });
      } else {
        setResult({
          success: false,
          message: data.error || data.message || '生成失败，请重试'
        });
      }
    } catch (error) {
      setResult({
        success: false,
        message: error.message || '网络错误，请确认后端服务已启动'
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const resetForm = () => {
    setStep(1);
    setFormData({
      topic: '',
      template: 'modern-elegant',
      type: 'business_presentation',
      audience: 'general_employees',
      duration: 15,
      tone: 'professional',
      industry: '',
      author: ''
    });
    setResult(null);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* 头部 */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-3 mb-4">
            <span className="text-5xl">🎯</span>
            <h1 className="text-4xl font-bold gradient-text">
              AI PPT 智能生成器
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            输入主题，AI 自动生成专业演示文稿
          </p>
        </motion.header>

        {/* 进度指示器 */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex justify-center mb-8"
        >
          <div className="flex items-center gap-4">
            {[1, 2, 3].map(num => (
              <React.Fragment key={num}>
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                    step >= num
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {num}
                </div>
                {num < 3 && (
                  <div className={`w-16 h-1 rounded ${step > num ? 'bg-gradient-to-r from-purple-500 to-pink-500' : 'bg-gray-200'}`} />
                )}
              </React.Fragment>
            ))}
          </div>
        </motion.div>

        {/* 主要内容区 */}
        <AnimatePresence mode="wait">
          {!result ? (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="glass-card rounded-3xl p-8 shadow-2xl"
            >
              {/* Step 1: 主题输入 */}
              {step === 1 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">
                    📝 输入演示主题
                  </h2>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      演示主题
                    </label>
                    <input
                      type="text"
                      value={formData.topic}
                      onChange={(e) => handleInputChange('topic', e.target.value)}
                      placeholder="例如：2024年Q4产品销售回顾"
                      className="input-field w-full px-6 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 outline-none text-lg"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        行业/领域
                      </label>
                      <input
                        type="text"
                        value={formData.industry}
                        onChange={(e) => handleInputChange('industry', e.target.value)}
                        placeholder="例如：科技、教育、医疗"
                        className="input-field w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        演讲者
                      </label>
                      <input
                        type="text"
                        value={formData.author}
                        onChange={(e) => handleInputChange('author', e.target.value)}
                        placeholder="您的名字"
                        className="input-field w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 outline-none"
                      />
                    </div>
                  </div>

                  <button
                    onClick={() => formData.topic && setStep(2)}
                    disabled={!formData.topic.trim()}
                    className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all"
                  >
                    下一步 →
                  </button>
                </div>
              )}

              {/* Step 2: 配置选项 */}
              {step === 2 && (
                <div className="space-y-8">
                  <div className="flex items-center justify-between">
                    <h2 className="text-2xl font-semibold text-gray-800">
                      ⚙️ 选择配置
                    </h2>
                    <button
                      onClick={() => setStep(1)}
                      className="text-purple-500 hover:text-purple-600"
                    >
                      ← 返回
                    </button>
                  </div>

                  {/* 演示类型 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      演示类型
                    </label>
                    <div className="grid grid-cols-4 gap-3">
                      {PRESENTATION_TYPES.map(type => (
                        <button
                          key={type.id}
                          onClick={() => handleInputChange('type', type.id)}
                          className={`p-4 rounded-xl border-2 text-left transition-all ${
                            formData.type === type.id
                              ? 'border-purple-500 bg-purple-50'
                              : 'border-gray-200 hover:border-purple-300'
                          }`}
                        >
                          <div className="text-2xl mb-2">{type.icon}</div>
                          <div className="font-medium text-gray-800">{type.name}</div>
                          <div className="text-xs text-gray-500">{type.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* 受众和时长 */}
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-3">
                        目标受众
                      </label>
                      <select
                        value={formData.audience}
                        onChange={(e) => handleInputChange('audience', e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 outline-none"
                      >
                        {AUDIENCES.map(aud => (
                          <option key={aud.id} value={aud.id}>
                            {aud.icon} {aud.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-3">
                        预计时长
                      </label>
                      <select
                        value={formData.duration}
                        onChange={(e) => handleInputChange('duration', parseInt(e.target.value))}
                        className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 outline-none"
                      >
                        {DURATIONS.map(dur => (
                          <option key={dur.value} value={dur.value}>
                            {dur.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* 色调风格 */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      色调风格
                    </label>
                    <div className="flex gap-4">
                      {TONES.map(tone => (
                        <button
                          key={tone.id}
                          onClick={() => handleInputChange('tone', tone.id)}
                          className={`flex-1 py-3 rounded-xl border-2 transition-all ${
                            formData.tone === tone.id
                              ? 'ring-2 ring-offset-2 ring-purple-500'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                          style={{ backgroundColor: tone.color }}
                        >
                          <span className="text-white font-medium">{tone.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button
                      onClick={() => setStep(1)}
                      className="flex-1 py-4 border-2 border-gray-200 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition-all"
                    >
                      上一步
                    </button>
                    <button
                      onClick={() => setStep(3)}
                      className="flex-1 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
                    >
                      下一步 →
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: 选择模板 */}
              {step === 3 && (
                <div className="space-y-8">
                  <div className="flex items-center justify-between">
                    <h2 className="text-2xl font-semibold text-gray-800">
                      🎨 选择模板
                    </h2>
                    <button
                      onClick={() => setStep(2)}
                      className="text-purple-500 hover:text-purple-600"
                    >
                      ← 返回
                    </button>
                  </div>

                  <div className="grid grid-cols-4 gap-4">
                    {TEMPLATES.map(template => (
                      <motion.button
                        key={template.id}
                        onClick={() => handleInputChange('template', template.id)}
                        className={`template-card relative overflow-hidden rounded-2xl p-6 text-left ${
                          formData.template === template.id
                            ? 'ring-4 ring-purple-500'
                            : 'bg-white border-2 border-gray-200'
                        }`}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        {/* 预览图 */}
                        <div
                          className="h-32 -m-6 mb-4 rounded-t-2xl"
                          style={{ background: template.preview }}
                        />

                        {/* 选中标识 */}
                        {formData.template === template.id && (
                          <div className="absolute top-3 right-3 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                            <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}

                        <div className="text-3xl mb-2">{template.icon}</div>
                        <h3 className="font-semibold text-gray-800">{template.name}</h3>
                        <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                        <div className="flex gap-2 mt-3">
                          {template.industries.slice(0, 2).map(ind => (
                            <span key={ind} className="text-xs px-2 py-1 bg-gray-100 rounded-full text-gray-600">
                              {ind}
                            </span>
                          ))}
                        </div>
                      </motion.button>
                    ))}
                  </div>

                  {/* 生成按钮 */}
                  <div className="flex gap-4 pt-4">
                    <button
                      onClick={() => setStep(2)}
                      className="flex-1 py-4 border-2 border-gray-200 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition-all"
                    >
                      上一步
                    </button>
                    <button
                      onClick={handleGenerate}
                      disabled={isGenerating}
                      className="flex-1 py-4 bg-gradient-to-r from-purple-500 via-pink-500 to-fuchsia-500 text-white rounded-xl font-semibold text-lg disabled:opacity-50 hover:shadow-xl transition-all animate-pulse-glow"
                    >
                      {isGenerating ? (
                        <span className="flex items-center justify-center gap-2">
                          <div className="loading-spinner w-6 h-6 border-2 border-white border-t-transparent" />
                          AI 正在生成中...
                        </span>
                      ) : (
                        '🚀 开始生成'
                      )}
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          ) : (
            /* 结果展示 */
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-card rounded-3xl p-8 shadow-2xl text-center"
            >
              {result.success ? (
                <>
                  <div className="text-6xl mb-6">🎉</div>
                  <h2 className="text-3xl font-bold gradient-text mb-4">
                    {result.message}
                  </h2>
                  <p className="text-gray-600 mb-8">
                    您的演示文稿已准备就绪！
                  </p>

                  {/* 预览区域 */}
                  {result.url && (
                    <div className="mb-8">
                      <div className="bg-gray-100 rounded-xl p-2">
                        <iframe
                          src={result.url}
                          className="w-full aspect-video preview-frame"
                          title="Preview"
                        />
                      </div>
                    </div>
                  )}

                  {/* 操作按钮 */}
                  <div className="flex justify-center gap-4 flex-wrap">
                    {result.url && (
                      <button
                        onClick={() => window.open(result.url, '_blank')}
                        className="px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
                      >
                        🔗 在新窗口打开
                      </button>
                    )}
                    {result.filename && result.url && (
                      <a
                        href={result.url}
                        download={result.filename}
                        className="px-8 py-3 bg-white border-2 border-purple-500 text-purple-600 rounded-xl font-semibold hover:bg-purple-50 transition-all"
                      >
                        📥 下载 HTML
                      </a>
                    )}
                    <button
                      onClick={resetForm}
                      className="px-8 py-3 border-2 border-gray-200 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition-all"
                    >
                      📝 创建新的演示
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <div className="text-6xl mb-6">😢</div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">
                    {result.message}
                  </h2>
                  <button
                    onClick={resetForm}
                    className="px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
                  >
                    重试
                  </button>
                </>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* 底部 */}
        <footer className="text-center mt-12 text-white/60 text-sm">
          <p>Powered by AI • 快速生成专业演示文稿</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
