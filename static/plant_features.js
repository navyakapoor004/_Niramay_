document.addEventListener("DOMContentLoaded", function() {
    let scientificName = document.querySelector(".scientific-name");

    if (scientificName) {
        // 🔹 Italicize the scientific name dynamically
        scientificName.style.fontStyle = "italic";
        scientificName.style.color = "#0b4f23";
    }

    let plantImage = document.querySelector(".plant-image");

    if (plantImage) {
        // 🔹 Add hover effect to the image
        plantImage.addEventListener("mouseenter", function() {
            this.style.transform = "scale(1.1)";
            this.style.transition = "transform 0.3s ease-in-out";
        });

        plantImage.addEventListener("mouseleave", function() {
            this.style.transform = "scale(1)";
        });
    }
});
