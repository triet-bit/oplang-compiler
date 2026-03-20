// Khởi tạo Editor (CodeMirror)
var editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    mode: "text/x-java", // Cú pháp giống Java
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4
});

async function submitCode() {
    const runBtn = document.getElementById("run-btn");
    const outputConsole = document.getElementById("output-console");
    const loader = document.getElementById("loader");

    // 1. Lấy code từ editor
    const sourceCode = editor.getValue();
    if (!sourceCode.trim()) {
        outputConsole.innerHTML = '<span class="error-text">Code cannot be empty!</span>';
        return;
    }

    // UI: Đang chạy
    runBtn.disabled = true;
    outputConsole.innerText = "";
    loader.classList.remove("hidden");

    try {
        // 2. Gửi API Submit
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: sourceCode })
        });

        const data = await response.json();
        const taskId = data.task_id;
        
        // 3. Bắt đầu polling (hỏi kết quả liên tục)
        pollResult(taskId);

    } catch (error) {
        outputConsole.innerHTML = `<span class="error-text">System Error: ${error.message}</span>`;
        resetUI();
    }
}

async function pollResult(taskId) {
    const outputConsole = document.getElementById("output-console");
    
    // Hàm đệ quy hỏi kết quả mỗi 1 giây
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`/result/${taskId}`);
            const data = await res.json();

            if (data.status === 'completed') {
                clearInterval(interval); // Dừng hỏi
                
                // 4. Hiển thị kết quả
                const result = data.data;
                if (result.status === 'success') {
                    outputConsole.innerHTML = `<span class="success-text">✓ Build Successful</span>\n\n${result.output}`;
                } else {
                    // Hiển thị lỗi (compile error, runtime error...)
                    outputConsole.innerHTML = `<span class="error-text">✗ Error (${result.status}):</span>\n${result.error}`;
                }
                resetUI();
            }
        } catch (e) {
            clearInterval(interval);
            outputConsole.innerHTML = `<span class="error-text">Network Error during polling</span>`;
            resetUI();
        }
    }, 500); // 500ms = 0.5 giây
}

function resetUI() {
    document.getElementById("run-btn").disabled = false;
    document.getElementById("loader").classList.add("hidden");
}