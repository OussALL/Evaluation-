function handleRadioClick() {
    const yesRadio = document.getElementById("yesRadio");
    const noRadio = document.getElementById("noRadio");
    const passerButton = document.getElementById("passer");
    const commencerButton = document.getElementById("commencer");
    const teacherSelect = document.getElementById("teachers");

    const isTeacherSelected = teacherSelect.value !== "";

    if (yesRadio.checked && isTeacherSelected) {
        passerButton.disabled = true;
        passerButton.style.backgroundColor = "#5c5c5c";


        commencerButton.disabled = false;
        commencerButton.style.backgroundColor = "green";

    } else if (noRadio.checked && isTeacherSelected) {
        passerButton.disabled = false;
        passerButton.style.backgroundColor = "green";

        commencerButton.style.backgroundColor = "#5c5c5c";
        commencerButton.disabled = true;
    } else {
        passerButton.disabled = true;
        commencerButton.disabled = true;
        commencerButton.style.backgroundColor = "#5c5c5c";
        passerButton.style.backgroundColor = "#5c5c5c";


    }
}

// Add an event listener to the teacher select element to handle changes
document.getElementById("teachers").addEventListener("change", handleRadioClick);
