const genieLines = [
    "🌿 I'm Nira! Ask me about any healing plant!",
    "🍃 Neem purifies blood and helps with skin issues!",
    "🌱 Tulsi boosts immunity & fights infections!",
    "💧 Aloe Vera heals burns and soothes your skin!",
    "✨ Nature has the cure. Just type a plant’s name!"
  ];
  
  let index = 0;
  const genieMsg = document.getElementById("genieMsg");
  
  setInterval(() => {
    index = (index + 1) % genieLines.length;
    genieMsg.innerText = genieLines[index];
  }, 5000);
  