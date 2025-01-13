
function showPinOnMap(event){
    L.marker([Number(event.id.split(' ')[0]), Number(event.id.split(' ')[1])]).addTo(map);
    event.disabled = true
    event.innerHTML = "Added"
    event.classList.remove("btn-success");
    event.classList.add("btn-primary");
}
    
var map;
window.addEventListener('DOMContentLoaded', event => {
    var workouts = reportRAW['report']['origin']['workouts'];

    let workoutsHTML='';
    let coordinatesHTML='';
    // var map = L.map('map');
    map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);


    var latlngs = [];
    var markers = [];

    workouts.forEach((item) => {
      workoutsHTML+=`        
        <tr>
            <td>${item.type}</td>
            <td>${timeConverter(item.start)}</td>
            <td>${timeConverter(item.end)}</td>
            <td>${item.distance}</td>
            <td>${item.calories}</td>
            <td>${item.steps}</td>
        </tr>
        `

        if(item.coordinates && Array.isArray(item.coordinates)){
            item.coordinates.forEach(coordinate => {
            coordinatesHTML+=`        
            <tr>
                <td>${coordinate.split(' ')[0]}</td>
                <td>${coordinate.split(' ')[1]}</td>
                <td><button type="button" class="btn btn-success" id="${coordinate.split(' ')[0]} ${coordinate.split(' ')[1]}" onclick=showPinOnMap(this)> <i class="fa fa-plus"></i> Add to map</button></td>
            </tr>
            `
            });
            item.coordinates.forEach((coordinate) => {
                if(Number(coordinate.split(' ')[0]) && Number(coordinate.split(' ')[1])){
                    latlngs.push([Number(coordinate.split(' ')[0]), Number(coordinate.split(' ')[1])]);
                }
            });
        }
    });
    
    if (latlngs && latlngs.length > 0) {
        var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);        
        L.marker(latlngs[0]).addTo(map);
        L.marker(latlngs[latlngs.length-1]).addTo(map);
        map.fitBounds(polyline.getBounds());
        map.setZoom(13);
        document.getElementById("emptyMap").style.display = "none";
        
    }else{
        document.getElementById("map").style.display = "none";
        document.getElementById("downloadMap").classList.add("disabled");
    }
    
    
    document.getElementById("workout-records").innerHTML = workoutsHTML;
    document.getElementById("coordinate-records").innerHTML = coordinatesHTML;

    const workoutDatatable = document.getElementById('workout-datatable');
    if (workoutDatatable) {
        new simpleDatatables.DataTable(workoutDatatable);
    }
    const coordinateDatatable = document.getElementById('coordinate-datatable');
    if (coordinateDatatable) {
        new simpleDatatables.DataTable(coordinateDatatable);
    }

    
});


// var map = L.map('map');

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   // attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// let markers = []

// reportData["AF_location"].forEach(item => {

//   timestamp = new Date(item["timestamp"] * 1000);
//   let date = timestamp.toLocaleDateString("pt-PT");
//   let time = timestamp.toLocaleTimeString("pt-PT");

//   popupContent = `
//   <strong>Date:</strong> ${date}<br>
//   <strong>Time:</strong> ${time}<br>
//   <strong>Latitude:</strong> ${item["latitude"]}<br>
//   <strong>Longitude:</strong> ${item["longitude"]}<br>
//   `

//   markers.push([item.latitude, item.longitude])
//   L.marker([item["latitude"], item["longitude"]]).addTo(map)

//     .bindPopup(popupContent)
//     .openPopup();


// });

// map.fitBounds(markers);
// map.setZoom(13);
// }