const getStorePotions = (store) => {
  return store.stocks.map(({ potion, amount }) => ({ ...potion, amount }));
};
