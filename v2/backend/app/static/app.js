const PAGE_SIZE = 20;
let offset = 0;
let total = 0;

const entriesNode = document.querySelector("#entries");
const statusNode = document.querySelector("#status");
const summaryNode = document.querySelector("#summary");
const pageLabel = document.querySelector("#page-label");
const previousButton = document.querySelector("#previous");
const nextButton = document.querySelector("#next");
const filters = document.querySelector("#filters");

function apiParams() {
  const params = new URLSearchParams({limit: String(PAGE_SIZE), offset: String(offset)});
  const q = document.querySelector("#query").value.trim();
  const dateFrom = document.querySelector("#date-from").value;
  const dateTo = document.querySelector("#date-to").value;
  if (q) params.set("q", q);
  if (dateFrom) params.set("date_from", dateFrom);
  if (dateTo) params.set("date_to", dateTo);
  return params;
}

function imageUrl(ref) {
  return `/api/images/${encodeURIComponent(ref)}`;
}

function renderEntry(entry) {
  const fragment = document.querySelector("#entry-template").content.cloneNode(true);
  fragment.querySelector("time").textContent = entry.entry_date;
  const source = fragment.querySelector(".source");
  if (entry.source) source.textContent = entry.source;
  else source.remove();
  fragment.querySelector(".entry-text").textContent = entry.text || "(내용 없음)";

  const images = fragment.querySelector(".images");
  for (const ref of entry.image_refs || []) {
    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = `${entry.entry_date} 첨부 이미지`;
    img.src = imageUrl(ref);
    img.addEventListener("error", () => {
      const message = document.createElement("span");
      message.className = "image-error";
      message.textContent = "이미지 파일을 불러오지 못했습니다.";
      img.replaceWith(message);
    });
    images.append(img);
  }
  entriesNode.append(fragment);
}

function updatePager() {
  const page = total ? Math.floor(offset / PAGE_SIZE) + 1 : 0;
  const pages = total ? Math.ceil(total / PAGE_SIZE) : 0;
  pageLabel.textContent = `${page} / ${pages}`;
  previousButton.disabled = offset === 0;
  nextButton.disabled = offset + PAGE_SIZE >= total;
}

async function loadStats() {
  try {
    const response = await fetch("/api/stats");
    if (!response.ok) return;
    const stats = await response.json();
    summaryNode.textContent = `일기 ${stats.entries.toLocaleString("ko-KR")}편 · 사진 ${stats.images.toLocaleString("ko-KR")}장`;
  } catch (_) {
    summaryNode.textContent = "나의 기록";
  }
}

async function loadEntries() {
  statusNode.className = "status";
  statusNode.textContent = "불러오는 중입니다…";
  previousButton.disabled = true;
  nextButton.disabled = true;
  try {
    const response = await fetch(`/api/entries?${apiParams()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    total = data.total;
    entriesNode.replaceChildren();
    for (const entry of data.entries) renderEntry(entry);
    statusNode.textContent = total ? `검색 결과 ${total.toLocaleString("ko-KR")}편` : "조건에 맞는 일기가 없습니다.";
    updatePager();
    window.scrollTo({top: 0, behavior: "smooth"});
  } catch (error) {
    entriesNode.replaceChildren();
    statusNode.className = "status error";
    statusNode.textContent = `일기를 불러오지 못했습니다. (${error.message})`;
  }
}

filters.addEventListener("submit", (event) => {
  event.preventDefault();
  offset = 0;
  loadEntries();
});

document.querySelector("#reset").addEventListener("click", () => {
  filters.reset();
  offset = 0;
  loadEntries();
});

previousButton.addEventListener("click", () => {
  offset = Math.max(0, offset - PAGE_SIZE);
  loadEntries();
});

nextButton.addEventListener("click", () => {
  offset += PAGE_SIZE;
  loadEntries();
});

loadStats();
loadEntries();
