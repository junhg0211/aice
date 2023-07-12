// noinspection JSUnresolvedReference

const packsList = document.getElementById('packs-list');
const abbreviationsList = document.getElementById('abbreviations-list');

window.addEventListener('pywebviewready', () => {
    loadPacks();
});

function loadPacks() {
    pywebview.api.get_packs().then(packs => {
        packs.forEach(pack => {
            const packItem = document.createElement('a');
            packItem.classList.add('nav-link');
            packItem.href = '#';
            packItem.innerText = pack;
            packItem.addEventListener('click', () => {
                setPack(pack);
            });
            packsList.appendChild(packItem);
        });
    });
}

function setPack(packName) {
    // update abbreviations list
    abbreviationsList.innerHTML = '';
    pywebview.api.get_pack_abbreviations(packName).then(abbreviations => {
        abbreviations.forEach((entry, _) => {
            const [key, value] = entry;

            const row = document.createElement('tr');

            const abbreviation = document.createElement('td');
            abbreviation.innerText = key;
            row.appendChild(abbreviation);

            const meaning = document.createElement('td');
            meaning.innerText = value;
            row.appendChild(meaning);

            abbreviationsList.appendChild(row);
        });
    });

    // update active pack
    packsList.querySelectorAll('a').forEach(a => {
        a.classList.remove('active');
        if (a.innerText === packName) {
            a.classList.add('active');
        }
    });
}
