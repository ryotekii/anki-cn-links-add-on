let popup = null;


function isChineseCharacter(char) {
    return /[\u3400-\u4DBF\u4E00-\u9FFF]/.test(char);
}


function makeCharactersHoverable() {
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT
    );

    const textNodes = [];

    while (walker.nextNode()) {
        textNodes.push(walker.currentNode);
    }

    for (const textNode of textNodes) {
        const parent = textNode.parentElement;

        if (
            parent &&
            parent.closest(".cn-links-character")
        ) {
            continue;
        }

        const text = textNode.nodeValue;

        if (!text) {
            continue;
        }

        if (![...text].some(isChineseCharacter)) {
            continue;
        }

        const fragment = document.createDocumentFragment();

        for (const char of text) {
            if (isChineseCharacter(char)) {
                const span = document.createElement("span");

                span.textContent = char;
                span.className = "cn-links-character";

                addCharacterHover(span);

                fragment.appendChild(span);
            } else {
                fragment.appendChild(
                    document.createTextNode(char)
                );
            }
        }

        textNode.parentNode.replaceChild(
            fragment,
            textNode
        );
    }
}


function addCharacterHover(character) {
    character.addEventListener("mouseenter", () => {
        showPopup(character);
    });

    character.addEventListener("mouseleave", () => {
        hidePopup();
    });
}


function showPopup(character) {
    hidePopup();

    popup = document.createElement("div");
    popup.id = "cn-links-popup";

    popup.textContent = "Recherche...";

    document.body.appendChild(popup);

    const rect = character.getBoundingClientRect();

    const centerX = rect.left + rect.width / 2;
    const topY = rect.bottom + 8;

    popup.style.left = `${centerX}px`;
    popup.style.top = `${topY}px`;

    pycmd(
        `cn-links:${character.textContent}|${window.cnLinksCurrentWord}`,
        (results) => {
            if (!popup) {
                return;
            }

            if (!results || results.length === 0) {
                popup.textContent = "Aucun résultat";
                return;
            }

            displayResults(results);
        }
    );
}


function displayResults(results) {
    popup.innerHTML = "";

    for (const result of results) {
        const row = document.createElement("div");

        row.className = "cn-links-result";
        row.dataset.knowledge = result.knowledge;

        const word = document.createElement("span");
        word.className = "cn-links-word";
        word.textContent = result.word;

        const translation = document.createElement("span");
        translation.className = "cn-links-translation";
        translation.textContent = result.translation;

        row.appendChild(word);
        row.appendChild(translation);

        popup.appendChild(row);
    }
}


function hidePopup() {
    if (popup !== null) {
        popup.remove();
        popup = null;
    }
}

window.cnLinksInit = function () {
    makeCharactersHoverable();
};