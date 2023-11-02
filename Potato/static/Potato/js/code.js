document.addEventListener("DOMContentLoaded", function () {
  const imageInput = document.getElementById("imageInput");
  const imagePreview = document.getElementById("imagePreview");
  const imagePreview2 = document.getElementById("imagePreview2");
  const submitButton = document.getElementById("submitButton");
  const feedbackDiv = document.getElementById("feedback");
  const backGroundInfo = document.getElementById("backGroundInfo")
  const allInformations = document.getElementById("allInformations")
  allInformations.style.display = "none";
  let buttons;

  // Preview the selected image
  let image;
  imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        image = e.target.result;
        imagePreview.src = image;
        allInformations.style.display = "none";
        imagePreview.style.display = "block";
        backGroundInfo.innerHTML = "";
        feedbackDiv.innerHTML = "";
        
      };
      reader.readAsDataURL(file);
    } else {
      imagePreview.src = "";
      imagePreview.style.display = "none";
    }
  });

  // Send the image to Django on button click
  submitButton.addEventListener("click", function () {
    const file = imageInput.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("image", file);
      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      fetch("predict", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken, // Add the CSRF token to the request headers
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          allInformations.style.display = "block";
          imagePreview2.src = image;
          
          let sick, early, late, healthy, con;
          early = data.early;
          late = data.late;
          healthy = data.healthy;
          

          if (early) sick = "Early Blight";
          else if (late) sick = "Late Blight";
          else if(healthy) sick = "Healthy";
          con = data.confidence;
          
          let diseaseDiv = document.createElement("div");
          let confidenceDiv = document.createElement("div");
          confidenceDiv.classList.add("confidence");
          diseaseDiv.classList.add("disease");
          let cont = `
                <h3>Detected disease:</h3>
                <span id="disease">${sick}</span>
          `

          let cont2 = `
                <h3>Confidence level:</h3>
                <span id="conf_level">${data.confidence}</span>
          `
          diseaseDiv.innerHTML = cont;
          confidenceDiv.innerHTML = cont2;
          
          backGroundInfo.appendChild(diseaseDiv);
          backGroundInfo.appendChild(confidenceDiv);

          
          let i=j = 0;
          let documentation = Object.values(data.documentation);
          let recommendation = documentation[0]["recommendations"];
          let background = documentation[1]["background"];
          

          for (bak in background) {
            let newDiv = document.createElement("div");
            j++;
            for (const bakKey in background[bak]) {
             
              const txtBack = background[bak][bakKey]

                newDiv.classList.add("option");
                newDiv.innerHTML =`
                <div class="left_carton">
                <p class="background" id="background">
                <i><b>${bakKey}</b></i> ${txtBack}
                </p>
                `;
                backGroundInfo.appendChild(newDiv);
            }
          }


          for (key in recommendation) {
            let newDiv = document.createElement("div");
            i++;
            for (const myKey in recommendation[key]) {
              const txt = recommendation[key][myKey]

                newDiv.classList.add("option");
                newDiv.innerHTML =`
                    <h1 id="number">${i}</h1>
                    <h3 id="key">${myKey}:</h3>
                    <p id="explanation">${txt}</p>
                    <button class="botChat">Ask agriBot</button>
                `;
                feedbackDiv.appendChild(newDiv);
            }
          
          }
         
          
        })
        .catch((error) => {
          feedbackDiv.innerHTML = "Error: " + error.message;
          console.log(error.message);
        });

        

    } else {
      feedbackDiv.innerHTML = "Please select an image to upload.";
    }
    buttons = document.querySelectorAll(".botChat");

  });
    console.log(buttons);
    buttons.forEach((button) =>{
      button.addEventListener("click",function(){
        alert("Hello")
          // let ele = this.previousElementSibling;
          // alert(ele.textContent);
      })
  })
});
