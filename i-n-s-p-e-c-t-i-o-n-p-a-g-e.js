
      var sUBMITContainer = document.getElementById("sUBMITContainer");
      if (sUBMITContainer) {
        sUBMITContainer.addEventListener("click", function (e) {
          window.location.href = "./p-d-f-preview.html";
        });
      }
      
      var logoImage = document.getElementById("logoImage");
      if (logoImage) {
        logoImage.addEventListener("click", function (e) {
          window.location.href = "./index.html";
        });
      }
      
      var linkColumnItem11 = document.getElementById("linkColumnItem11");
      if (linkColumnItem11) {
        linkColumnItem11.addEventListener("click", function (e) {
          window.location.href = "./index.html";
        });
      }
      
      var linkColumnItem12 = document.getElementById("linkColumnItem12");
      if (linkColumnItem12) {
        linkColumnItem12.addEventListener("click", function (e) {
          window.location.href = "./index.html";
        });
      }
      
      var linkColumnItem13 = document.getElementById("linkColumnItem13");
      if (linkColumnItem13) {
        linkColumnItem13.addEventListener("click", function () {
          var anchor = document.querySelector("[data-scroll-to='navContainer']");
          if (anchor) {
            anchor.scrollIntoView({ block: "start", behavior: "smooth" });
          }
        });
      }
    
