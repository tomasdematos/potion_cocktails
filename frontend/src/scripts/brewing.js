const avatar = document.getElementById("avatar");
const cards = document.getElementsByClassName("potion-card");

const sidebar = document.getElementById("ingridients-sidebar");
const ingridientsContainer = document.getElementById("ingridients-container");
const potionNameElement = document.getElementById("potion-name");

let selectedCard = "";
let selectedCardElement;

let selectedIngridient = "";
let selectedIngridientElement;

let brewing = false;
let ready = false;

let potionName = "";

const ingridients = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

const selections = {};

// FUNTIONS
// ---------------------------------
const handleOnFull = () => {
  const resultElement = document.getElementById(`potion-result`);
  resultElement.classList.remove("disabled");
  ready = true;
};

const openSidebar = () => {
  selectedIngridientElement?.classList.remove("selected");
  sidebar.classList.add("visible");
  const sidebarTitle = document.getElementById("sidebar-title");
  sidebarTitle.textContent = selectedCard;
  selectedIngridient = selections[selectedCard];

  if (selectedIngridient != "") {
    selectedIngridientElement = document.getElementById(
      `ingridient-${selectedIngridient}`
    );
    selectedIngridientElement?.classList.add("selected");
  }
};

const closeSidebar = () => {
  sidebar.classList.remove("visible");

  selectedCardElement?.classList.remove("selected");
  selectedIngridientElement?.classList.remove("selected");
  selectedCardElement = undefined;
  selectedIngridientElement = undefined;
  selectedIngridient = "";
  selectedCard = "";
};

const onClickCard = (id) => {
  if (!brewing) {
    selectedCard = id;

    for (let card of cards) {
      if (card.id === selectedCard) {
        card.classList.add("selected");
        selectedCardElement = card;
      } else {
        card.classList.remove("selected");
      }
    }

    openSidebar();
  }
};

const onClickIngridient = (ingridient) => {
  selections[selectedCardElement.id] = ingridient;
  const newSelectedIngridientElement = document.getElementById(
    `ingridient-${ingridient}`
  );

  selectedIngridientElement?.classList.remove("selected");
  selectedCardElement.classList.add("assigned");

  newSelectedIngridientElement.classList.add("selected");
  selectedIngridientElement = newSelectedIngridientElement;
  selectedIngridient = ingridient;

  if (Object.keys(selections).length === cards.length - 1 && !ready) {
    handleOnFull();
  } else if (ready) {
    potionName = "";
  }
};

const onClickBrew = () => {
  const button = document.getElementById("brew-button");
  brewing = true;
  button.disabled = true;
  button.innerHTML = "Brewing";
  button.classList.add("loading");
  avatar.classList.add("shake-jump");

  for (let card of cards) {
    card.classList.add("shake-jump");

    let i = 0;
    let intervalID = setInterval(function () {
      cards[i].classList.remove("shake-jump");
      i++;
      if (i === cards.length) {
        window.clearInterval(intervalID);
      }
    }, 1000);
  }

  setTimeout(() => {
    button.disabled = false;
    button.classList.remove("loading");
    avatar.classList.remove("shake-jump");
    button.innerHTML = "Brew";
    console.log(potionNameElement);
    potionNameElement.classList.add("revealed");
    brewing = false;
  }, 1000 * cards.length);
};

const onClickPotionCard = () => {
  const keys = Object.keys(selections);
  if (keys.length === cards.length - 1) {
    console.log("new potion for you", selections);
    let name = "";
    keys.forEach((key) => {
      name = `${name} ${selections[key]}`;
    });
    // createPotion(name.trimStart());
    potionName = name;
    potionNameElement.textContent = potionName;
  }
};

// INIT
// ---------------------------------
for (let card of cards) {
  if (!card.classList.contains("potion-result")) {
    card.onclick = () => onClickCard(card.id);
  } else {
    card.onclick = () => onClickPotionCard(card.id);
  }
}

for (let i = 0; i < ingridients.length; i++) {
  const ingridientElement = document.createElement("div");
  ingridientElement.classList.add("ingridient");
  ingridientElement.id = `ingridient-${ingridients[i]}`;
  ingridientElement.textContent = ingridients[i];

  ingridientElement.onclick = () => onClickIngridient(ingridients[i]);

  ingridientsContainer.appendChild(ingridientElement);
}

function myClick() {
  console.log("This is in click");
  afterClick();
}

function afterClick() {
  console.log("This is after click");
}
