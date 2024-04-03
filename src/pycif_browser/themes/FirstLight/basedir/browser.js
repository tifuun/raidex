function toggleExpanded(card) {
  if (!card.classList.contains('expanded')) {
    blur();
    popOut(card);
  }
  else {
    unblur();
    setTimeout(() => {popIn(card);}, "540");
    // Timeout gives the animation time to play out
  }

  setTimeout(() => {card.classList.toggle('expanded');}, "10");
}

function popOut(card) {
  // Convert an element's positioning to `fixed`
  // while keeping its relative position on screen
  // THANK YOU https://stackoverflow.com/a/77497727/22930104
  wrap = card.parentElement;

  bbox_wrap = wrap.getBoundingClientRect();
  wrap.style.width = bbox_wrap.width + "px";
  wrap.style.height = bbox_wrap.height + "px";

  wrap.style.maxWidth = bbox_wrap.width + "px";
  wrap.style.minWidth = bbox_wrap.width + "px";

  bbox_card = card.getBoundingClientRect();
  card.style.position = 'fixed';
  card.style.left = bbox_card.x - 7 + "px";
  card.style.top = bbox_card.y - 7 + "px";
  card.style.width = bbox_card.width + "px";
  //card.style.maxWidth = bbox_card.width + "px";
  //card.style.minWidth = bbox_card.width + "px";
}

function popIn(card) {
  wrap = card.parentElement;

  card.style.position = 'relative';
  card.style.left = '';
  card.style.top = '';
  card.style.width = '';
  //card.style.maxWidth = '';
  //card.style.minWidth = '';

  wrap.style.width = '';
  wrap.style.height = '';
  wrap.style.maxWidth = '';
  wrap.style.minWidth = '';
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

function blur() {
  //document.getElementById('blur').classList.add('blur-active');
  document.body.classList.add('blur-active');
}

function unblur() {
  //document.getElementById('blur').classList.remove('blur-active');
  document.body.classList.remove('blur-active');
}

