document.addEventListener("DOMContentLoaded", () => {
  const rooms = [
    {
      name: "Deluxe Room",
      image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
      desc: "Spacious deluxe room with modern facilities, balcony view, and 24/7 service.",
      price: "₹3,500 / night"
    },
    {
      name: "Single Room",
      image: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
      desc: "Perfect for solo travelers. Cozy, comfortable, and affordable stay.",
      price: "₹1,200 / night"
    },
    {
      name: "Family Suite",
      image: "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=800&q=80",
      desc: "Spacious suite for the entire family with attached kitchen and private balcony.",
      price: "₹5,000 / night"
    },
    {
      name: "Executive Suite",
      image: "https://images.unsplash.com/photo-1582719478171-2b1a79a8f6b0?auto=format&fit=crop&w=800&q=80",
      desc: "Luxurious suite for business professionals with workspace and lounge access.",
      price: "₹6,500 / night"
    },
    {
      name: "Dormitory Room",
      image: "https://images.unsplash.com/photo-1616594039964-ae9021a62e6b?auto=format&fit=crop&w=800&q=80",
      desc: "Shared dorm for budget travelers. Clean beds, lockers, and free Wi-Fi.",
      price: "₹800 / night"
    },
    {
      name: "Luxury Villa",
      image: "https://images.unsplash.com/photo-1501117716987-c8e1ecb2106f?auto=format&fit=crop&w=800&q=80",
      desc: "Private villa with swimming pool, garden, and personal butler service.",
      price: "₹12,000 / night"
    }
  ];

  const roomList = document.getElementById("roomList");
  roomList.innerHTML = rooms.map(room => `
    <div class="room-card">
      <img src="${room.image}" alt="${room.name}">
      <div class="details">
        <h3>${room.name}</h3>
        <p>${room.desc}</p>
        <p class="price">${room.price}</p>
      </div>
    </div>
  `).join('');
});
