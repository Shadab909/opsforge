// ==========================================================================
// 🔥 OpsForge Client-Side Interactivity & Terminal Highlighting
// ==========================================================================

const COPY_ICON_SVG = `
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
</svg>
`;

const CHECK_ICON_SVG = `
<svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
</svg>
`;

document.addEventListener('DOMContentLoaded', () => {
    // 1. Colorize Ansible terminal playbook output (Matching Image 2)
    colorizeAnsiblePlaybookOutputs();

    // 2. Add minimalist SVG copy buttons to code blocks
    document.querySelectorAll('.markdown-content pre').forEach((pre) => {
        const btn = document.createElement('button');
        btn.className = 'copy-code-btn';
        btn.innerHTML = COPY_ICON_SVG;
        btn.type = 'button';
        btn.title = 'Copy code';
        
        btn.addEventListener('click', () => {
            const code = pre.querySelector('code') || pre;
            navigator.clipboard.writeText(code.innerText.trim()).then(() => {
                btn.innerHTML = CHECK_ICON_SVG;
                setTimeout(() => {
                    btn.innerHTML = COPY_ICON_SVG;
                }, 2000);
            });
        });
        
        pre.appendChild(btn);
    });

    // 3. Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.bg-emerald-950\\/60, .bg-rose-950\\/60').forEach((el) => {
            el.style.transition = 'opacity 0.5s ease-out';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 500);
        });
    }, 5000);
});

// Colorizes Ansible playbook execution outputs to match terminal aesthetic (Image 2)
function colorizeAnsiblePlaybookOutputs() {
    document.querySelectorAll('.markdown-content pre code').forEach((codeBlock) => {
        const rawText = codeBlock.innerText || codeBlock.textContent;
        if (!rawText.includes('PLAY [') && !rawText.includes('TASK [') && !rawText.includes('PLAY RECAP')) {
            return;
        }

        const lines = rawText.split('\n');
        const formattedLines = lines.map(line => {
            const trimmed = line.trim();
            // PLAY [webservers] **************************
            if (trimmed.startsWith('PLAY ') || trimmed.startsWith('PLAY:')) {
                return `<span class="ansible-header-play">${escapeHtml(line)}</span>`;
            }
            // TASK [Install nginx] ************************
            if (trimmed.startsWith('TASK ') || trimmed.startsWith('TASK:')) {
                return `<span class="ansible-header-task">${escapeHtml(line)}</span>`;
            }
            // PLAY RECAP *********************************
            if (trimmed.startsWith('PLAY RECAP')) {
                return `<span class="ansible-header-recap">${escapeHtml(line)}</span>`;
            }
            // ok: [web1]
            if (trimmed.startsWith('ok:')) {
                return `<span class="ansible-status-ok">${escapeHtml(line)}</span>`;
            }
            // changed: [web1]
            if (trimmed.startsWith('changed:')) {
                return `<span class="ansible-status-ok">${escapeHtml(line)}</span>`;
            }
            // Recap line: web1 : ok=2 changed=1 unreachable=0 failed=0 skipped=0
            if (trimmed.includes(':') && trimmed.includes('ok=') && trimmed.includes('changed=')) {
                let escaped = escapeHtml(line);
                // Host name in cyan
                escaped = escaped.replace(/^(\s*[\w.-]+\s*:)/, '<span class="ansible-status-ok">$1</span>');
                // ok=N in amber
                escaped = escaped.replace(/(ok=\d+)/g, '<span class="ansible-status-changed">$1</span>');
                // changed=N in amber
                escaped = escaped.replace(/(changed=\d+)/g, '<span class="ansible-status-changed">$1</span>');
                // unreachable=N in red
                escaped = escaped.replace(/(unreachable=\d+)/g, '<span class="ansible-status-failed">$1</span>');
                // failed=N in red
                escaped = escaped.replace(/(failed=\d+)/g, '<span class="ansible-status-failed">$1</span>');
                // skipped=N in red
                escaped = escaped.replace(/(skipped=\d+)/g, '<span class="ansible-status-failed">$1</span>');
                return escaped;
            }

            return escapeHtml(line);
        });

        codeBlock.innerHTML = formattedLines.join('\n');
    });
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// AJAX Mark As Reviewed Handler
function handleMarkAsRead(url) {
    const btn = document.getElementById('markReadBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span>⏳</span><span>Saving review...</span>`;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Update UI
            const markReadSection = document.getElementById('markReadSection');
            if (markReadSection) {
                markReadSection.innerHTML = `
                    <div class="flex items-center space-x-2 text-sm text-emerald-400 font-semibold bg-emerald-500/10 px-4 py-2.5 rounded-xl border border-emerald-500/20">
                        <span>✓</span>
                        <span>Reviewed & Unlocked</span>
                    </div>
                `;
            }

            // Update badge at top
            const readStatusBadge = document.getElementById('readStatusBadge');
            if (readStatusBadge) {
                readStatusBadge.className = 'text-emerald-400';
                readStatusBadge.innerText = '✓ Content Reviewed';
            }

            // Enable quiz buttons
            ['takeQuizBtnTop', 'takeQuizBtnBottom', 'takeQuizBtnSidebar'].forEach(id => {
                const quizBtn = document.getElementById(id);
                if (quizBtn) {
                    quizBtn.classList.remove('opacity-60', 'cursor-not-allowed', 'pointer-events-none');
                }
            });
        }
    })
    .catch(err => {
        console.error('Error marking as read:', err);
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = `<span>⚠️</span><span>Failed. Try Again</span>`;
        }
    });
}
