const createPotman = () => {
  fetch("http://localhost:5000/potman", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: "testPost" }),
  }).then((response) => response.json());
};

const getPotman = async (id) => {
  return fetch(`http://localhost:5000/potman/${id}`).then((response) =>
    response.json()
  );
};

const createStore = () => {
  fetch("http://localhost:5000/store", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ownerId: 4, name: "No se Porciones..." }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data));
};

const createPotion = async (name) => {
  try {
    const response = await fetch("http://localhost:5000/potion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    }).then((response) => {
      if (response.status !== 400 && response.status !== 500) {
        return response.json();
      } else {
        throw new Error();
      }
    });

    return response;
  } catch (error) {
    throw new Error(error.message);
  }
};

const createStock = async (storeId, potionId) => {
  try {
    return fetch("http://localhost:5000/stock", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        storeId,
        potionId,
      }),
    }).then((response) => {
      if (response.status !== 400 && response.status !== 500) {
        return response.json();
      } else {
        throw new Error();
      }
    });
  } catch (error) {
    throw new Error(error.message);
  }
};

const postBrew = async (storeId, potionName) => {
  try {
    return fetch("http://localhost:5000/brew", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        storeId,
        potionName,
      }),
    }).then((response) => {
      if (response.status !== 400 && response.status !== 500) {
        return response.json();
      } else {
        throw new Error();
      }
    });
  } catch (error) {
    throw new Error(error.message);
  }
};
