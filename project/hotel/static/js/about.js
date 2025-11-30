// ===== DYNAMIC ROOMS SECTION =====
const roomList = document.getElementById("roomList");

const rooms = [
    {
        name: "Luxury Suite",
        desc: "Spacious suite with premium amenities and city view.",
        price: "₹8000/night",
        img: "{% static 'images/room4.jpg' %}"
    },
    {
        name: "Dorm Room",
        desc: "Affordable dorm-style room for backpackers and solo travelers.",
        price: "₹1000/night",
        img: "{% static 'images/room5.jpg' %}"
    },
    {
        name: "Ocean View Suite",
        desc: "Room with a breathtaking ocean view and king-size bed.",
        price: "₹9000/night",
        img: "{% static 'images/room6.jpg' %}"
    },
    {
        name: "Family Room",
        desc: "Comfortable room perfect for a family stay.",
        price: "₹6000/night",
        img: "{% static 'images/room7.jpg' %}"
    },
    {
        name: "Executive Room",
        desc: "Premium room with workspace and luxury facilities.",
        price: "₹7500/night",
        img: "{% static 'images/room8.jpg' %}"
    }
];

rooms.forEach(room => {
    const card = document.createElement("div");
    card.className = "room-card";
    card.innerHTML = `
        <img src="${room.img}" alt="${room.name}">
        <h3>${room.name}</h3>
        <p>${room.desc} <br> <strong>${room.price}</strong></p>
    `;
    roomList.appendChild(card);
});

// ===== OPTIONAL: SCROLL ANIMATION =====
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.room-card');
    const triggerBottom = window.innerHeight / 5 * 4;

    elements.forEach(el => {
        const boxTop = el.getBoundingClientRect().top;
        if(boxTop < triggerBottom){
            el.classList.add('show');
        } else {
            el.classList.remove('show');
        }
    });
});
