const messages = [
    "🌿 Stay hydrated and take deep breaths.",
    "🍋 Vitamin C boosts your immunity.",
    "🧘‍♀️ 10 mins of yoga can do wonders!",
    "😴 A good sleep heals half the body.",
    "🥦 Eat green, stay clean.",
    "🧴 Massage with coconut oil reduces stress.",
    "🌞 Early sun gives natural vitamin D.",
    "🍵 Tulsi tea soothes sore throat."
  ];
  
  let index = 0;
  const genieMsg = document.getElementById("genieMsg");
  
  setInterval(() => {
    index = (index + 1) % messages.length;
    genieMsg.innerText = messages[index];
}, 5000);

  