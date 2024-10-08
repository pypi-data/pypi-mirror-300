document.addEventListener("DOMContentLoaded", (event) => {
  const updateGPSLocation = (lat, lon, alt, ts) => {
    const latitude = document.getElementById("latitude");
    const longitude = document.getElementById("longitude");
    const altitude = document.getElementById("altitude");
    const gps_timestamp = document.getElementById("gps-timestamp");

    latitude.textContent = lat;
    longitude.textContent = lon;
    altitude.textContent = alt;
    gps_timestamp.textContent = ts;
  };

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "location_update") {
      updateGPSLocation(
        data.latitude,
        data.longitude,
        data.altitude,
        data.gps_timestamp
      );
    }
  });
});
