// State
let allTasks = [];
let currentMonth = new Date().getMonth() + 1; // 1-12
let selectedMonth = currentMonth;
let searchQuery = "";
let selectedPhases = ["VOORZAAIEN", "DIRECTZAAIEN", "UITPLANTEN", "OOGSTEN"];

// DOM Elements
const searchInput = document.getElementById("searchInput");
const clearSearchBtn = document.getElementById("clearSearch");
const taskList = document.getElementById("taskList");
const statusMessage = document.getElementById("statusMessage");
const emptyState = document.getElementById("emptyState");
const btnVandaag = document.getElementById("btnVandaag");
const monthBtns = document.querySelectorAll(".month-btn");
const phaseCheckboxes = document.querySelectorAll(".phase-filter");

// Init
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    setupEventListeners();
    updateMonthButtons();
});

async function loadTasks() {
    try {
        const response = await fetch("taken.json");
        if (!response.ok) throw new Error("Kon taken niet laden");
        allTasks = await response.json();
        statusMessage.style.display = "none";
        renderTasks();
    } catch (error) {
        console.error(error);
        statusMessage.textContent = "Fout bij laden van taken. Controleer je verbinding.";
    }
}

function setupEventListeners() {
    // Search
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value.toLowerCase();
        toggleClearButton();
        renderTasks();
    });

    clearSearchBtn.addEventListener("click", () => {
        searchInput.value = "";
        searchQuery = "";
        toggleClearButton();
        renderTasks();
    });

    // Month Filters
    monthBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const month = parseInt(btn.dataset.month);
            if (selectedMonth === month) {
                // Toggle off? No, always enforce one month selection or 'all'?
                // For simplicity: click same month -> no change or toggle?
                // Construct: Click Month -> Select Month. Click Vandaag -> Select Current.
                return;
            }
            selectedMonth = month;
            updateMonthButtons();
            renderTasks();
        });
    });

    btnVandaag.addEventListener("click", () => {
        selectedMonth = currentMonth;
        updateMonthButtons();
        renderTasks();
    });

    // Phase Filters
    phaseCheckboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            selectedPhases = Array.from(phaseCheckboxes)
                .filter(c => c.checked)
                .map(c => c.value);
            renderTasks();
        });
    });

    // Reset filters
    document.getElementById("resetFilters").addEventListener("click", () => {
        searchInput.value = "";
        searchQuery = "";
        selectedMonth = currentMonth;
        selectedPhases = ["VOORZAAIEN", "DIRECTZAAIEN", "UITPLANTEN", "OOGSTEN"];
        phaseCheckboxes.forEach(c => c.checked = true);
        toggleClearButton();
        updateMonthButtons();
        renderTasks();
    });
}

function toggleClearButton() {
    if (searchQuery.length > 0) {
        clearSearchBtn.classList.remove("hidden");
    } else {
        clearSearchBtn.classList.add("hidden");
    }
}

function updateMonthButtons() {
    // Reset all
    monthBtns.forEach(btn => btn.classList.remove("active"));
    btnVandaag.classList.remove("active");

    if (selectedMonth === currentMonth) {
        btnVandaag.classList.add("active");
        // Also highlight the specific month button for clarity?
        const currentBtn = document.querySelector(`.month-btn[data-month="${currentMonth}"]`);
        if (currentBtn) currentBtn.classList.add("active");
    } else {
        const btn = document.querySelector(`.month-btn[data-month="${selectedMonth}"]`);
        if (btn) btn.classList.add("active");
    }
}

function renderTasks() {
    // Filter
    const filtered = allTasks.filter(task => {
        // 1. Search (matches vegetable name OR month name)
        const matchesSearch = !searchQuery ||
            task.groente.toLowerCase().includes(searchQuery) ||
            task.maand.toLowerCase().includes(searchQuery);

        if (!matchesSearch) return false;

        // 2. Month (if NO search query is active, strict month filter. 
        //    If search query IS active, maybe show all matches regardless of month? 
        //    User requirement: "Zoekfunctie razendsnel door 1000 items".
        //    Interaction design: Usually search overrides filters.
        //    Let's make search OVERRIDE month filter, but Phase filter always applies.)

        const matchesMonth = searchQuery ? true : (task.maand_nr === selectedMonth);

        // 3. Phase
        const matchesPhase = selectedPhases.includes(task.fase.toUpperCase());

        return matchesMonth && matchesPhase;
    });

    // Sort (already sorted by JSON generation, but good to ensure)
    // Render
    taskList.innerHTML = "";

    if (filtered.length === 0) {
        emptyState.classList.remove("hidden");
    } else {
        emptyState.classList.add("hidden");

        // Limit rendering for performance if massive (unlikely with 1000 items but good practice)
        // const subset = filtered.slice(0, 100); 

        filtered.forEach(task => {
            const card = createTaskCard(task);
            taskList.appendChild(card);
        });

        // Helper text
        if (searchQuery) {
            const countInfo = document.createElement("div");
            countInfo.className = "col-span-full text-center text-gray-400 text-sm mb-2";
            countInfo.textContent = `${filtered.length} zoekresultaten`;
            taskList.prepend(countInfo);
        }
    }
}

function createTaskCard(task) {
    const div = document.createElement("div");
    div.className = `task-card bg-gray-800 rounded-xl p-4 shadow-lg flex items-center space-x-4 phase-${task.fase.toUpperCase()}`;

    // Icon
    const img = document.createElement("img");
    img.src = `icons/${task.icoon}`;
    img.alt = task.groente;
    img.className = "w-16 h-16 object-contain vegetable-icon";
    img.onerror = () => { img.src = "icons/Default.png"; }; // Fallback

    // Content
    const content = document.createElement("div");
    content.className = "flex-1 min-w-0";

    const header = document.createElement("div");
    header.className = "flex justify-between items-start";

    const title = document.createElement("h3");
    title.className = "text-xl font-bold text-white truncate";
    title.textContent = task.groente;

    const badge = document.createElement("span");
    badge.className = `px-2 py-1 rounded text-xs font-bold uppercase tracking-wide 
        ${getPhaseColor(task.fase)}`;
    badge.textContent = task.fase;

    header.appendChild(title);
    header.appendChild(badge);

    const meta = document.createElement("p");
    meta.className = "text-green-400 text-sm font-semibold mt-1";
    meta.textContent = `${task.maand} (${task.weken_display})`;

    const desc = document.createElement("p");
    desc.className = "text-gray-400 text-sm mt-1 line-clamp-2 leading-relaxed";
    desc.textContent = task.beschrijving;

    // Tip (optioneel expandable maken?)
    // const tip = document.createElement("p");
    // tip.className = "text-gray-500 text-xs mt-2 italic";
    // tip.textContent = "💡 " + task.tip;

    content.appendChild(header);
    content.appendChild(meta);
    content.appendChild(desc);
    // content.appendChild(tip);

    div.appendChild(img);
    div.appendChild(content);

    return div;
}

function getPhaseColor(fase) {
    switch (fase.toUpperCase()) {
        case "VOORZAAIEN": return "bg-blue-900 text-blue-200";
        case "DIRECTZAAIEN": return "bg-yellow-900 text-yellow-200";
        case "UITPLANTEN": return "bg-green-900 text-green-200";
        case "OOGSTEN": return "bg-red-900 text-red-200";
        default: return "bg-gray-700 text-gray-300";
    }
}
