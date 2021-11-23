const down = document.getElementById("down");
const packsList = document.getElementById("packs-list");
const description = document.getElementById("description");

function applyLanguage(language) {
    // todo
}

function closeWindow() {
    window.close();
}
eel.expose(closeWindow);

function requestLanguage() {  // todo with applyLanguage()
    // noinspection JSUnresolvedFunction
    eel._get_language()().then((data) => {
        applyLanguage(data);
    });
}

function apply(packName, keyword) {
    let key = document.getElementById(`${packName}-${keyword}-key`);
    let term = document.getElementById(`${packName}-${keyword}-term`);
    let edit_ = document.getElementById(`${packName}-${keyword}-edit`);
    let del = document.getElementById(`${packName}-${keyword}-delete`);

    let keyInput = document.getElementById(`${packName}-${keyword}-key-input`);
    let termInput = document.getElementById(`${packName}-${keyword}-term-input`);

    let rawKey = keyInput.value;
    let rawTerm = termInput.value;

    key.innerText = rawKey;
    term.innerText = rawTerm;

    edit_.innerText = "edit";
    edit_.onclick = () => edit(packName, rawKey);
    edit_.colSpan = 1;

    del.style.display = "";

    key.id = `${packName}-${rawKey}-key`;
    term.id = `${packName}-${rawKey}-term`;
    edit_.id = `${packName}-${rawKey}-edit`;
    del.id = `${packName}-${rawKey}-delete`;

    // noinspection JSUnresolvedFunction
    eel._edit_key(packName, keyword, rawKey, rawTerm)();
}

function edit(packName, keyword) { // todo
}

function add(packName) { // todo
}

function remove(packName, keyword) {
    let table = document.getElementById(`${packName}-table`);
    let tr = document.getElementById(`${packName}-${keyword}-tr`);

    table.removeChild(tr);
    // noinspection JSUnresolvedFunction
    eel._delete_abbreviation(packName, keyword)();
}

function toggleHide(packName) {
    let table = document.getElementById(`${packName}-table`);
    let h3 = document.getElementById(`${packName}-h3`);
    let span = document.getElementById(`${packName}-toggle-switch`);
    if (table.style.display === "") {
        table.style.display = "none";
        span.style.display = "none";
        h3.innerText = `▶ ${packName}`;
    } else {
        table.style.display = "";
        span.style.display = "";
        h3.innerText = `▼ ${packName}`;
    }
}

function togglePack(packName) {
    let span = document.getElementById(`${packName}-toggle-switch`);
    let h3 = document.getElementById(`${packName}-h3`);
    if (span.innerText === "enabled") {
        span.innerText = "disabled";
        // noinspection JSUnresolvedFunction
        eel._disable_pack(packName)();
        h3.style.opacity = "0.5";
    } else {
        span.innerText = "enabled";
        // noinspection JSUnresolvedFunction
        eel._enable_pack(packName)();
        h3.style.opacity = "1";
    }
}

function requestPackList() {
    // noinspection JSUnresolvedFunction
    eel._get_pack_list()().then(packs => {
        packs.forEach(packName => {
            // noinspection JSUnresolvedFunction
            eel._get_pack_data(packName)().then(pack => {
                let h3 = document.createElement("h3");
                h3.innerText = `▶ ${packName}`;
                h3.id = `${packName}-h3`
                h3.onclick = () => toggleHide(packName);
                h3.style.cursor = "pointer";
                down.appendChild(h3);

                let span = document.createElement("span");
                span.innerText = "enabled";
                span.id = `${packName}-toggle-switch`;
                span.style.cursor = "pointer";
                span.onclick = () => togglePack(packName);
                down.appendChild(span);

                let table = document.createElement("table");
                table.id = `${packName}-table`;

                let tr = document.createElement("tr");
                let td = document.createElement("td");
                td.colSpan = 4;
                td.innerText = "+";
                td.onclick = () => add(packName);
                td.style.textAlign = "center";
                td.style.cursor = "pointer";
                tr.appendChild(td);
                table.appendChild(tr);

                for (let datum in pack) {
                    if (pack.hasOwnProperty(datum)) {
                        tr = document.createElement("tr");
                        tr.id = `${packName}-${datum}-tr`;

                        let td = document.createElement("td");
                        td.innerText = datum;
                        td.id = `${packName}-${datum}-key`;
                        tr.appendChild(td);

                        td = document.createElement("td");
                        td.innerText = pack[datum];
                        td.id = `${packName}-${datum}-term`;
                        tr.appendChild(td);

                        td = document.createElement("td");
                        td.onclick = () => edit(packName, datum);
                        td.innerText = "edit";
                        td.id = `${packName}-${datum}-edit`;
                        tr.appendChild(td)

                        td = document.createElement("td");
                        td.onclick = () => remove(packName, datum);
                        td.innerText = "delete";
                        td.id = `${packName}-${datum}-delete`;
                        tr.appendChild(td);

                        table.appendChild(tr);
                    }
                }

                down.appendChild(table);
                toggleHide(packName);

                let li = document.createElement("li");
                li.innerText = packName;
                li.onclick = () => h3.scrollIntoView();
                li.style.cursor = "pointer";
                packsList.appendChild(li);
            });
        });
    });
}

requestPackList()

function refreshAbbreviationCount() {
    // noinspection JSUnresolvedFunction
    eel._get_pack_count()().then(
        packCount => eel._get_available_abbreviation_count()().then(
            abbreviationCount => { description.innerText = `${packCount}개의 팩, ${abbreviationCount}개의 상용구가 준비되어있습니다.`; }
        )
    );
}
refreshAbbreviationCount();