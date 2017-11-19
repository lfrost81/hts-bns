function change_bar_value(barId, valueId) {
     var slider = document.getElementById(barId);
     var output = document.getElementById(valueId);
     output.innerHTML = slider.value; // Display the default slider value

     // Update the current slider value (each time you drag the slider handle)
     slider.oninput = function() {
        output.innerHTML = this.value;
     }
}