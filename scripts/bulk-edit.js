const fs = require('fs');
const path = require('path');
const glob = require('glob'); // npm install glob

// Функция для чтения и записи файлов
function processHtmlFiles(pattern, callback) {
    const files = glob.sync(pattern);

    files.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');
        const newContent = callback(content, file);

        if (newContent !== content) {
            fs.writeFileSync(file, newContent, 'utf8');
            console.log(`✓ Updated: ${file}`);
        }
    });

    console.log(`\nProcessed ${files.length} files.`);
}

// Пример 1: Замена текста
function replaceText(oldText, newText, pattern = '**/*.html') {
    processHtmlFiles(pattern, (content) => {
        return content.replace(new RegExp(oldText, 'g'), newText);
    });
}

// Пример 2: Замена телефона на всех страницах
function updatePhoneNumber(newPhone) {
    processHtmlFiles('**/*.html', (content) => {
        return content
            .replace(/437-747-6737/g, newPhone)
            .replace(/4377476737/g, newPhone.replace(/-/g, ''));
    });
}

// Пример 3: Добавить элемент перед закрывающим тегом
function addBeforeClosing(tag, htmlToAdd, pattern = '**/*.html') {
    processHtmlFiles(pattern, (content) => {
        const regex = new RegExp(`</${tag}>`, 'i');
        return content.replace(regex, `${htmlToAdd}\n</${tag}>`);
    });
}

// Пример 4: Удалить элемент по ID
function removeElementById(elementId, pattern = '**/*.html') {
    processHtmlFiles(pattern, (content) => {
        // Простое удаление (работает для большинства случаев)
        const regex = new RegExp(`<[^>]+id="${elementId}"[^>]*>.*?</[^>]+>`, 'gs');
        return content.replace(regex, '');
    });
}

// Пример 5: Обновить все booking формы
function updateBookingForms(newIframeSrc) {
    processHtmlFiles('**/*.html', (content) => {
        return content.replace(
            /https:\/\/online-booking\.workiz\.com\/\?ac=[a-f0-9]+/g,
            newIframeSrc
        );
    });
}

// Пример 6: Добавить CSS файл в head
function addCssLink(cssPath, pattern = '**/*.html') {
    const cssLink = `<link rel="stylesheet" href="${cssPath}">`;

    processHtmlFiles(pattern, (content) => {
        // Проверяем, есть ли уже этот CSS
        if (content.includes(cssPath)) {
            return content;
        }

        return content.replace('</head>', `    ${cssLink}\n</head>`);
    });
}

// Пример 7: Обновить мета-теги
function updateMetaDescription(newDescription, pattern = '**/*.html') {
    processHtmlFiles(pattern, (content) => {
        return content.replace(
            /<meta name="description" content="[^"]*">/,
            `<meta name="description" content="${newDescription}">`
        );
    });
}

// Пример 8: Заменить целый блок кода
function replaceCodeBlock(startMarker, endMarker, newContent, pattern = '**/*.html') {
    processHtmlFiles(pattern, (content) => {
        const regex = new RegExp(
            startMarker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') +
            '[\\s\\S]*?' +
            endMarker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
            'g'
        );

        return content.replace(regex, startMarker + '\n' + newContent + '\n' + endMarker);
    });
}

// ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

// Заменить телефон:
// updatePhoneNumber('NEW-PHONE-NUMBER');

// Заменить текст только в location pages:
// replaceText('старый текст', 'новый текст', 'locations/*.html');

// Добавить CSS:
// addCssLink('css/new-style.css');

// Удалить элемент:
// removeElementById('old-section-id');

// Обновить все booking формы:
// updateBookingForms('https://new-booking-url.com');

// Заменить блок между маркерами:
// replaceCodeBlock(
//     '<!-- START BOOKING -->',
//     '<!-- END BOOKING -->',
//     '<div>New booking content here</div>',
//     'locations/*.html'
// );

console.log('Bulk edit script loaded. Use the functions above.');
console.log('\nAvailable functions:');
console.log('  replaceText(old, new, pattern)');
console.log('  updatePhoneNumber(newPhone)');
console.log('  addBeforeClosing(tag, html, pattern)');
console.log('  removeElementById(id, pattern)');
console.log('  updateBookingForms(newUrl)');
console.log('  addCssLink(cssPath, pattern)');
console.log('  updateMetaDescription(desc, pattern)');
console.log('  replaceCodeBlock(start, end, content, pattern)');

// Экспорт функций для использования
module.exports = {
    replaceText,
    updatePhoneNumber,
    addBeforeClosing,
    removeElementById,
    updateBookingForms,
    addCssLink,
    updateMetaDescription,
    replaceCodeBlock,
    processHtmlFiles
};
