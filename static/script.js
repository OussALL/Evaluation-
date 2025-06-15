  function handleRadioClick() {
            const yesRadio = document.getElementById("yesRadio");
            const noRadio = document.getElementById("noRadio");
            const passerButton = document.getElementById("passer");
            const commencerButton = document.getElementById("commencer");

            if (yesRadio.checked) {
                passerButton.disabled = true;
                commencerButton.disabled = false;
            } else if (noRadio.checked) {
                passerButton.disabled = false;
                commencerButton.disabled = true;
            }
        }