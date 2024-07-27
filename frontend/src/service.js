const createPotman = () => {
  fetch("http://localhost:5000/potman", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: "testPost" }),
  }).then((response) => response.json());
};

const getPotman = (id) => {
  fetch(`http://localhost:5000/potman/${id}`)
    .then((response) => response.json())
    .then((data) => console.log("get: ", data));
};

const createStore = () => {
  fetch("http://localhost:5000/store", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ownerId: 4, name: "testStore" }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data));
};

const createPotion = () => {
  fetch("http://localhost:5000/potion", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: "potionTest" }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data));
};

const createStock = () => {
  fetch("http://localhost:5000/stock", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      storeId: 1,
      potionId: 1,
    }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data));
};
