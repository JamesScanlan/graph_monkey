function highlight_line(id) {
      
    if (document.getElementById(id).getAttribute("class") == "highlighted") {
        document.getElementById(id).setAttribute("class","");
    } else {
        document.getElementById(id).setAttribute("class","highlighted");
    }

    highlight_legend(id);
}

function highlight_lines(id) {
    highlight_by_tag('polyline', id);
    highlight_by_tag('line', id);
    highlight_legend(id);
}

function highlight_by_tag(tagname, id) {
    items = document.getElementsByTagName(tagname);
    for (item of items) {
        if (item.getAttribute('id') == id) {
            if (item.getAttribute("class") == "highlighted") {
                item.setAttribute("class", "")
            } else {
                item.setAttribute("class","highlighted")
            }
        }
    }
}

function highlight_legend(id) {
    // window.alert(id);
    items = document.getElementsByTagName('text');
    for (item of items) {
        if (item.getAttribute('id') == id) {
            if (item.getAttribute("class") == "legend_item_highlighted") {
                item.setAttribute("class", "legend_item")
            } else {
                item.setAttribute("class","legend_item_highlighted")
            }    
        }
    }
}