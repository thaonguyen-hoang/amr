// Script to handle multi-item annotation across two pages (index.html and adequacy.html)
(() => {
    // Replace this with your data source or load via fetch
    const items = [
        { id: 'item1', sentence: 'Go, China, go', amr: `(g / go-01 :mode imperative\n    :ARG1 (c / country :wiki "China" :name (n / name :op1 "China")))` },
        { id: 'item2', sentence: 'She ate the apple', amr: `(e / eat-01 :ARG0 (s / she) :ARG1 (a / apple))` },
        { id: 'item3', sentence: 'He runs quickly', amr: `(r / run-01 :ARG0 (h / he) :manner (q / quickly))` }
    ];

    // Utilities
    function qsParam(name){
        const params = new URLSearchParams(location.search);
        return params.has(name) ? params.get(name) : null;
    }
    function setQsParam(name, value){
        const params = new URLSearchParams(location.search);
        params.set(name, String(value));
        history.replaceState(null, '', `${location.pathname}?${params.toString()}`);
    }

    function keyFor(itemId, field){
        return `amr.${itemId}.${field}`;
    }

    // Position-based navigation: pos ranges 0 .. (2*items.length - 1)
    // even pos -> fluency for item (pos/2)
    // odd pos  -> adequacy for item (floor(pos/2))
    const totalSteps = items.length * 2;

    function getPos(){
        const raw = qsParam('pos');
        const n = raw === null ? 0 : parseInt(raw,10);
        if(Number.isNaN(n) || n < 0) return 0;
        return Math.min(Math.max(0, n), totalSteps - 1);
    }

    function setPos(pos){
        const p = Math.min(Math.max(0, pos), totalSteps - 1);
        setQsParam('pos', p);
        return p;
    }

    function populatePage(){
        const pos = getPos();
        const itemIdx = Math.floor(pos / 2);
        const it = items[itemIdx];
        if(!it) return;

        // If elements exist on page, populate them
        const utteranceEls = document.querySelectorAll('#utterance');
        utteranceEls.forEach(el => el.textContent = it.sentence);

        const amrEl = document.getElementById('amrPre');
        if(amrEl) amrEl.textContent = it.amr;

        // sliders
        const fluency = document.getElementById('fluencySlider');
        const fluVal = document.getElementById('fluencyValue');
        const adequacy = document.getElementById('adequacySlider');
        const adeVal = document.getElementById('adequacyValue');

        const savedF = localStorage.getItem(keyFor(it.id,'fluency'));
        if(fluency){
            if(savedF !== null) fluency.value = savedF;
            if(fluVal) fluVal.textContent = fluency.value;
            fluency.oninput = () => { if(fluVal) fluVal.textContent = fluency.value; localStorage.setItem(keyFor(it.id,'fluency'), fluency.value); };
        }

        const savedA = localStorage.getItem(keyFor(it.id,'adequacy'));
        if(adequacy){
            if(savedA !== null) adequacy.value = savedA;
            if(adeVal) adeVal.textContent = adequacy.value;
            adequacy.oninput = () => { if(adeVal) adeVal.textContent = adequacy.value; localStorage.setItem(keyFor(it.id,'adequacy'), adequacy.value); };
        }

        // checkboxes
        ['p1','p2','p3'].forEach(id => {
            const el = document.getElementById(id);
            if(!el) return;
            const sv = localStorage.getItem(keyFor(it.id,id));
            el.checked = (sv === 'true');
            el.onchange = () => localStorage.setItem(keyFor(it.id,id), el.checked);
        });

        // navigation controls
        const progress = document.getElementById('progress');
        if(progress) {
            const stage = (pos % 2 === 0) ? 'Fluency' : 'Adequacy';
            progress.textContent = `item ${itemIdx+1} / ${items.length} — ${stage}`;
        }

        // update progress bar fill (if present)
        const progressBarFill = document.getElementById('progressBarFill');
        if(progressBarFill) {
            const pct = Math.round(((itemIdx + 1) / items.length) * 100);
            progressBarFill.style.width = pct + '%';
            // update accessible attribute if present on parent
            const parent = progressBarFill.parentElement;
            if(parent) parent.setAttribute('aria-valuenow', String(pct));
        }

        const prevItem = document.getElementById('prevItem');
        const nextItem = document.getElementById('nextItem');
        const toAdequacy = document.getElementById('toAdequacy');
        const toFluency = document.getElementById('toFluency');

        if(prevItem) prevItem.onclick = () => { const ni = setPos(pos - 1); const page = (ni % 2 === 0) ? 'index.html' : 'adequacy.html'; location.href = page + '?pos=' + ni; };
        if(nextItem) nextItem.onclick = () => { const ni = setPos(pos + 1); const page = (ni % 2 === 0) ? 'index.html' : 'adequacy.html'; location.href = page + '?pos=' + ni; };

        if(toAdequacy) toAdequacy.onclick = () => { const target = itemIdx*2 + 1; location.href = 'adequacy.html?pos=' + target; };
        if(toFluency) toFluency.onclick = () => { const target = itemIdx*2; location.href = 'index.html?pos=' + target; };
    }

    // Populate on load
    if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', populatePage);
    else populatePage();

})();