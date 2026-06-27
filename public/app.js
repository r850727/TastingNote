// elements
const wineList = document.getElementById("wine-list");
const categoryTabs = document.getElementById("category-tabs");
const filters = document.getElementById("filters");
const sorts = document.getElementById("sorts");
const countLabel = document.getElementById("count-label");

// stats
const statTotal = document.getElementById("stat-total");
const statAvg = document.getElementById("stat-avg");
const statWhisky = document.getElementById("stat-whisky");
const statFruit = document.getElementById("stat-fruit");
const statSake = document.getElementById("stat-sake");
const statSpirits = document.getElementById("stat-spirits");
const statWine = document.getElementById("stat-wine");
const statsRow2 = document.getElementById("stats-row-2");
const sakeLegend = document.getElementById("sake-legend");

// modal
const wineModal = document.getElementById("wine-modal");
const modalBody = document.getElementById("modal-body");
const modalClose = document.getElementById("modal-close");

// cart
const cartBar = document.getElementById("cart-bar");
const cartHeader = document.getElementById("cart-header");
const cartToggle = document.getElementById("cart-toggle");
const cartBody = document.getElementById("cart-body");
const cartItems = document.getElementById("cart-items");
const cartCount = document.getElementById("cart-count");

// state
let currentCat = "All";
let currentFilter = "all";
let currentSort = "default";
let cart = new Set(); // store ids

const JPY_TO_TWD = 0.21; // 匯率設定

function getTwdPrice(w) {
  return w.currency === 'TWD' ? w.price : w.price * JPY_TO_TWD;
}

function formatPriceHtml(w) {
  if (w.currency === 'TWD') {
    return `NT$${w.price.toLocaleString()}`;
  } else {
    const twd = Math.round(w.price * JPY_TO_TWD);
    if (w.category && w.category.includes('清酒')) {
      return `¥${w.price.toLocaleString()} <span style="font-size:0.85em; opacity:0.7;">(NT$${twd.toLocaleString()})</span>`;
    } else {
      return `NT$${twd.toLocaleString()} <span style="font-size:0.85em; opacity:0.7;">(¥${w.price.toLocaleString()})</span>`;
    }
  }
}

// extract categories
const categories = ["All", ...new Set(wineData.map(w => w.category))];

const categoryFilters = {
  "威士忌": [
    { label: "全部", filter: "all" },
    { label: "單一麥芽威士忌", filter: "tag-單一麥芽威士忌" },
    { label: "調和威士忌", filter: "tag-調和威士忌" }
  ],
  "果實酒": [
    { label: "全部", filter: "all" },
    { label: "梅酒", filter: "tag-梅酒" }
  ],
  "清酒": [
    { label: "全部", filter: "all" },
    { label: "Saketime Top 10", filter: "rank-S+" },
    { label: "Saketime Top 20", filter: "rank-S" },
    { label: "Saketime Top 50", filter: "rank-A" },
    { label: "Saketime Top 100", filter: "rank-B" },
    { label: "知名銘柄", filter: "rank-C" }
  ],
  "烈酒": [
    { label: "全部", filter: "all" },
    { label: "蘭姆酒", filter: "tag-蘭姆酒" },
    { label: "高粱", filter: "tag-高粱" },
    { label: "琴酒", filter: "tag-琴酒" }
  ],
  "葡萄酒": [
    { label: "全部", filter: "all" },
    { label: "氣泡酒", filter: "tag-氣泡酒" },
    { label: "白酒", filter: "tag-白酒" },
    { label: "紅酒", filter: "tag-紅酒" },
    { label: "香檳", filter: "tag-香檳" }
  ],
  "All": []
};

function renderFilters() {
  const filterList = categoryFilters[currentCat] || [];
  
  if (filterList.length === 0) {
    filters.style.display = "none";
  } else {
    filters.style.display = "flex";
    filters.innerHTML = filterList.map(f => 
      `<button class="fbtn ${f.filter === currentFilter ? 'active' : ''}" data-filter="${f.filter}">${f.label}</button>`
    ).join('');
  }
}

const defaultSorts = [
  { label: "預設排序", sort: "default" },
  { label: "價格高→低", sort: "price-desc" },
  { label: "價格低→高", sort: "price-asc" }
];

const sakeSorts = [
  ...defaultSorts,
  { label: "評級高→低", sort: "rank-desc" },
  { label: "評級低→高", sort: "rank-asc" }
];

function renderSorts() {
  const sortListToUse = currentCat === "清酒" ? sakeSorts : defaultSorts;
  
  if (!sortListToUse.some(s => s.sort === currentSort)) {
    currentSort = "default";
  }

  sorts.innerHTML = sortListToUse.map(s => 
    `<button class="fbtn ${s.sort === currentSort ? 'active' : ''}" data-sort="${s.sort}">${s.label}</button>`
  ).join('');
}

function init() {
  renderTabs();
  renderFilters();
  renderSorts();
  bindEvents();
  updateView();
}

function renderTabs() {
  categoryTabs.innerHTML = categories.map(cat => 
    `<button class="type-tab ${cat === currentCat ? 'active' : ''}" data-cat="${cat}">${cat === 'All' ? '全部' : cat}</button>`
  ).join("");
  
  categoryTabs.querySelectorAll('.type-tab').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.type-tab').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentCat = e.target.dataset.cat;
      // Reset filter on category change
      currentFilter = "all";
      renderFilters();
      renderSorts();
      
      updateView();
    });
  });
}

function bindEvents() {
  // filters
  filters.addEventListener('click', (e) => {
    if(e.target.tagName === 'BUTTON') {
      filters.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentFilter = e.target.dataset.filter;
      updateView();
    }
  });

  // sorts
  sorts.addEventListener('click', (e) => {
    if(e.target.tagName === 'BUTTON') {
      sorts.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentSort = e.target.dataset.sort;
      updateView();
    }
  });

  // modal close
  modalClose.addEventListener('click', () => {
    wineModal.classList.remove('open');
  });
  wineModal.addEventListener('click', (e) => {
    if(e.target === wineModal) wineModal.classList.remove('open');
  });

  // cart toggle
  cartHeader.addEventListener('click', () => {
    cartBody.classList.toggle('open');
    cartToggle.classList.toggle('open');
  });
  
  // add wine tool
  const addCat = document.getElementById("add-cat");
  const addTag = document.getElementById("add-tag");
  const addRankContainer = document.getElementById("add-rank-container");

  const addCategoryTags = {
    "清酒": ["吟釀", "大吟釀", "氣泡清酒", "本釀造", "純米酒", "特別純米", "純米吟釀", "純米大吟釀", "生酒", "山廢", "生酛", "貴釀酒", "無特定名稱 / 非公開"],
    "葡萄酒": ["氣泡酒", "白酒", "紅酒", "香檳"],
    "威士忌": ["單一麥芽威士忌", "調和威士忌"],
    "琴酒": ["琴酒"],
    "果實酒": ["柚子酒", "梅酒"],
    "烈酒": ["蘭姆酒", "高粱", "琴酒"],
    "其他": ["其他"]
  };

  function updateAddModal() {
    const cat = addCat.value;
    const tags = addCategoryTags[cat] || [];
    addTag.innerHTML = tags.map(t => `<option value="${t}">${t}</option>`).join('');
    addRankContainer.style.display = cat === "清酒" ? "block" : "none";
  }

  addCat.addEventListener('change', updateAddModal);

  let selectedCurrency = "JPY";
  const btnJpy = document.getElementById("btn-currency-jpy");
  const btnTwd = document.getElementById("btn-currency-twd");

  btnJpy.addEventListener("click", () => {
    selectedCurrency = "JPY";
    btnJpy.classList.add("active");
    btnTwd.classList.remove("active");
  });

  btnTwd.addEventListener("click", () => {
    selectedCurrency = "TWD";
    btnTwd.classList.add("active");
    btnJpy.classList.remove("active");
  });

  document.getElementById("btn-add-wine").addEventListener('click', () => {
    updateAddModal();
    document.getElementById("add-modal").classList.add('open');
  });
  document.getElementById("add-modal-close").addEventListener('click', () => {
    document.getElementById("add-modal").classList.remove('open');
  });
  document.getElementById("add-generate").addEventListener('click', () => {
    const name = document.getElementById("add-name").value;
    const cat = document.getElementById("add-cat").value;
    const tag = document.getElementById("add-tag").value;
    const priceRaw = document.getElementById("add-price").value.trim() || "0";
    const price = parseInt(priceRaw.replace(/[^\d]/g, '')) || 0;

    const img = document.getElementById("add-img").value;
    const rank = document.getElementById("add-rank").value;
    
    const obj = {
      id: wineData.length + 1,
      category: cat,
      tag: tag,
      name: name,
      image: `./images/${img}`,
      price: price,
      currency: selectedCurrency
    };
    if (cat === "清酒") {
      obj.saketime_rank = rank;
    }

    
    const str = JSON.stringify(obj, null, 2) + ",";
    document.getElementById("add-result").value = str;
    navigator.clipboard.writeText(str).then(() => {
      alert("已產生並複製到剪貼簿！請貼上到 data.js 檔案中。");
    });
  });
}

function getFilteredData() {
  let list = wineData;
  
  if(currentCat !== "All") {
    list = list.filter(w => w.category === currentCat);
  }
  
  if(currentFilter !== "all") {
    if(currentFilter.startsWith("rank-")) {
      const rank = currentFilter.split('-')[1];
      list = list.filter(w => w.saketime_rank === rank);
    } else if(currentFilter.startsWith("tag-")) {
      const tag = currentFilter.split('-')[1];
      list = list.filter(w => w.tag && w.tag.includes(tag));
    }
  }
  
  list = [...list]; // clone for sorting
  
  const rankWeight = {
    "S+": 5,
    "S": 4,
    "A": 3,
    "B": 2,
    "C": 1,
    "-": 0,
    "": 0,
    undefined: 0
  };

  if(currentSort === "price-desc") {
    list.sort((a, b) => getTwdPrice(b) - getTwdPrice(a));
  } else if(currentSort === "price-asc") {
    list.sort((a, b) => getTwdPrice(a) - getTwdPrice(b));
  } else if(currentSort === "rank-desc") {
    list.sort((a, b) => rankWeight[b.saketime_rank] - rankWeight[a.saketime_rank]);
  } else if(currentSort === "rank-asc") {
    list.sort((a, b) => rankWeight[a.saketime_rank] - rankWeight[b.saketime_rank]);
  } else {
    list.sort((a, b) => a.id - b.id); // default
  }
  
  return list;
}

function updateView() {
  const list = getFilteredData();
  
  // Show/hide legend based on category
  sakeLegend.style.display = currentCat === "清酒" ? "block" : "none";
  
  renderList(list);
  updateStats(list);
}

function getRankClass(rank) {
  if(!rank || rank === "-") return "none";
  return rank.toLowerCase().replace('+', 'p'); // handling S+ as sp in css
}

function renderList(list) {
  countLabel.textContent = `顯示 ${list.length} 筆酒款`;
  
  if(list.length === 0) {
    wineList.innerHTML = `<p style="text-align:center; color:var(--t3); padding:40px;">找不到符合條件的酒款</p>`;
    return;
  }
  
  wineList.innerHTML = list.map(w => {
    const rankCls = getRankClass(w.saketime_rank);
    const inCart = cart.has(w.id);
    return `
      <div class="wine-card rank-${w.saketime_rank}" data-id="${w.id}">

        <div class="wc-info">
          <div class="wc-name" title="${w.name}">${w.name}</div>
          <div class="wc-meta">
            ${w.saketime_rank && w.saketime_rank !== '-' ? `<span class="badge ${rankCls}">${w.saketime_rank}</span>` : ''}
            <span class="badge none">${w.tag}</span>
            <span class="wc-price">${formatPriceHtml(w)}</span>
          </div>
        </div>
        <button class="wc-fav-btn ${inCart ? 'active' : ''}" data-id="${w.id}">
          ${inCart ? '♥' : '♡'}
        </button>
      </div>
    `;
  }).join('');
  
  // Bind card clicks
  wineList.querySelectorAll('.wine-card').forEach(card => {
    card.addEventListener('click', (e) => {
      // Don't open modal if clicked on fav button
      if(e.target.closest('.wc-fav-btn')) return;
      
      const id = parseInt(card.dataset.id);
      openModal(id);
    });
  });
  
  wineList.querySelectorAll('.wc-fav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = parseInt(btn.dataset.id);
      toggleCart(id);
    });
  });
}

function openModal(id) {
  const w = wineData.find(x => x.id === id);
  if(!w) return;
  
  const rankCls = getRankClass(w.saketime_rank);
  
  modalBody.innerHTML = `
    <div class="modal-img-container">
      <img src="${w.image}" class="modal-img" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' fill=\\'%2321262d\\'><rect width=\\'100%\\' height=\\'100%\\'/></svg>'">
    </div>
    <div class="modal-info">
      <div class="modal-tags">
        ${w.saketime_rank && w.saketime_rank !== '-' ? `<span class="badge ${rankCls}">${w.saketime_rank}</span>` : ''}
        <span class="badge none">${w.category}</span>
        <span class="badge none">${w.tag}</span>
      </div>
      <h3 class="modal-title">${w.name}</h3>
      <div class="modal-price">
        ${formatPriceHtml(w)}
      </div>
      ${w.note ? `<div class="modal-note">${w.note}</div>` : ''}
    </div>
  `;
  
  wineModal.classList.add('open');
}

function updateStats(list) {
  statsRow2.style.display = currentCat === "All" ? "flex" : "none";

  statTotal.textContent = list.length;
  
  const validList = list.filter(w => w.price > 0);
  if(validList.length > 0) {
    if (currentCat === "清酒") {
      const jpyPrices = validList.map(w => w.currency === 'JPY' ? w.price : w.price / JPY_TO_TWD);
      const sum = jpyPrices.reduce((a, b) => a + b, 0);
      statAvg.textContent = `¥${Math.round(sum / validList.length).toLocaleString()}`;
    } else {
      const twdPrices = validList.map(w => getTwdPrice(w));
      const sum = twdPrices.reduce((a, b) => a + b, 0);
      statAvg.textContent = `NT$${Math.round(sum / validList.length).toLocaleString()}`;
    }
  } else {
    statAvg.textContent = "-";
  }
  
  statWhisky.textContent = list.filter(w => w.category.includes('威士忌')).length;
  statFruit.textContent = list.filter(w => w.category.includes('果實酒')).length;
  statSake.textContent = list.filter(w => w.category.includes('清酒')).length;
  statSpirits.textContent = list.filter(w => w.category.includes('烈酒')).length;
  statWine.textContent = list.filter(w => w.category.includes('葡萄酒')).length;
}

function toggleCart(id) {
  if(cart.has(id)) {
    cart.delete(id);
  } else {
    cart.add(id);
  }
  
  // Re-render buttons
  document.querySelectorAll(`.wc-fav-btn[data-id="${id}"]`).forEach(btn => {
    btn.classList.toggle('active');
    btn.innerHTML = cart.has(id) ? '♥' : '♡';
  });
  
  updateCartView();
}

function updateCartView() {
  if(cart.size > 0) {
    cartBar.classList.remove('hidden');
  } else {
    cartBar.classList.add('hidden');
    cartBody.classList.remove('open');
    cartToggle.classList.remove('open');
  }
  
  cartCount.textContent = cart.size;
  
  const items = Array.from(cart).map(id => wineData.find(w => w.id === id)).filter(Boolean);
  
  cartItems.innerHTML = items.map(w => `
    <div class="cart-item">
      <div class="cart-item-info">
        <div class="cart-item-name">${w.name}</div>
        <div style="font-size: 11px; color: var(--t2);">${formatPriceHtml(w)}</div>
      </div>
      <button class="cart-item-rm" data-id="${w.id}">×</button>
    </div>
  `).join('');
  
  cartItems.querySelectorAll('.cart-item-rm').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCart(parseInt(btn.dataset.id));
    });
  });
}

// start
init();
