function createXMLHttpRequestObject() {
    if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    }
    if (window.ActiveXObject) {
        var names = [
            "Msxml2.XMLHTTP.6.0",
            "Msxml2.XMLHTTP.3.0",
            "Msxml2.XMLHTTP",
            "Microsoft.XMLHTTP"
        ];
        for (var i in names) {
            try {
                return new ActiveXObject(names[i]);
            }
            catch(e) {}
        }
    }
    throw new Error("This browser does not support XMLHttpRequest.");
}

function downloadFile(filename, callback) {
    var xhr = createXMLHttpRequestObject();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            callback(xhr.responseText);
        }
    }
    xhr.open('GET', filename, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send(null);
    return xhr;
}

function parseJson(jsonText) {
    if (typeof JSON === 'object' && typeof JSON.parse === 'function') {
        return JSON.parse(jsonText);
    } else {
        return eval('(' + jsonText + ')');
    }
}

var index = null;

downloadFile('search-index.json', function(content) {
    index = parseJson(content);
});

function searchLolis(query, groups) {
    var results = [];
    var queryWords = query.split(' ');
    for (var i in groups) {
        for (var j in index[groups[i]]) {
            var loli = index[groups[i]][j];
            var foundWordsCount = 0;
            for (var k in queryWords) {
                for (var l in loli['keywords']) {
                    if (loli['keywords'][l].indexOf(queryWords[k]) != -1) {
                        foundWordsCount++;
                        break;
                    }
                }
            }
            if (foundWordsCount == queryWords.length) {
                results.push(loli['fname']);
            }
        }
    }
    return results;
}

var loliXhrs = [];

function updateResults(resultsContainer, results) {
    for (var i in results) {
        var xhr = downloadFile(results[i], function(content) {
            var tmpContainer = document.createElement('div');
            var matches = content.match(/(<article (.|\n)+<\/article>)/);
            tmpContainer.innerHTML = matches[0];
            resultsContainer.appendChild(tmpContainer.firstChild);
        });
        loliXhrs.push(xhr);
    }
}

var searchQueryInput = document.getElementById('search-query');
var searchLolisCheckbox = document.getElementById('search-lolis');
var searchGranniesCheckbox = document.getElementById('search-grannies');
var resultsContainer = document.getElementById('results');

var query = null;
var lolisFilter = null;
var granniesFilter = null;

var prevQuery = null;
var prevLolisFilter = null;
var prevGranniesFilter = null;

function formStateChanged() {
    if (query != prevQuery
            || lolisFilter != prevLolisFilter
            || granniesFilter != prevGranniesFilter) {
        prevQuery = query;
        prevLolisFilter = lolisFilter;
        prevGranniesFilter = granniesFilter
        return true;
    }
    return false;
}

function processSearch() {
    query = searchInputField.value.toLowerCase();
    lolisFilter = searchLolisCheckbox.checked;
    granniesFilter = searchGranniesCheckbox.checked;
    if (formStateChanged()) {
        for (var i in loliXhrs) {
            loliXhrs[i].abort();
        }
        loliXhrs.length = 0;
        resultsContainer.innerHTML = '';
        if (query.length >= 2) {
            var groups = [];
            if (lolisFilter) {
                groups.push('lolis');
            }
            if (granniesFilter) {
                groups.push('grannies');
            }
            var results = searchLolis(query, groups);
            updateResults(resultsContainer, results);
        }
    }
}

window.onload = function() {
    searchInputField = document.getElementById('search-input');
    searchLolisCheckbox = document.getElementById('search-lolis');
    searchGranniesCheckbox = document.getElementById('search-grannies');
    resultsContainer = document.getElementById('results');

    searchInputField.onkeyup = processSearch;
    searchLolisCheckbox.onclick = processSearch;
    searchGranniesCheckbox.onclick = processSearch;
};

