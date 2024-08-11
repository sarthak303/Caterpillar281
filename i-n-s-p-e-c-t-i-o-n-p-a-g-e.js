document.addEventListener("DOMContentLoaded", function() {
  const uploadVideoButton = document.getElementById("uploadVideoButton");
  const videoInput = document.getElementById("videoInput");
  const previewContainer = document.querySelector(".container-302");
  const transcriptContainer = document.querySelector(".container-332"); // Ensure this class matches your transcript container

  // Create video element for preview
  const videoElement = document.createElement("video");
  videoElement.controls = true;
  videoElement.style.width = "100%";
  videoElement.style.height = "auto";
  previewContainer.appendChild(videoElement);

  uploadVideoButton.addEventListener("click", function() {
    videoInput.click();
  });

  videoInput.addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
      const fileURL = URL.createObjectURL(file);
      videoElement.src = fileURL;
      videoElement.style.display = "block"; // Ensure video is visible

      // Upload video to backend
      const formData = new FormData();
      formData.append('file', file);

      fetch('http://localhost:5000/upload', { // Update with your backend URL
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.transcript) {
          transcriptContainer.textContent = data.transcript; // Update transcript container with the response
        } else {
          transcriptContainer.textContent = "No transcript available.";
        }
      })
      .catch(error => {
        console.error('Error:', error);
        transcriptContainer.textContent = "Error generating transcript.";
      });
    }
  });

  // Other button functionalities
  document.getElementById("submitButton").addEventListener("click", function() {
    alert("Form submitted!");
  });

  document.getElementById("skipButton").addEventListener("click", function() {
    window.location.href = "next-page.html"; // Redirect to the next page
  });
});
