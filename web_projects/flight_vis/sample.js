function myFunction() {
  document.getElementById("demo").innerHTML = "God No!";
}

document.body.onload = function showMap() {
    // Creating map options
    var mapOptions = {
       center: [17.385044, 78.486671],
       zoom: 10
    }
     
    // Creating a map object
    var map = new L.map('map', mapOptions);
     
    // Creating a Layer object
    var layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
     
    // Adding layer to the map
    map.addLayer(layer);
}