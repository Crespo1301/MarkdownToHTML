"use strict";

const MAX_FILE_BYTES = 750000;
const STORAGE_KEY = "mdtohtmlconverter:draft:v2";
const SAMPLE = `# Publish-ready Markdown

Turn **Markdown** into clean HTML for a website, blog, or CMS.

## What you can do

- Preview the rendered result
- Inspect and copy the HTML source
- Download a complete styled document

> The preview is sandboxed and unsafe links are removed.

\`\`\`html
<article>Your code examples remain escaped.</article>
\`\`\``;

const elements = {
  markdown: document.querySelector("#markdown-input"),
  title: document.querySelector("#title-input"),
  theme: document.querySelector("#theme-select"),
  output: document.querySelector("#output-select"),
  toc: document.querySelector("#toc-checkbox"),
  iframe: document.querySelector("#preview-frame"),
  preview: document.querySelector("#preview-container"),
  source: document.querySelector("#source-output"),
  sourceCode: document.querySelector("#source-output code"),
  empty: document.querySelector("#empty-state"),
  status: document.querySelector("#status"),
  stats: document.querySelector("#input-stats"),
  file: document.querySelector("#file-input"),
  upload: document.querySelector("#upload-btn"),
  sample: document.querySelector("#sample-btn"),
  clear: document.querySelector("#clear-btn"),
  copy: document.querySelector("#copy-btn"),
  download: document.querySelector("#download-btn"),
  previewTab: document.querySelector("#preview-tab"),
  sourceTab: document.querySelector("#source-tab"),
  toast: document.querySelector("#toast"),
};

let currentHtml = "";
let debounceTimer;
let activeRequest;
let requestSequence = 0;
let toastTimer;

function announce(message, kind = "") {
  elements.status.textContent = message;
  elements.status.dataset.kind = kind;
}

function toast(message) {
  window.clearTimeout(toastTimer);
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  toastTimer = window.setTimeout(() => elements.toast.classList.remove("show"), 2400);
}

function updateStats() {
  const value = elements.markdown.value;
  const words = value.trim() ? value.trim().split(/\s+/u).length : 0;
  const lines = value ? value.split(/\r\n|\r|\n/u).length : 0;
  elements.stats.textContent = `${value.length.toLocaleString()} characters · ${words.toLocaleString()} words · ${lines.toLocaleString()} lines`;
}

function saveDraft() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      markdown: elements.markdown.value,
      title: elements.title.value,
      theme: elements.theme.value,
      output: elements.output.value,
      toc: elements.toc.checked,
    }));
  } catch (_error) {
    announce("Draft could not be saved in this browser.", "error");
  }
}

function restoreDraft() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (!saved || typeof saved.markdown !== "string") return;
    elements.markdown.value = saved.markdown;
    elements.title.value = typeof saved.title === "string" ? saved.title : "Converted Document";
    elements.theme.value = saved.theme === "dark" ? "dark" : "light";
    elements.output.value = saved.output === "fragment" ? "fragment" : "document";
    elements.toc.checked = saved.toc !== false;
  } catch (_error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function setBusy(isBusy) {
  elements.copy.disabled = isBusy || !currentHtml;
  elements.download.disabled = isBusy || !elements.markdown.value.trim();
  elements.markdown.setAttribute("aria-busy", String(isBusy));
}

async function requestConversion(fragmentOnly, signal) {
  const response = await fetch("/api/convert", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      markdown: elements.markdown.value,
      title: elements.title.value || "Converted Document",
      theme: elements.theme.value,
      includeToc: elements.toc.checked,
      fragmentOnly,
    }),
    signal,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Conversion failed. Please try again.");
  return data.html;
}

async function convertMarkdown() {
  saveDraft();
  updateStats();
  if (!elements.markdown.value.trim()) {
    if (activeRequest) activeRequest.abort();
    currentHtml = "";
    elements.iframe.srcdoc = "";
    elements.sourceCode.textContent = "";
    elements.empty.hidden = false;
    announce("Ready");
    setBusy(false);
    return;
  }

  if (activeRequest) activeRequest.abort();
  activeRequest = new AbortController();
  const sequence = ++requestSequence;
  setBusy(true);
  announce("Converting…");
  try {
    const html = await requestConversion(elements.output.value === "fragment", activeRequest.signal);
    if (sequence !== requestSequence) return;
    currentHtml = html;
    elements.iframe.srcdoc = html;
    elements.sourceCode.textContent = html;
    elements.empty.hidden = true;
    announce("Conversion complete", "success");
  } catch (error) {
    if (error.name === "AbortError") return;
    announce(error.message, "error");
  } finally {
    if (sequence === requestSequence) setBusy(false);
  }
}

function scheduleConversion() {
  window.clearTimeout(debounceTimer);
  updateStats();
  saveDraft();
  announce("Waiting for input…");
  debounceTimer = window.setTimeout(convertMarkdown, 450);
}

function showView(view) {
  const sourceVisible = view === "source";
  elements.preview.hidden = sourceVisible;
  elements.source.hidden = !sourceVisible;
  elements.previewTab.classList.toggle("active", !sourceVisible);
  elements.sourceTab.classList.toggle("active", sourceVisible);
  elements.previewTab.setAttribute("aria-selected", String(!sourceVisible));
  elements.sourceTab.setAttribute("aria-selected", String(sourceVisible));
}

async function copyHtml() {
  if (!currentHtml) return;
  try {
    await navigator.clipboard.writeText(currentHtml);
  } catch (_error) {
    const temporary = document.createElement("textarea");
    temporary.value = currentHtml;
    document.body.append(temporary);
    temporary.select();
    document.execCommand("copy");
    temporary.remove();
  }
  toast(elements.output.value === "fragment" ? "HTML fragment copied" : "Complete HTML copied");
}

async function downloadHtml() {
  if (!elements.markdown.value.trim()) return;
  elements.download.disabled = true;
  announce("Preparing complete document…");
  try {
    const html = elements.output.value === "document" ? currentHtml : await requestConversion(false);
    const filename = (elements.title.value || "converted-document").toLowerCase().replace(/[^a-z0-9]+/gu, "-").replace(/^-|-$/gu, "") || "converted-document";
    const url = URL.createObjectURL(new Blob([html], { type: "text/html;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `${filename}.html`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    toast("Complete HTML document downloaded");
    announce("Conversion complete", "success");
  } catch (error) {
    announce(error.message, "error");
  } finally {
    elements.download.disabled = false;
  }
}

async function loadFile(event) {
  const file = event.target.files[0];
  event.target.value = "";
  if (!file) return;
  const extensionAllowed = /\.(md|markdown|txt)$/iu.test(file.name);
  if (!extensionAllowed) return toast("Choose a .md, .markdown, or .txt file");
  if (file.size > MAX_FILE_BYTES) return toast("File must be 750 KB or smaller");
  try {
    elements.markdown.value = await file.text();
    elements.title.value = file.name.replace(/\.(md|markdown|txt)$/iu, "").slice(0, 200);
    await convertMarkdown();
    toast(`Loaded ${file.name}`);
  } catch (_error) {
    announce("The file could not be read.", "error");
  }
}

function clearEditor() {
  if (elements.markdown.value && !window.confirm("Clear the editor and saved draft?")) return;
  elements.markdown.value = "";
  elements.title.value = "Converted Document";
  localStorage.removeItem(STORAGE_KEY);
  convertMarkdown();
  elements.markdown.focus();
}

elements.markdown.addEventListener("input", scheduleConversion);
elements.title.addEventListener("input", scheduleConversion);
elements.theme.addEventListener("change", convertMarkdown);
elements.output.addEventListener("change", convertMarkdown);
elements.toc.addEventListener("change", convertMarkdown);
elements.upload.addEventListener("click", () => elements.file.click());
elements.file.addEventListener("change", loadFile);
elements.sample.addEventListener("click", () => { elements.markdown.value = SAMPLE; elements.title.value = "Publish-ready Markdown"; convertMarkdown(); });
elements.clear.addEventListener("click", clearEditor);
elements.copy.addEventListener("click", copyHtml);
elements.download.addEventListener("click", downloadHtml);
elements.previewTab.addEventListener("click", () => showView("preview"));
elements.sourceTab.addEventListener("click", () => showView("source"));

restoreDraft();
updateStats();
showView("preview");
convertMarkdown();
