let potman;
let store;
let storePotions = [];
let allPotions = [];

const avatar = document.getElementById("avatar");
const cards = document.getElementsByClassName("potion-card");
const progressContainerElement = document.getElementById("progress-container");

const sidebar = document.getElementById("ingridients-sidebar");
const ingridientsContainer = document.getElementById("ingridients-container");
const ingridientsDetailsElement = document.getElementById("ingridient-details");
const descriptionElement = document.getElementById("description");
const effectsElement = document.getElementById("effects");

const potionResultElement = document.getElementById(`potion-result`);
const potionNameElement = document.getElementById("potion-name");

const discoveriesElement = document.getElementById("discoveries");

const brewButton = document.getElementById("brew-button");

let loading = false;

let selectedCard = "";
let selectedCardElement;

let selectedIngridient = {};
let selectedIngridientElement;

let readyToBrew = false;
let brewing = false;
let brewingDone = false;

let potionName = "";

const ingridientVariants = [
  {
    id: "frog-eyes",
    name: "Frog Eyes",
    description:
      "Glistening, bulging eyes of a frog, known for their peculiar squishiness. ( pops in your mouth )",
    effects: ["Enhanced night vision", "Increased jump height"],
    potionName: ["Swampy Potion", "With Tapioca (I hope)"],
  },
  {
    id: "dragon-scales",
    name: "Dragon Scales",
    description: "Tough, shimmering scales of a dragon (They are hard)",
    effects: ["Fire resistance", "Enhanced strength"],
    potionName: ["House Potion", "With a Fiery Kick"],
  },
  {
    id: "unicorn-horn",
    name: "Unicorn Horn",
    description:
      "A rare and mystical horn of a unicorn, A horny beast ( Because it has a horn )",
    effects: ["Healing", "Horny (?)"],
    potionName: ["Horny Elixir", "With a Dash of Hornyness"],
  },
  {
    id: "phoenix-feather",
    name: "Phoenix Feather",
    description:
      "A vibrant feather from a phoenix, glowing with rejuvenating power. ( It keeps bursting into flames )",
    effects: ["Rejuvenation", "Fire immunity"],
    potionName: ["intermittent Flaming Potion", "With Some Sparkling Flames"],
  },
  {
    id: "mermaid-scales",
    name: "Mermaid Scales",
    description:
      "Scales of a mermaid, holding the essence of the ocean. ( They smell like fish )",
    effects: ["Water breathing", "Bad breath"],
    potionName: ["Fishy Potion", "With a Fishy Smell"],
  },
  {
    id: "basilisk-fang",
    name: "Basilisk Fang",
    description: "A sharp fang from a basilisk, filled with potent venom.",
    effects: ["Petrification", "Poison"],
    potionName: ["Venomous Brew", "With a Bite ( You get it? )"],
  },
  {
    id: "fairy-dust",
    name: "Fairy Dust",
    description:
      "Sparkling dust left behind by fairies, full of whimsical energy. ( Things are fliying )",
    effects: ["Levitation", "Glowing"],
    potionName: ["Insects Dust Potion", "With a Tinker Bell"],
  },
  {
    id: "troll-hair",
    name: "Troll Hair",
    description:
      "Thick, coarse hair from a troll, exuding brute strength ( And it smells ) ",
    effects: ["Durability", "Nauseating"],
    potionName: ["Hairy Brew", "With Floating Hair"],
  },
  {
    id: "mandrake-root",
    name: "Mandrake Root",
    description:
      "A gnarled root of a mandrake, known for its potent magical properties. ( It looks like a baby )",
    effects: ["Anti-Petrification", "Screaming"],
    potionName: ["Crying Elixir", "With Potato Flavour"],
  },
  {
    id: "griffin-feather",
    name: "Griffin Feather",
    description: "A feather from a griffin...",
    effects: ["Berserk State", "Guts Discomfort"],
    potionName: ["Berserks Brew", "With Guts Flavour"],
  },
];

let selections = {};

// FUNTIONS
// ---------------------------------
const loadPotman = async () => {
  loading = true;
  const potmanResponse = await getPotman("4");
  if (potmanResponse) {
    potman = potmanResponse;
    store = potman.stores[0];
    storePotions = getStorePotions(store);

    for (let i = 0; i < ingridientVariants.length; i++) {
      for (let j = i; j < ingridientVariants.length; j++) {
        allPotions.push({
          a: ingridientVariants[i],
          b: ingridientVariants[j],
          name: `${ingridientVariants[i].potionName[0]} + ${ingridientVariants[j].potionName[1]}`,
        });
      }
    }

    discoveriesElement.textContent = `${storePotions.length}/${allPotions.length}`;
    progressContainerElement.style.height = `${
      (storePotions.length * 11) / allPotions.length
    }rem`;
  } else {
    alert("The magic core of the potions is broken (unexpected error)");
  }
  loading = false;
};

const handleOnFull = () => {
  const keys = Object.keys(selections);
  if (keys.length === cards.length - 1) {
    let name = "";
    keys.forEach((key, index) => {
      name = `${name} ${selections[key].potionName[index]}`;
    });
    potionName = name.trim();
    potionNameElement.textContent = potionName;
  }
  brewButton.classList.remove("disabled");
  readyToBrew = true;
};

const openSidebar = () => {
  selectedIngridientElement?.classList.remove("selected");
  sidebar.classList.add("visible");
  selectedIngridient = selections[selectedCard];

  console.log(selectedIngridient);
  if (selectedIngridient?.id) {
    selectedIngridientElement = document.getElementById(selectedIngridient.id);
    selectedIngridientElement?.classList.add("selected");
    ingridientsDetailsElement.classList.remove("disabled");
    descriptionElement.textContent = selectedIngridient.description;
    effectsElement.textContent = selectedIngridient.effects.join(", ");
  } else {
    ingridientsDetailsElement.classList.add("disabled");
    descriptionElement.textContent = "";
    effectsElement.textContent = "";
  }
};

const closeSidebar = () => {
  sidebar.classList.remove("visible");

  selectedCardElement?.classList.remove("selected");
  selectedIngridientElement?.classList.remove("selected");
  selectedCardElement = undefined;
  selectedIngridientElement = undefined;
  descriptionElement.textContent = "";
  effectsElement.textContent = "";
  selectedIngridient = {};
  selectedCard = "";
  ingridientsDetailsElement.classList.add("disabled");
};

const onClickCard = (id) => {
  if (!brewing && !brewingDone) {
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
  const newSelectedIngridientElement = document.getElementById(ingridient.id);

  selectedIngridientElement?.classList.remove("selected");
  selectedCardElement.classList.add("assigned");

  newSelectedIngridientElement.classList.add("selected");
  selectedIngridientElement = newSelectedIngridientElement;
  selectedIngridient = ingridient;

  ingridientsDetailsElement.classList.remove("disabled");
  descriptionElement.textContent = ingridient.description;
  effectsElement.textContent = selectedIngridient.effects.join(", ");

  if (Object.keys(selections).length === cards.length - 1) {
    handleOnFull();
  }
};

const onClickBrew = () => {
  if (readyToBrew && !brewingDone) {
    closeSidebar();

    potionResultElement.classList.remove("disabled");

    brewing = true;
    brewButton.disabled = true;
    brewButton.innerHTML = "Brewing";
    brewButton.classList.add("brewing");
    avatar.classList.add("shake-jump");

    for (let card of cards) {
      card.classList.add("shake-jump");

      let i = 0;
      let intervalID = setInterval(function () {
        cards[i].classList.remove("shake-jump");
        if (!cards[i].classList.contains("potion-result")) {
          cards[i].classList.add("disabled");
        }

        i++;
        if (i === cards.length) {
          window.clearInterval(intervalID);
        }
      }, 1000);
    }

    setTimeout(() => {
      brewButton.disabled = false;
      brewButton.classList.remove("brewing");
      avatar.classList.remove("shake-jump");
      brewButton.innerHTML = "Brew";
      potionNameElement.classList.add("revealed");
      brewButton.classList.add("disabled");

      brewing = false;
      brewingDone = true;
    }, 1000 * cards.length);
  }
};

const onClickPotionCard = async () => {
  if (brewingDone) {
    try {
      const { stock } = await postBrew(store.id, potionName);
      const storeStockIndex = store.stocks.findIndex(
        ({ id }) => id === stock.id
      );
      if (storeStockIndex > -1) {
        store.stocks[storeStockIndex] = stock;
      } else {
        store.stocks.push(stock);
      }

      storePotions = getStorePotions(store, stock);
      brewingDone = false;
      potionNameElement.classList.remove("revealed");
      potionName = "";
      potionNameElement.textContent = "";
      selections = {};

      for (let card of cards) {
        if (card.classList.contains("potion-result")) {
          card.classList.add("disabled");
        } else {
          card.classList.remove("disabled");
          card.classList.remove("assigned");
        }
      }
      discoveriesElement.textContent = `${storePotions.length}/${allPotions.length}`;
      progressContainerElement.style.height = `${
        (storePotions.length * 11) / allPotions.length
      }rem`;
    } catch (error) {
      console.log(error);
      alert("The potion is lost in the Disformity");
    }
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

ingridientVariants.forEach((ingridient) => {
  const ingridientElement = document.createElement("div");
  ingridientElement.classList.add("ingridient");
  ingridientElement.id = `${ingridient.id}`;
  ingridientElement.textContent = ingridient.name;

  ingridientElement.onclick = () => onClickIngridient(ingridient);

  ingridientsContainer.appendChild(ingridientElement);
});

document.addEventListener("DOMContentLoaded", loadPotman);
