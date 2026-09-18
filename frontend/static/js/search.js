document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.getElementById('filter-form');
    const resultsContainer = document.getElementById('room-results');

    if (!filterForm || !resultsContainer) return;

    function fetchResults(params) {
        const url = `${window.location.pathname}?${params.toString()}`;
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then((res) => res.json())
            .then((data) => {
                resultsContainer.innerHTML = data.html;
                history.pushState(null, '', url);
                const countEl = document.querySelector('.results-header h2');
                if (countEl) countEl.textContent = `${data.count} rooms found`;
            })
            .catch((err) => console.error('Search failed:', err));
    }

    // Filter form submit (dropdowns, checkboxes, price range)
    filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(filterForm));
        fetchResults(params);
    });

    // Auto-apply filters immediately when a select/checkbox changes
    filterForm.querySelectorAll('select, input[type="checkbox"]').forEach((el) => {
        el.addEventListener('change', function () {
            const params = new URLSearchParams(new FormData(filterForm));
            fetchResults(params);
        });
    });

    // Debounced live text search
    const searchInput = document.getElementById('q-input');
    if (searchInput) {
        let timer;
        searchInput.addEventListener('input', function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                const params = new URLSearchParams(new FormData(filterForm));
                fetchResults(params);
            }, 400);
        });
    }
});
