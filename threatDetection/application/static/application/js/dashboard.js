/**
 * AI-Based Threat Intelligence System - Dashboard JavaScript
 * Handles Safe Markdown Parsing, Loading Radar, Email Presets,
 * Dynamic Character Counters, and Animated Probability Gauges.
 */

document.addEventListener('DOMContentLoaded', () => {
  initEmailEditor();
  initFormSubmission();
  initProbabilityBars();
  renderThreatReport();
});

/* ==========================================================================
   1. Email Editor & Presets
   ========================================================================== */

const EMAIL_SAMPLES = {
  bank_phishing: `URGENT: Your Chase Bank Account Access Has Been Suspended!

Dear Customer,

We detected unauthorized sign-in attempts on your account from an unrecognized IP address (Moscow, RU). For your protection, your online banking access has been temporarily restricted.

To restore full account functionality immediately, you must verify your identity within 12 hours by accessing the secure link below:

http://security-update-chase-verification.net/login?token=892348

Failure to verify will result in permanent suspension of your account and debit card.

Sincerely,
Chase Fraud Prevention & Security Team
JPMorgan Chase Bank, N.A.`,

  password_reset: `Urgent Security Notice: Reset your Corporate Microsoft 365 Password

Attention Employee,

Your Office 365 password expires in 2 hours. If you do not update your credentials immediately, you will lose access to Outlook, Teams, and internal servers.

Update your credentials right away at:
http://internal-portal-login.office365-auth-sync.com/update-pwd

Do not ignore this message. Contact IT Helpdesk if you encounter issues.`,

  fake_prize: `Congratulations! You Have Won $2,500,000 in the International Mega Lottery!

Reference Ticket No: LMT-99410-WIN
Batch Number: 2026/EU-991

You were selected as one of the 5 lucky winners in our international email lottery draw. To claim your prize money, send your full name, bank account number, phone number, and a copy of your passport to:

claims-officer@international-lottery-distribution-center.org

You must pay a clearance fee of $150 via Western Union or Gift Cards to initiate wire transfer.`,

  normal_meeting: `Hi Team,

Just a reminder about our weekly sprint planning meeting scheduled for tomorrow, Wednesday at 10:30 AM EST via Zoom.

Agenda:
1. Review sprint goals and deliverables for Q4.
2. Discuss threat telemetry data pipeline performance.
3. Assign tickets for API rate limiting and security audits.

Please review the attached project board and add your updates before the meeting starts.

Best regards,
Sarah Jenkins
Project Manager | Engineering Operations`,

  normal_job: `Dear Hiring Team,

I am writing to express my strong interest in the Cybersecurity Analyst position at your organization. 

With over 4 years of experience in SOC operations, incident response, and SIEM monitoring (Splunk and Elastic), I have consistently helped organizations identify threats and strengthen their security posture.

I have attached my resume and certifications (Security+, CySA+) for your consideration. I look forward to the opportunity to discuss how my technical skills align with your team's objectives.

Thank you for your time and consideration.

Sincerely,
David Miller
Email: david.miller@email.com
LinkedIn: linkedin.com/in/david-miller-sec`,

  delivery_phishing: `DHL Express: Your package delivery #US-982143 is on hold!

Dear Customer,

Your parcel #US-982143 could not be delivered on November 2, 2026, due to an incorrect shipping address and unpaid customs fee ($2.95 USD).

Please confirm your delivery address and settle the fee within 24 hours to schedule re-delivery:

http://dhl-express-tracking-delivery-confirm.net/pay?parcel=982143

If no response is received, the shipment will be returned to the sender.

DHL Logistics Support`
};

function initEmailEditor() {
  const textarea = document.getElementById('email_text');
  const charCounter = document.getElementById('char-count');
  const wordCounter = document.getElementById('word-count');
  const presetSelect = document.getElementById('sample-presets');
  const clearBtn = document.getElementById('btn-clear');

  if (!textarea) return;

  function updateCounters() {
    const text = textarea.value;
    const charCount = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;

    if (charCounter) charCounter.textContent = `${charCount} characters`;
    if (wordCounter) wordCounter.textContent = `${words} words`;
  }

  textarea.addEventListener('input', updateCounters);
  updateCounters();

  if (presetSelect) {
    presetSelect.addEventListener('change', (e) => {
      const selectedKey = e.target.value;
      if (selectedKey && EMAIL_SAMPLES[selectedKey]) {
        textarea.value = EMAIL_SAMPLES[selectedKey];
        updateCounters();
        textarea.focus();
      }
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      textarea.value = '';
      if (presetSelect) presetSelect.value = '';
      updateCounters();
      textarea.focus();
    });
  }
}

/* ==========================================================================
   2. Form Submission & Radar Animation
   ========================================================================== */

function initFormSubmission() {
  const form = document.getElementById('threat-form');
  const textarea = document.getElementById('email_text');
  const analyzeBtn = document.getElementById('btn-analyze');
  const loadingIndicator = document.getElementById('loading-indicator');
  const stepIndicators = document.querySelectorAll('.loading-step');

  if (!form || !analyzeBtn) return;

  form.addEventListener('submit', (e) => {
    const content = textarea ? textarea.value.trim() : '';

    if (!content) {
      e.preventDefault();
      alert('Please enter or paste email content to analyze.');
      if (textarea) textarea.focus();
      return;
    }

    // Disable button to prevent duplicate submissions
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <svg class="radar-sweep-icon" style="width:18px;height:18px;animation:spin 1s linear infinite" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Analyzing Threat Vectors...
    `;

    // Show loading radar indicator
    if (loadingIndicator) {
      loadingIndicator.style.display = 'block';
      loadingIndicator.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Cycle through analysis steps visually
    let currentStep = 0;
    const stepInterval = setInterval(() => {
      if (stepIndicators && stepIndicators.length > 0) {
        stepIndicators.forEach((step, idx) => {
          if (idx <= currentStep) {
            step.classList.add('active');
          } else {
            step.classList.remove('active');
          }
        });
        currentStep = (currentStep + 1) % stepIndicators.length;
      }
    }, 2800);
  });
}

/* ==========================================================================
   3. Probability Progress Bar Animation
   ========================================================================== */

function initProbabilityBars() {
  const phishingFill = document.getElementById('fill-phishing');
  const safeFill = document.getElementById('fill-safe');

  if (!phishingFill && !safeFill) return;

  // Read target probabilities from data attributes
  setTimeout(() => {
    if (phishingFill) {
      const phishingPct = parseFloat(phishingFill.getAttribute('data-percentage') || 0);
      phishingFill.style.width = `${Math.min(100, Math.max(0, phishingPct))}%`;
    }

    if (safeFill) {
      const safePct = parseFloat(safeFill.getAttribute('data-percentage') || 0);
      safeFill.style.width = `${Math.min(100, Math.max(0, safePct))}%`;
    }
  }, 100);
}

/* ==========================================================================
   4. Safe Markdown Rendering Engine for Llama 3.2 Report
   ========================================================================== */

/**
 * Escapes any raw HTML entities to strictly prevent HTML/XSS injection.
 */
function escapeHtml(unsafeText) {
  return String(unsafeText)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Parses markdown safely without any arbitrary HTML execution.
 */
function safeMarkdownParser(markdownText) {
  if (!markdownText) return '';

  // Step 1: Escape all HTML entities completely
  let text = escapeHtml(markdownText);

  // Normalize line breaks
  text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // Step 2: Convert Headers (###, ##, #)
  text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  text = text.replace(/^# (.*$)/gim, '<h2>$1</h2>');

  // Step 3: Format Risk Level tags dynamically
  text = text.replace(/\b(Risk Level|Risk):\s*(High|Critical)\b/gi, (match, p1, p2) => {
    return `<strong>${p1}:</strong> <span class="risk-tag critical">${p2}</span>`;
  });
  text = text.replace(/\b(Risk Level|Risk):\s*(Medium|Moderate)\b/gi, (match, p1, p2) => {
    return `<strong>${p1}:</strong> <span class="risk-tag medium">${p2}</span>`;
  });
  text = text.replace(/\b(Risk Level|Risk):\s*(Low|Minimal|Safe)\b/gi, (match, p1, p2) => {
    return `<strong>${p1}:</strong> <span class="risk-tag low">${p2}</span>`;
  });

  // Step 4: Convert bold & italics
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/__(.*?)__/g, '<strong>$1</strong>');
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
  text = text.replace(/_(.*?)_/g, '<em>$1</em>');

  // Step 5: Convert inline code
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Step 6: Convert blockquotes
  text = text.replace(/^>\s+(.*$)/gim, '<blockquote>$1</blockquote>');

  // Step 7: Convert lists
  // Unordered lists (- or *)
  text = text.replace(/^\s*[-*]\s+(.*)$/gim, '<li class="ul-item">$1</li>');
  // Numbered lists (1. 2. etc.)
  text = text.replace(/^\s*(\d+)\.\s+(.*)$/gim, '<li class="ol-item" value="$1">$2</li>');

  // Wrap consecutive list items
  text = text.replace(/(<li class="ul-item">.*<\/li>(\s*<li class="ul-item">.*<\/li>)*)/g, '<ul>$1</ul>');
  text = text.replace(/(<li class="ol-item".*<\/li>(\s*<li class="ol-item".*<\/li>)*)/g, '<ol>$1</ol>');

  // Clean helper classes
  text = text.replace(/class="ul-item"/g, '');
  text = text.replace(/class="ol-item"/g, '');

  // Step 8: Convert paragraphs & remaining double linebreaks
  const blocks = text.split(/\n{2,}/);
  const formattedBlocks = blocks.map(block => {
    const trimmed = block.trim();
    if (!trimmed) return '';
    if (
      trimmed.startsWith('<h2>') ||
      trimmed.startsWith('<h3>') ||
      trimmed.startsWith('<ul>') ||
      trimmed.startsWith('<ol>') ||
      trimmed.startsWith('<blockquote>')
    ) {
      return trimmed;
    }
    // Convert single newlines inside paragraph to <br>
    return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
  });

  return formattedBlocks.join('\n');
}

function renderThreatReport() {
  const rawReportContainer = document.getElementById('raw-llm-report');
  const renderedContainer = document.getElementById('rendered-llm-report');

  if (!rawReportContainer || !renderedContainer) return;

  const rawText = rawReportContainer.textContent || '';
  if (rawText.trim()) {
    renderedContainer.innerHTML = safeMarkdownParser(rawText);
  }
}
