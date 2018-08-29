function send(data) {
    var d = JSON.stringify(data)
    xhr.open("POST", "/development", true)
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(d)
}

function generateList(list, place) {
    pl = document.getElementById(place)
    for (var i = pl.childNodes.length - 1; i > 5; i--) {
        pl.childNodes[i].remove()
    }
    for (var i = 0; i < list.length; i++) {
        var listElem = document.createElement("a")
        listElem.innerHTML = list[i]
        listElem.className = "lang-label"
        pl.appendChild(listElem)
    }
}

function getInfo(obj, name) {
    send({"action": "get" + obj + "Info", "name": name})
}

function addIdDiv(row, text) {
    var td = document.createElement("td")
    var div = document.createElement("div")
    div.innerHTML = text
    td.style = "display: None; width: 0%;"
    td.appendChild(div)
    row.appendChild(td)
}

function addDiv(row, style, text) {
    var td = document.createElement("td")
    var div = document.createElement("div")
    div.innerHTML = text
    div.style = style
    td.appendChild(div)
    row.appendChild(td)
}

function cleanString(s) {
    if (s !== "") {
        s = s.slice(1, -1)
        return s
    }
}

function filterFunction(inp, outp) {
    var filter = document.getElementById(inp).value.toUpperCase()
    var div = document.getElementById(outp)
    var a = div.getElementsByTagName("a")
    for (var i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = ""
        } else {
            a[i].style.display = "none"
        }
    }
}

function filterRows(inp, outp) {
    var filter = document.getElementById(inp).value.toUpperCase()
    var tbody = document.getElementById(outp)
    for (var i = 0; i < tbody.childNodes.length; i++) {
        tbody.childNodes[i].style.display = "none"
        for (var j = 0; j < tbody.childNodes[i].childNodes.length; j++) {
            if (tbody.childNodes[i].childNodes[j].childNodes[0].innerHTML.toUpperCase().indexOf(filter) > -1) {
                tbody.childNodes[i].style.display = ""
            }
        }
    }
}

function sortRows(inp, outp) {
    var tbody = document.getElementById(outp)
    var itemsArr = []
    for (var i = 0; i < tbody.childNodes.length; i++) {
        itemsArr.push(tbody.childNodes[i])
    }
    if (itemsArr.length < 2) {
        return null
    }
    if (itemsArr[0].childNodes[inp].childNodes[0].innerHTML < itemsArr[itemsArr.length -
        1].childNodes[inp].childNodes[0].innerHTML) {
        itemsArr.sort(function(a, b) {
            return a.childNodes[inp].childNodes[0].innerHTML == b.childNodes[inp].childNodes[0].innerHTML
              ? 0
              : (a.childNodes[inp].childNodes[0].innerHTML < b.childNodes[inp].childNodes[0].innerHTML ? 1 : -1)
        })
    } else {
        itemsArr.sort(function(a, b) {
            return a.childNodes[inp].childNodes[0].innerHTML == b.childNodes[inp].childNodes[0].innerHTML
              ? 0
              : (a.childNodes[inp].childNodes[0].innerHTML > b.childNodes[inp].childNodes[0].innerHTML ? 1 : -1)
        })
    }
    for (i = 0; i < itemsArr.length; ++i) {
        tbody.appendChild(itemsArr[i])
    }
}

function clearTableBody(name, except="") {
    var t = document.getElementById(name)
    for (var i = t.childNodes.length - 1; i > -1; i--) {
        if (t.childNodes[i].id !== except) {
            t.childNodes[i].remove()
        }
    }
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent")
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none"
    }
    tablinks = document.getElementsByClassName("tablinks")
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "")
    }
    document.getElementById(tabName).style.display = "block"
    evt.currentTarget.className += " active"
}

function showHide() {
    document.getElementById("typesList").classList.toggle("show")
}

/* Types recognition (string, datetime, integer, float, currency, percent) */

function isDatetime(str) {
    if (str.search(/[0-9]{1,2}[.\/][0-9]{1,2}[.\/][0-9]{1,4}/) === -1) {
        return false
    }
    return true
}

function isCurrency(str) {
    if (str.search(/([$¢£¤¥₠₣₤₪€₯₰₱₸₹₽﹩＄￠￥￡￦]\s*[0-9])|([0-9]\s*[$¢£¤¥₠₣₤₪€₯₰₱₸₹₽﹩＄￠￥￡￦])/) === -1) {
        return false
    }
    return true
}

function isPercent(str) {
    if (str.search(/[0-9]\s*%/) === -1) {
        return false
    }
    return true
}

function isFloat(str) {
    if (str.search(/([0-9]*[.,][0-9]+)|([0-9]+[.,][0-9]*)/) === -1) {
        return false
    }
    return true
}

function isInteger(str) {
    if (str.search(/[0-9]+/) === -1) {
        return false
    }
    return true
}