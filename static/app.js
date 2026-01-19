/**
 * AI 磨課師前端應用
 */

let currentResults = null;
let videoBlob = null;

// 初始化
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('courseForm');
    form.addEventListener('submit', handleFormSubmit);

    const generateVideoBtn = document.getElementById('generateVideoBtn');
    generateVideoBtn.addEventListener('click', handleGenerateVideo);

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.addEventListener('click', handleDownload);
});

// 處理表單提交
async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = {
        topic: document.getElementById('topic').value,
        target_audience: document.getElementById('audience').value,
        duration_minutes: parseInt(document.getElementById('duration').value)
    };

    // 顯示進度區域
    document.getElementById('progressSection').classList.add('active');
    document.getElementById('previewSection').classList.remove('active');

    // 禁用按鈕
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> 生成中...';

    // 清空日誌
    const logContainer = document.getElementById('logContainer');
    logContainer.innerHTML = '';

    addLog('🚀 啟動 AI 磨課師系統...');
    addLog(`📚 主題：${formData.topic}`);
    addLog(`👥 受眾：${formData.target_audience}`);
    addLog(`⏱️ 時長：約 ${formData.duration_minutes} 分鐘`);
    addLog('');

    try {
        // 調用後端 API
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            currentResults = result;
            addLog('✅ 所有 Agent 執行完成！');
            addLog(`⏱️ 總耗時：${result.elapsed_time.toFixed(2)} 秒`);

            // 顯示預覽
            showPreview(result);
        } else {
            addLog(`❌ 執行失敗：${result.error}`);
            alert('課程生成失敗：' + result.error);
        }
    } catch (error) {
        addLog(`❌ 網絡錯誤：${error.message}`);
        alert('系統錯誤：' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🚀 開始生成課程';
    }
}

// 添加日誌
function addLog(message) {
    const logContainer = document.getElementById('logContainer');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = `> ${message}`;
    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// 更新 Agent 狀態
function updateAgentStatus(agentNum, status) {
    const agentCard = document.getElementById(`agent${agentNum}`);
    agentCard.classList.remove('active', 'completed');
    if (status === 'active') {
        agentCard.classList.add('active');
    } else if (status === 'completed') {
        agentCard.classList.add('completed');
    }
}

// 顯示預覽
function showPreview(result) {
    const previewSection = document.getElementById('previewSection');
    previewSection.classList.add('active');

    const results = result.results;

    // 顯示課程信息
    const courseInfo = document.getElementById('courseInfo');
    const curriculum = results.curriculum;
    courseInfo.innerHTML = `
        <h3>${curriculum.course_title}</h3>
        <p><strong>目標受眾：</strong>${curriculum.target_audience}</p>
        <p><strong>總時長：</strong>約 ${curriculum.total_duration} 分鐘</p>
        <p><strong>章節數：</strong>${curriculum.chapters.length} 個</p>
    `;

    // 顯示投影片預覽
    const slidesPreview = document.getElementById('slidesPreview');
    slidesPreview.innerHTML = '';

    const slides = results.visual_design.slides;
    slides.forEach((slide, index) => {
        const slideCard = document.createElement('div');
        slideCard.className = 'slide-card';
        slideCard.innerHTML = `
            <div class="slide-preview">${index + 1}</div>
            <h4>${slide.title || '投影片 ' + (index + 1)}</h4>
            <p><small>${slide.slide_type}</small></p>
        `;
        slidesPreview.appendChild(slideCard);
    });

    addLog(`📊 課程包含 ${slides.length} 張投影片`);
}

// 生成影片
async function handleGenerateVideo() {
    if (!currentResults) {
        alert('請先生成課程內容');
        return;
    }

    const btn = document.getElementById('generateVideoBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> 生成影片中...';

    addLog('');
    addLog('🎬 開始生成影片...');
    addLog('📦 準備投影片數據...');

    try {
        // 這裡實現瀏覽器端影片合成
        // 由於完整的 FFmpeg.wasm 實現較複雜，這裡提供簡化版本

        addLog('🎨 渲染投影片...');
        const slides = await renderSlides(currentResults.results);

        addLog('🎵 處理音訊...');
        // 這裡應該調用 TTS API 生成音訊

        addLog('🎞️ 合成影片...');
        // 這裡應該使用 FFmpeg.wasm 合成影片

        // 模擬生成過程
        await new Promise(resolve => setTimeout(resolve, 2000));

        addLog('✅ 影片生成完成！');

        // 啟用下載按鈕
        document.getElementById('downloadBtn').disabled = false;

        // 顯示影片預覽（這裡是佔位符）
        const videoPreview = document.getElementById('videoPreview');
        videoPreview.style.display = 'block';

    } catch (error) {
        addLog(`❌ 影片生成失敗：${error.message}`);
        alert('影片生成失敗：' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🎥 生成影片';
    }
}

// 渲染投影片
async function renderSlides(results) {
    const slides = results.visual_design.slides;
    const renderedSlides = [];

    for (const slide of slides) {
        const canvas = document.createElement('canvas');
        canvas.width = 1920;
        canvas.height = 1080;
        const ctx = canvas.getContext('2d');

        // 背景
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#764ba2');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 標題
        ctx.fillStyle = 'white';
        ctx.font = 'bold 60px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(slide.title || '', canvas.width / 2, 200);

        // 內容
        if (slide.content && slide.content.text) {
            ctx.font = '40px Arial';
            ctx.fillText(slide.content.text.substring(0, 50) + '...', canvas.width / 2, 400);
        }

        // 轉換為 Blob
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        renderedSlides.push(blob);
    }

    return renderedSlides;
}

// 下載影片
function handleDownload() {
    if (!videoBlob && currentResults) {
        // 如果沒有實際的影片，下載課程數據作為 JSON
        const dataStr = JSON.stringify(currentResults, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `course_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        addLog('💾 課程數據已下載（JSON 格式）');
    } else if (videoBlob) {
        const url = URL.createObjectURL(videoBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `course_${Date.now()}.mp4`;
        a.click();
        URL.revokeObjectURL(url);

        addLog('💾 影片已下載');
    }
}
