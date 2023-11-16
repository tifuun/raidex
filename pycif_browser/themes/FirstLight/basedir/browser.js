function toggleExpanded(compo) {
  /*compo = button.parentElement*/
  wrap = compo.parentElement

  if (!compo.classList.contains('expanded')) {
    popOutWidth(wrap);
    popOut(compo);
  }
  else {
    setTimeout(() => {popIn(compo);popInWidth(wrap);}, "320");
    // Timeout gives the animation time to play out
  }

  setTimeout(() => {compo.classList.toggle('expanded');}, "10");
  //compo.classList.toggle('expanded');

}

function popOut(elem) {
  // Convert an element's positioning to `absolute`
  // while keeping its relative position on screen
  bbox = elem.getBoundingClientRect();
  elem.style.position = 'fixed';
  elem.style.left = bbox.x + "px";
  elem.style.top = bbox.y + "px";
  elem.style.width = bbox.width + "px";
  //elem.style.left = elem.offsetLeft + "px";
  //elem.style.top = elem.offsetTop + "px";
}

function popIn(elem) {
  elem.style.position = 'relative';
  elem.style.left = "";
  elem.style.top = "";
  elem.style.width = "";
}

function popOutWidth(elem) {
  elem.style.width = elem.clientWidth + "px";
  elem.style.height = elem.clientHeight + "px";
}

function popInWidth(elem) {
  elem.style.width = "";
  elem.style.height = "";
}

// THANK YOU
// https://css-tricks.com/in-page-filtered-search-with-vanilla-javascript/
function liveSearch(key, child_selector, hide_class) {

  key = key.toLowerCase();

  let cards = document.querySelectorAll('.compo-wrap');

  for (var i = 0; i < cards.length; i++) {

    child = cards[i].querySelector(child_selector);
    text = child.innerText.toLowerCase();

    if(text.includes(key)) {
      cards[i].classList.remove(hide_class);
    } else {
      cards[i].classList.add(hide_class);
    }
  }
}

