var React = require("react")

module.exports = React.createClass({
  render: function(){

    // Example of the front-end talking to the back-end

    // Get the socket
    // /co2/ route defined in carbondoomsday.carbondioxide.consumers.py
    var socket = new WebSocket("ws://" + window.location.host + "/co2/");

    // Ask for the CO2Measurement for the 22nd of July
    socket.onopen = function() { socket.send('{"date":"2017-06-22"}'); }

    // Show what we get back in an alert
    socket.onmessage = function(e) {
      console.log("Hi. A message from your loving back-end.");
      console.log("Here is what I sent you.");
      console.log(e.data);
    }

    // When the socket opens, send the request
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

    // Go forth and create an amazing front-end please.
  }
})
