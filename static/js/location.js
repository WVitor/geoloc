async function FindLocation(lat, lng){
    console.log(lat, lng)
    await fetch('https://api-geoloc-iot.onrender.com/maps/reverse-geocode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            lat,
            lng
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        let filterData = null;
        if(Array.isArray(data)){
            filterData = data.filter((item) => {
                if(item.geometry.location.lng.toString() == lng.toString() && item.geometry.location.lat.toString() == lat.toString()){
                    return item;
                }
            })
        }
        if(filterData == null){
            alert("Localização não Encontrada, digite manualmente");
        }
        let searchLocation = document.getElementById('SearchLocationId')
        searchLocation.value = filterData[0].formatted_address;
    })
}

async function LocationSucess(position){
    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'flex';
    await FindLocation(position.coords.latitude, position.coords.longitude);
    loadingElement.style.display = 'none';
}

function LocationError(err){
    console.log(err);
}

async function onClickLocation(){
    //navigator.geolocation.watchPosition(LocationSucess, LocationError);
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(LocationSucess, LocationError);
    }else{
        alert("Seu navegador não suporta a ferramenta de geolocalização.");
    }
}





