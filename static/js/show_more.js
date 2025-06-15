document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('#demandesList .hidden');
    const showMoreBtn = document.getElementById('showMoreBtn');
    let visibleRows = 3; // Number of rows to show initially or each time button is clicked
    if (visibleRows >= rows.length) {
        showMoreBtn.style.display = 'none';
    }
    function showRows() {
        for (let i = 0; i < visibleRows; i++) {
            if (rows[i]) {
                rows[i].classList.remove('hidden');
            }
        }
    }

    showRows();

    showMoreBtn.addEventListener('click', function () {
        visibleRows += 7; 
        showRows();


        if (visibleRows >= rows.length) {
            showMoreBtn.style.display = 'none';
        }
    });
});
